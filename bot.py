"""
The main entry for the bot, here you can implement your
mehtods as commands, by matching the messages content.
"""

import logging
import whatsapp


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="bot.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

bot = whatsapp.Bot()

# Set the chat name for the Bot
# You can set it manulay with mouse
bot.set_chat(chat_name="Ammar Alfaifi")


# match the command with its methods to invoke
# the first parameter will be the last message
COMMANDS = {
    "/start": bot.send_message,
    "/media": bot.send_media,
    "gpt": bot.ask_gpt,
    "chat": bot.ask_chat_gpt,
    "dalle": bot.ask_DALL_E,
}


def handle(msg: str):
    """Place here your comands to hadle them
    the vraible `msg` is the last read comming message
    it gets called every 1s"""

    if msg:

        if msg == "/start":
            bot.send_message("Hello!")

        elif msg == "/media":
            bot.send_media("/path/to/imagem.jpg")

        elif msg.startswith("gpt"):
            bot.ask_gpt(msg.replace("/gpt\n", ""), 500)

        elif msg.startswith("chat"):
            bot.ask_chat_gpt(msg.replace("chat\n", ""))

        elif msg.startswith("dalle"):
            bot.ask_DALL_E(msg.replace("dalle\n", ""))


# start looping forever
bot.loop(handle)
