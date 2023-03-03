"""
Here the core of the Bot,
all the mehtods to handle commands.
"""


import logging
import os
from time import sleep

import openai
import openai.error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


os.system("rm -rf profile")  # REMOVE OLD PROFILE

logger = logging.getLogger(__name__)
OPENAI_TOKEN = os.environ.get("OPENAI_TOKEN", None)
DRIVER_PATH = "chromedriver"
WHATSAPP_WEB = "https://web.whatsapp.com/"

# You shouldn't need to change this
CLASSES = {
    "msg_text": "_21Ahp",
    "msg_box": "fd365im1",
    "send_button": "epia9gcq",
    "search_box": "Er7QU",
    "loading": "_2dfCc",
}

XPATH = {
    "left_msg": "span.selectable-text",
    "media_button": "span[data-icon='clip']",
    "media_input": "input[type='file']",
    "send_button": "//div[contains(@class, 'iA40b')]",
}


class Bot:
    """The bot implementaion
    this class creates the webdriver and manages it.
    It establishes connection with OpenAI API.
    """

    dir_path = os.getcwd()
    chromedriver = DRIVER_PATH
    profile = os.path.join(dir_path, "profile", "wpp")

    def __init__(self):
        if OPENAI_TOKEN:
            openai.api_key = OPENAI_TOKEN
            self.conversations = []
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir={}".format(self.profile))
        # start webdriver
        self.driver = webdriver.Chrome(self.chromedriver, chrome_options=self.options)
        self.driver.get(WHATSAPP_WEB)
        self.driver.implicitly_wait(5)

    def get_last_message(self):
        try:
            # get the last message
            messages = self.driver.find_elements_by_class_name(CLASSES["msg_text"])
            self.msg_element = messages[-1].find_element_by_css_selector(
                XPATH["left_msg"]
            )

            return self.msg_element.text

        except Exception as e:
            logger.error(f"Error getting message: {e}")

    def reply(self, message):
        try:
            # hover
            ActionChains(self.driver).move_to_element(self.msg_element).perform()
            try:
                # click options
                self.driver.find_element_by_class_name("_2T2Kt").click()
            except NoSuchElementException:
                self.driver.find_element_by_class_name("_3Gzl9").click()

            sleep(0.5)
            # choose reply
            for choice in self.driver.find_elements_by_class_name("_1MZM5"):
                if choice.text == "Reply":
                    choice.click()
                    sleep(0.1)
                    break

            self.send_message(message)
        except Exception as e:
            logger.error(f"Erorr: in `reply`: {e}")

    def send_message(self, msg):
        try:
            sleep(1)
            # select box message and typing
            self.msg_box_element = self.driver.find_element_by_class_name(
                CLASSES["msg_box"]
            )
            for part in msg.split("\n"):
                self.msg_box_element.send_keys(part)
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(
                    Keys.ENTER
                ).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            sleep(0.5)
            # Select send button
            self.send_btn_element = self.driver.find_element_by_class_name(
                CLASSES["send_button"]
            )
            # click
            self.send_btn_element.click()
            sleep(0.5)
        except Exception as e:
            logger.error("Error send message", e)

    def send_media(self, file):
        try:
            self.driver.find_element_by_css_selector(XPATH["media_button"]).click()
            attach = self.driver.find_element_by_css_selector(XPATH["media_input"])
            attach.send_keys(fileToSend)
            sleep(3)
            send = self.driver.find_element_by_xpath(XPATH["send_button"])
            send.click()
        except Exception as e:
            print("Error send media", e)

    def is_ready(self):
        """By checking if the seach box is availble
        we know it's ready to chat"""

        return bool(self.driver.find_elements_by_class_name(CLASSES["search_box"]))

    def set_chat(self, chat_name):
        """Open specific chat"""

        while not self.is_ready():
            sleep(1)

        sleep(5)
        try:
            self.search_chat_element = self.driver.find_element_by_class_name(
                CLASSES["search_box"]
            )  #
            self.search_chat_element.send_keys(chat_name)
            sleep(2)
            self.chat_element = self.driver.find_element_by_xpath(
                f"//span[contains(@title, '{chat_name}')]"
            )
            self.chat_element.click()
            self.search_chat_element.clear()
        except Exception as e:
            raise e

    def ask_gpt(self, msg, max_tokens=50):

        logger.info(f"Prompe: {msg}")
        if not OPENAI_TOKEN:
            print("Make sure you setup OpenAI token.")

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=msg,
                temperature=0.3,
                max_tokens=max_tokens,
            )

        except openai.InvalidRequestError as e:
            logger.error(e)
            self.reply(e)
            return

        except openai.APIError as e:
            logger.error(e)
            self.send_message("APIConnectionError, try again latter")
            return

        except openai.OpenAIError as e:
            logger.error(e)
            self.reply("A fatal error ocurred")
            return

        text = response.to_dict()["choices"][0].to_dict()["text"]
        self.reply(f"GPT:{text}")

    def construct_conversation(self, prompt: str):
        """This is to help constructing
        the `messages` parameter for `ChstCompletion`
        so it can biuld an answer based on prevoius responses"""

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant for students of King Fahd University of Petroleum and Minerals (KFUPM).",
            },
        ]
        messages.extend(self.conversations)
        messages.append({"role": "user", "content": prompt})

        return messages

    def store_response(self, completion):
        """To store new responses as 'assistant'"""

        self.conversations.append(completion.choices[0]["message"].to_dict())

        # to prevent excceding the max tokens:
        # 4096 tokens for gpt-3.5-turbo-0301
        if completion.usage.total_tokens > 3000:
            self.conversations.pop(0)

    def ask_chat_gpt(self, msg):

        logger.info(f"Prompe: {msg}")
        if not OPENAI_TOKEN:
            print("Make sure you setup OpenAI token.")

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.construct_conversation(msg),
            )

        except openai.InvalidRequestError as e:
            logger.error(e)
            self.reply(e)
            return

        except openai.APIError as e:
            logger.error(e)
            self.send_message("APIConnectionError, try again latter")
            return

        except openai.OpenAIError as e:
            logger.error(e)
            self.reply("A fatal error ocurred")
            return

        self.store_response(completion)
        self.reply(f"Chat:\n{completion.choices[0].message.content}")

    def ask_DALL_E(self, msg):

        logger.info(f"Prompe: {msg}")
        try:
            response = openai.Image.create(prompt=msg, n=1, size="512x512")

        except openai.InvalidRequestError as e:
            logger.error(e)
            self.reply(e)
            return

        except openai.APIError as e:
            logger.error(e)
            self.send_message("APIConnectionError, try again latter")
            return

        except openai.OpenAIError as e:
            logger.error(e)
            self.reply("A fatal error ocurred")
            return

        image_url = response["data"][0]["url"]

        self.reply(image_url)

    def loop(self, handle):

        while True:
            if self.is_ready():
                msg = self.get_last_message()
                if msg:
                    handle(msg)

            sleep(1)
