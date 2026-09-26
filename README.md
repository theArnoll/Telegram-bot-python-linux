# Telegram-bot-python-linux

A telegram bot program run on a linux computer made with python-telegram-bot to see whether Telegram bot is only easy to develop only on Arduino core.

This project is currently focus on WoL (Wake on Lan).

[The Telegram bot solution I chose](https://python-telegram-bot.org/)  

As for why don't I use C++ since I'm mostly prefer developing with C++, that's because the C++ Telegram bot developing method I know so far is too complicated and costed too much time to develop, and I don't have that much time currently, so I choose to use a simpler method instead.

## Functions

| Command  | Description |
| -------- | ----------- |
| `/hello` | Manually having a welcome message.<br>It's different from the automatic startup message tho so it's not really a duplicated function, maybe. |
| `/ping`  | Reply "Pong!". To confirm whether the bot is still online.|
| `/wake`  | Wake the computer / device you've setup to do wake on lan. |
| `/restartBot` | Restart the bot. |

### Todos

- [ ] `/server <functions>` (Alias: `/svr`, `/srv`)
  - [ ] `/server reboot` Reboot the server with confirmation message. Confirm and replying `Yes` etc. is required
  - [ ] `/server shutdown` Shutdown the server with confirmation message. Confirm and replying `Yes` etc. is required
  - [ ] `/server status` Show the status of the server, including:
    - CPU usage % and temperature
    - RAM usage GB + MB, %, free ram GB + MB, %, total RAM GB float, GB + MB
    - Up time
  - [ ] Being not `@restricted` **ONLY FOR `/server status`**, but only show the rough status like
    - Low usage, but it's not always like that, so you should leave.
    - High CPU usage, so it won't be able to accept your request. You should better leave.
    - High RAM usage, so it's not having enough capacity to accept your request. You should leave.
    - High usage on EVERYTHING, so you need to leave.
- [ ] `/calc <expression>` Calculator. Using the safer `eval` to handle it
- [ ] `/random <choice>`
  - [ ] `/random dice` Random number between 1 and 6. Also the default value if not giving any arguments
  - [ ] `/random yn` Randomly choose between Yes and No
  - [ ] `/random <int> <int>` Randomly choose between equals two numbers

## Setup

In Linux, clone this repo, `cd` to the location you cloned to, then run these:

``` shell
python3 -m venv tgbot
source ./tgbot/bin/activate
pip install python-telegram-bot --upgrade
pip install python-dotenv wakeonlan
mv ./.env.template ./.env
chmod +x ./autorunSetup.sh && ./autorunSetup.sh
```

Add a ".env" file at the root folder of the repo, and add the following content to it:

```
botToken=[Your Telegram bot token generated from @BotFather on Telegram]
userID=[[Your User ID]]
WoLIP=[The IP address of the computer that's going to wake on lan. Need to make it end with 255.]
WoLmac=[Your MAC address of the computer you want to wake on lan. Need to replace ':' with '-']
```

For example:

```
botToken=1234567890:ABC-DEF1234ghIkl-zyxw
userID=[1234567890]
WoLIP=12.34.56.255
WoLmac=00-11-22-33-44-55
```

If you have multiple users to allow, you can add multiple user IDs

```
botToken=1234567890:ABC-DEF1234ghIkl-zyxw
userID=[1234567890, 9876543210]
WoLIP=192.168.0.255
WoLmac=00-11-DE-AD-BE-EF
```

There are already `.env.template` file given in the repo. If the setup command is fully executed, the file should be renamed to `.env`.

## AI Usage

Gemini Flash 3.8 + High thinking level on Google AI Studio with paid API key is used to solving some problem and generate `autorunSetup.sh`.

! `autorunSetup.sh` isn't tested at all !  
Although it doesn't seem to be having any problem, but still kinda need to say "use it on your own risk", while I don't think there are any risk that's gonna happen other than not successfully creating autorun service.

## Tested in:

- Intel N100 mini PC **`Currently running`**  
  Spec:
  - Intel N100
  - 8GB DDR5
  - 120GB 2.5" SSD (connected via USB)
  - Ubuntu Server 24.04 LTS
  - Yes, the one mentioned on my [serverboxDCutil](https://github.com/theArnoll/serverboxDCutil) repo