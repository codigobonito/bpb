import locale
import logging
from telegram import ext
from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser


# Helper functions and variables
def parse_date(date_args):
    if isinstance(date_args, (list, tuple)):
        date_args = " ".join(date_args)
    elif isinstance(date_args, datetime):
        date_args = str(date_args)
    datetime_obj = dateutil_parser.parse(date_args)
    parsed_date = datetime_obj.strftime("%A %Hh, %d %b %Y")
    return parsed_date, datetime_obj


please_schedule = " Por favor marque um horário com o comando /setmeeting."


# Handlers
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, sou o BPB!")


def get_meeting(update, context):
    try:
        datetime_obj = getattr(context.bot, "next_meeting")
        parsed_date, _ = parse_date(datetime_obj)
        message = f"A próxima reunião está marcada para:\n {parsed_date}.\n".lower().capitalize()
        try:
            next_meetings = getattr(context.bot, "next_meetings")
            message += "Esse horário irá se repetir pelas próximas 4 semanas:\n"
            message += " \n".join(i[0] for i in next_meetings)
        except AttributeError:
            pass
    except Exception as _:
        message = "Nenhuma reunião marcada." + please_schedule

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def set_meeting(update, context):
    try:
        # Get message meeting and following ones
        parsed_date, datetime_obj = parse_date(context.args)
        next_meetings, interval = [
            (parsed_date, datetime_obj),
        ], 7
        for i in range(3):
            next_meetings.append(parse_date(datetime_obj + timedelta(days=interval)))
            interval += interval

        # Add attributes to bot
        context.bot.next_meeting = datetime_obj
        context.bot.next_meetings = next_meetings

        message = f"Reunião marcada para:\n {parsed_date}.\n".lower().capitalize()
        message += "Esse horário irá se repetir pelas próximas 4 semanas:\n"
        message += " \n".join(i[0] for i in context.bot.next_meetings)
    except Exception as e:
        message = (
            "Não consegui marcar a reunião. Por favor verifique a mensagem submetida.\n"
        )
        message += f"'{' '.join(context.args)}'"
        print(e)

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def clear_meetings(update, context):
    try:
        delattr(context.bot.next_meeting)
        delattr(context.bot.next_meetings)
        message = "Limpei a agenda de reuniões." + please_schedule
    except AttributeError:
        message = "Nenhuma reunião agendada."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


start_handler = ext.CommandHandler("start", start)
set_meeting_handler = ext.CommandHandler("setmeeting", set_meeting)
get_meeting_handler = ext.CommandHandler("getmeeting", get_meeting)
clear_meetings_handler = ext.CommandHandler("clear", clear_meetings)


def main():
    # Configuration
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    locale.setlocale(locale.LC_TIME, "pt_BR")
    with open("token.txt") as f:
        token = f.read().strip()

    # Defining bot
    updater = ext.Updater(token=token)
    dispatcher = updater.dispatcher

    for handler in (start_handler, set_meeting_handler, get_meeting_handler, clear_meetings_handler):
        dispatcher.add_handler(handler)

    updater.start_polling()


if __name__ == "__main__":
    main()