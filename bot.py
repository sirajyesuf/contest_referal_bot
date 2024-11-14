from telegram.ext import Updater
from telegram import Update
import config
import logging



# Enable logging
log_format = logging.Formatter(
    "%(asctime)s - [%(name)s] [%(levelname)s]  %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_logger = logging.FileHandler("contest_bot.log")
file_logger.setFormatter(log_format)
file_logger.setLevel(logging.INFO)
logger.addHandler(file_logger)

console_logger = logging.StreamHandler()
console_logger.setFormatter(log_format)
console_logger.setLevel(logging.INFO)
logger.addHandler(console_logger)
from campaign import update_status_campaign, delete_stop_discard_award_campaign_handler
from admin import new_contest_conv_handler, admin_command_handler, campaign_btn_handler, get_list_invited_member_command_handler
from start import start_command_handler
from participants import participant_registration_conv_handler, participant_main_menu_handler
from invitation import members_membership_status_handler


def error_handler(update, context):
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=config.BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    #scheduler
    dispatcher.job_queue.run_repeating(callback=update_status_campaign,
                                       interval=30)
    # # bot handlers
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(new_contest_conv_handler)
    dispatcher.add_handler(participant_registration_conv_handler)
    dispatcher.add_handler(admin_command_handler)
    dispatcher.add_handler(campaign_btn_handler)
    dispatcher.add_handler(participant_main_menu_handler)
    dispatcher.add_handler(members_membership_status_handler)
    dispatcher.add_handler(delete_stop_discard_award_campaign_handler)
    dispatcher.add_handler(get_list_invited_member_command_handler)

    # dispatcher.add_handler(allmessage_handler)

    # error handler
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    updater.start_polling(allowed_updates=Update.ALL_TYPES)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
