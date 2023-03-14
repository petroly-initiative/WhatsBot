"""
The main entry for the bot, here you can implement your
mehtods as commands, by matching the messages content.
"""

import logging
import whatsapp

CHAT_NAME = "Petroly Bot"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s in %(filename)s `%(funcName)s` - %(message)s",
)
logger = logging.getLogger(__name__)

bot = whatsapp.Bot()

# Set the chat name for the Bot
# You can set it manulay with mouse
bot.set_chat(CHAT_NAME)


# match the command with its methods to invoke
# the first parameter will be the last message
COMMANDS = {
    "/start": bot.send_message,
    "/media": bot.send_media,
    "gpt": bot.ask_gpt,
    "chat": bot.ask_chat_gpt,
    "dalle": bot.ask_DALL_E,
    "kickout": bot.remove_participant,
    "delete": bot.delete_message,
}

read_done = []


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
            print(msg)
            bot.ask_gpt(msg.replace("/gpt", "").strip(), 500)

        elif msg.startswith("chatgpt"):
            print(msg)
            bot.ask_chat_gpt(msg.replace("chatgpt", "").strip(), new_thread=True)

        elif msg.startswith("chat"):
            print(msg)
            bot.ask_chat_gpt(msg.replace("chat", "").strip())

        elif msg.startswith("dalle"):
            print(msg)
            bot.ask_DALL_E(msg.replace("dalle", "").strip())

        elif msg == "delete" and bot.is_sender_me:
            if bot.msg_element.text not in read_done:
                read_done.append(bot.msg_element.text)
                msg_el = bot.go_to_replied_message(bot.msg_element)
                bot.delete_message(msg_el)

        elif msg == "kickout" and bot.is_sender_me:
            if bot.msg_element.text not in read_done:
                read_done.append(bot.msg_element.text)
                msg_el = bot.go_to_replied_message(bot.msg_element)
                bot.remove_participant(bot.get_contact(msg_el))


# start looping forever
bot.loop(handle)
