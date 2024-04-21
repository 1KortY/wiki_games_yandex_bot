import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import wikipedia
import re
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

wikipedia.set_lang("ru")

reply_keyboard = [['/guess_the_word', '/describe_the_word'],
                  ['/stop'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


words = ['топор', 'утро', 'сон', 'море', 'пирог', 'часы', 'флаг',
         'мяч', 'дерево', 'змея', 'дверь', 'стол', 'кот', 'собака',
         'гвоздь', 'дождь', 'шапка', 'хлеб', 'фильм', 'письмо', 'фрукт',
         'алмаз', 'яйцо', 'чайник', 'поезд', 'рыба', 'рюкзак', 'карандаш']
n = ''


def wiki_text(word):
    try:
        page = wikipedia.page(word)
        # Получаем первую тысячу символов
        wikitext = page.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikitext = wikimas[:-1]
        # Создаем пустую переменную для текста
        text = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikitext:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if (len((x.strip())) > 3):
                    text = text + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        text = re.sub('\([^()]*\)', '', text)
        text = re.sub('\([^()]*\)', '', text)
        text = re.sub('\{[^\{\}]*\}', '', text)
        # Возвращаем текстовую строку
        return text
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        "Привет " + user.mention_html() + "!\n"
        "Я бот помогающий найти информацию о слове.\n"
        "Просто напишите мне любое слово и я выведу информацию о нём.\n"
        "\n"
        "Так же я могу поиграть с вами в игры:\n"
        "Игра угадай слово: /guess_the_word.\n"
        "Игра опиши слово: /describe_the_word.",
        reply_markup=markup
    )


async def stop(update, context):
    await update.message.reply_text(
        "Просто напишите мне любое слово и я выведу информацию о нём.\n"
        "\n"
        "Так же я могу поиграть с вами в игры:\n"
        "Игра угадай слово: /guess_the_word.\n"
        "Игра опиши слово: /describe_the_word."
    )
    return ConversationHandler.END


async def help(update, context):
    await update.message.reply_text(
        "Все команды:\n"
        "Начать заново: /start or /stop.\n"
        "Игра Угадай слово: /guess_the_word.\n"
        "Игра Опиши слово: /describe_the_word."
    )


def short_answer(t):
    global words
    global n

    if t == 1:
        n = random.choice(words)
        a = wiki_text(n).split()
        a[0] = '???'
    else:
        a = wiki_text(t).split()
    a = ' '.join(a)
    a = a.split('.')
    a = ''.join(a[0]) + '.'
    return a


async def guess_the_word(update, context):
    await update.message.reply_text(
        'Игра угадай слово.\n'
        '\n'
        'Я скажу вам определение слова которое загадал,\n'
        'А вам предстоит угадать это слово.\n'
        'Все просто :)\n'
        '\n'
        'Команда для выхода из игры: /stop.'
    )
    await update.message.reply_text(short_answer(1))
    await update.message.reply_text('Какое слово я загадал?')
    return 1


async def guess_response(update, context):
    global n
    answer = update.message.text
    if n in answer or n.capitalize() in answer:
        await update.message.reply_text('Отлично, вы угадали слово!')
        return ConversationHandler.END
    else:
        await update.message.reply_text('Вы не угадали :(\n'
                                        'Подумайте лучше и напишите ответ снова.\n'
                                        'или попробуйте другие функции: /stop.')


async def describe_the_word(update, context):
    global words
    global n
    n = random.choice(words)
    await update.message.reply_text(
        "Игра опиши слово.\n"
        "\n"
        "Я называю слово, которое мы с вами должны описать.\n"
        "Я сверю наши ответы и скажу похожи они или нет."
    )
    await update.message.reply_text(f'Давайте опишем слово: {n.capitalize()}.')
    return 2


async def describe_response(update, content):
    global n
    sa = short_answer(n)
    count = 0
    answer = update.message.text.split()
    for i in answer:
        if i in sa:
            count += 1
    if count * 100 / len(answer) >= 15:
        await update.message.reply_text('Отлично, наши ответы похожи!\n'
                                        '\n'
                                        'Вот мой ответ:\n'
                                        f'{sa}')
        return ConversationHandler.END
    else:
        await update.message.reply_text('Наши ответы разные :(\n'
                                        'Вот мой ответ:\n'
                                        '' + sa + '\n'
                                        '\n'
                                        'Подумайте лучше и напишите ответ снова.\n'
                                        '\n'
                                        'или попробуйте другие функции: /stop.\n')


async def wiki(update, context):
    await update.message.reply_text(wiki_text(update.message.text))


def main():
    application = Application.builder().token('6849720257:AAEF065UJMXeZfny0Dljn6wzSyNOf-ttOyU').build()

    guess = ConversationHandler(
        entry_points=[CommandHandler('guess_the_word', guess_the_word)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, guess_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    describe = ConversationHandler(
        entry_points=[CommandHandler('describe_the_word', describe_the_word)],

        states={
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, describe_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(guess)
    application.add_handler(describe)

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("guess_the_word", guess_the_word))
    application.add_handler(CommandHandler("describe_the_word", describe_the_word))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("help", help))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, wiki)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
