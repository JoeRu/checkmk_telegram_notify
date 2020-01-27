# checkmk_telegram_notify
The original this was found under [1](https://metzlog.srcbox.net/2016/01/monitoring-notifications-via-telegram/)
and  [2](https://www.tutonaut.de/checkmk-notifications-per-telegram-empfangen/) but wasn't working any longer - since some changes in API and urllib-libraries.

Adapted to use with python3 and python-telegram-bot.

## quickstart
Register a Telegram-Bot (Please use a search-engine for how this is done).
Open a conversation with your bot and aquire a _chat-id_.

Required Informations to change within telegram.py:
```
telegram_bot_token = '0123456789:myHash....'
telegram_chatid = '123456789'
```

Change these lines to match to your bot and chat.

As this make use of [Python Telegram Bot](https://python-telegram-bot.org/) install the requirements:
Weather as root or under the sites user.
```pip install python-telegram-bot```

su into your sites User;
Download telegram.py to your OMD-Site under
```
cd local/share/check_mk/notifications
chmod a+x telegram.py
```
- **important** to make it **executable** - otherwise it will not be found by checkmk otherwise the script will not show in Notifications. 

If you don't want to see ```telegram.py``` as a name in CheckMK-Notifications rename it the way you like it.

### Ressources:
* https://checkmk.de/cms_notifications.html
* https://www.tutonaut.de/checkmk-notifications-per-telegram-empfangen/
* https://metzlog.srcbox.net/2016/01/monitoring-notifications-via-telegram/

### Other Notfiy-Programms
if you like to use Signal - rather than telegram have a look here
[Signal Notify](https://morph027.gitlab.io/signal-web-gateway/usage/examples/check-mk/)
