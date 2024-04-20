import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import wikipedia
import re


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


wikipedia.set_lang("ru")


reply_keyboard = [['/Guess_the_word', '/describe_the_word'],
                  ['/stop'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


# async def close_keyboard(update, context):
#     await update.message.reply_text(
#         "Ok",
#         reply_markup=ReplyKeyboardRemove()
#     )

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
        "Описание бота.\n"
        "Игра угадай слово: /Guess_the_word.\n"
        "Игра опиши слово: /describe_the_word.",
        reply_markup=markup
    )

#     await update.message.reply_text(
#         "Я бот-справочник. Какая информация вам нужна?",
#         reply_markup=markup
#     )


# async def start(update, context):
#     await update.message.reply_text(
#         "Привет. Пройдите небольшой опрос, пожалуйста!\n"
#         "Вы можете прервать опрос, послав команду /stop.\n"
#         "В каком городе вы живёте?", reply_markup=markup)
#
#     # Число-ключ в словаре states —
#     # втором параметре ConversationHandler'а.
#     return 1
#     # Оно указывает, что дальше на сообщения от этого пользователя
#     # должен отвечать обработчик states[1].
#     # До этого момента обработчиков текстовых сообщений
#     # для этого пользователя не существовало,
#     # поэтому текстовые сообщения игнорировались.


# # Добавили словарь user_data в параметры.
# async def first_response(update, context):
#     # Сохраняем ответ в словаре.
#     context.user_data['locality'] = update.message.text
#     await update.message.reply_text(
#         f"Какая погода в городе {context.user_data['locality']}?")
#     return 2


# # Добавили словарь user_data в параметры.
# async def second_response(update, context):
#     weather = update.message.text
#     logger.info(weather)
#     # Используем user_data в ответе.
#     await update.message.reply_text(
#         f"Спасибо за участие в опросе! Привет, {context.user_data['locality']}!")
#     context.user_data.clear()  # очищаем словарь с пользовательскими данными
#     return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")


async def help(update, context):
    await update.message.reply_text(
        "Все команды:\n"
        "Начать заново: /start or /stop.\n"
        "Игра Угадай слово: /Guess_the_word.\n"
        "Игра Опиши слово: /describe_the_word."
    )


async def Guess_the_word(update, context):
    await update.message.reply_text(
        "Игра Угадай слово")


async def describe_the_word(update, context):
    await update.message.reply_text(
        "Игра Опиши слово")


async def wiki(update, context):
    await update.message.reply_text(wiki_text(update.message.text))


def main():
    application = Application.builder().token('6849720257:AAEF065UJMXeZfny0Dljn6wzSyNOf-ttOyU').build()

    # conv_handler = ConversationHandler(
    #     # Точка входа в диалог.
    #     # В данном случае — команда /start. Она задаёт первый вопрос.
    #     entry_points=[CommandHandler('start', start)],
#
    #     # Состояние внутри диалога.
    #     # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
    #     states={
    #         # Функция читает ответ на первый вопрос и задаёт второй.
    #         1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
    #         # Функция читает ответ на второй вопрос и завершает диалог.
    #         2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
    #     },
#
    #     # Точка прерывания диалога. В данном случае — команда /stop.
    #     fallbacks=[CommandHandler('stop', stop)]
    # )
#
    # application.add_handler(conv_handler)

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("Guess_the_word", Guess_the_word))
    application.add_handler(CommandHandler("describe_the_word", describe_the_word))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("help", help))

    # application.add_handler(CommandHandler("close", close_keyboard))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, wiki)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
