# WhatsBot


## Preview
It a simple web-based WhatsApp bot. It requires starting up a webdriver to control the session.
It also support OpenAI API, just put your token and you can ask `ChatGPT`, `GPT-3`, `DALL.E`, 
or any other model.


## installation
- Latest version of Python, at least `3.10`
- Clone this repo as

``` shell
git clone <REPO>
```
and change the working director to it,

``` shell
cd WhatsBot
```

- Run 

``` shell
pip install openai selenium
```


----
### Settings

- Set the variable `CHAT_NAME`, it'll be used to find the chat you want the bot to interact in.
- To use commands of OpenAI you should export the env variable as

``` shell
export OPENAI_TOKE=right_here_your_token
```

----
### Dowload ChromeDriver

- Open ```https://chromedriver.chromium.org/downloads``` and download the file according to your version of chrome.
- Place the `chromedriver` in `PATH` env variable,

### starting the bot
Now it's as simple as running 

``` shell
python bot.py
```

A chrome browser will pop up, wait for the QR to scan, then wait for downloading chats.
After 5s it'll start search for the chat as in the variable `CHAT_NAME` then enters it.

----
## Commands
By default there are four commands, the simplest one is
suitable for testing: `/start`, bot returns "Hello!".

You can add as many as you want of commands in the dict variable `COMMANDS`, in the format
of `"command": THE_METHOD_TO_EXECuTE`


## Sharing is caring, don't hesitate to sponsor us <3.
