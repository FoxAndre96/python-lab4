from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import pymysql


def print_options(list_task):
    string = ''
    for (i, item) in list_task.items():
        string += str(item) + '\n'
    return string


def print_tasks(list_task):
    string = ''
    for item in list_task:
        string += str(item[1]) + '\n'
    return string


def remove_item(list_task, item):
    for element in list_task:
        element = element.split()
        if item in element:
            element = ' '.join(element)
            list_task.remove(element)


def start(bot, update):
    options = {
        1: "/showTasks",
        2: "/newTask",
        3: "/removeTask",
        4: "/removeAllTasks"
    }

    bot.send_message(chat_id=update.message.chat_id, text=print_options(options))


def error_text(bot, update):
    # simulate typing from the bot
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

    # send the error message
    update.message.reply_text("I'm sorry. I can't do that.")


def show_tasks(update):
    sql = 'SELECT todo FROM to_do_list'
    cursor = conn.cursor()
    cursor.execute(sql)
    tasks = cursor.fetchall()
    if len(tasks) == 0:
        update.message.reply_text("Nothing to do, here!")
        conn.close()
    else:
        update.message.reply_text(print_tasks(tasks))
        conn.close()


def new_task(update, args):
    sql = 'INSERT INTO to_do_list VALUES (%s,%s)'
    task = ' '.join(args)
    cursor = conn.cursor()
    try:
        cursor.execute(sql, ('', task))
        conn.commit()
        update.message.reply_text("Task successfully added.")
    except Exception as e:
        print(str(e))
        conn.rollback()
        update.message.reply_text("Error in adding the task.")
    conn.close()


def remove_task(update, args):
    try:
        task = ' '.join(args)
        sql = 'DELETE FROM to_do_list WHERE todo="%s"'
        cursor = conn.cursor()
        cursor.execute(sql, task)
        update.message.reply_text("The task was successfully deleted.")
    except ValueError:
        update.message.reply_text("The task you specified is not in the list.")


def remove_all(args):
    task = ' '.join(args)
    sql = 'DELETE FROM to_do_list WHERE todo LIKE "%%s%"'
    cursor = conn.cursor()
    cursor.execute(sql, task)


if __name__ == "__main__":
    conn = pymysql.connect(user='root', password='', host='localhost', database='tasks')

    updater = Updater('Code API')

    # dispatcher
    dp = updater.dispatcher

    # add the command handler commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", show_tasks))
    dp.add_handler(CommandHandler("newTask", new_task, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", remove_task, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", remove_all, pass_args=True))

    dp.add_handler(MessageHandler(Filters.text, error_text))

    # start the bot
    updater.start_polling()

    updater.idle()