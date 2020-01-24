#!/usr/bin/python
# Telegram

# Copyright Mathias Kettner  2013  mk@mathias-kettner.de
#           Stefan Gehn      2016  stefan+cmk@srcxbox.net
# adaption  Johannes Rumpf   2020  johannes.rumpf+telegram+ 
# added https://python-telegram-bot.org/ rather than urllib;
#
# install prerequisits  pip install python-telegram-bot
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.
# 
# Git: https://github.com/JoeRu/checkmk_telegram_notify

import os, re, sys, requests
import telegram
from telegram.error import NetworkError, Unauthorized

update_id = None

### CHANGE THESE ###
telegram_bot_token = '0123456789:myHash....'
telegram_chatid = '123456789'

####################

tmpl_host_text = """*Check_MK: $HOSTNAME$ - $EVENT_TXT$*
```
Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
Event:    $EVENT_TXT$
Output:   $HOSTOUTPUT$

$LONGHOSTOUTPUT$```"""

tmpl_service_text = """*Check_MK: $HOSTNAME$/$SERVICEDESC$ $EVENT_TXT$*
```
Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
Service:  $SERVICEDESC$
Event:    $EVENT_TXT$
Output:   $SERVICEOUTPUT$

$LONGSERVICEOUTPUT$```"""

def substitute_context(template, context):
    # First replace all known variables
    for varname, value in context.items():
        template = template.replace('$'+varname+'$', value)

    # Remove the rest of the variables and make them empty
    template = re.sub("\$[A-Z_][A-Z_0-9]*\$", "", template)
    return template
# better markdown formating @Todo:
def construct_message_text(context):
    notification_type = context["NOTIFICATIONTYPE"]
    if notification_type in [ "PROBLEM", "RECOVERY" ]:
        txt_info = "$PREVIOUS@HARDSHORTSTATE$ -> $@SHORTSTATE$"
    elif notification_type.startswith("FLAP"):
        if "START" in notification_type:
            txt_info = "Started Flapping"
        else:
            txt_info = "Stopped Flapping ($@SHORTSTATE$)"
    elif notification_type.startswith("DOWNTIME"):
        what = notification_type[8:].title()
        txt_info = "Downtime " + what + " ($@SHORTSTATE$)"
    elif notification_type == "ACKNOWLEDGEMENT":
        txt_info = "Acknowledged ($@SHORTSTATE$)"
    elif notification_type == "CUSTOM":
        txt_info = "Custom Notification ($@SHORTSTATE$)"
    else:
        txt_info = notification_type # Should neven happen

    txt_info = substitute_context(txt_info.replace("@", context["WHAT"]), context)

    context["EVENT_TXT"] = txt_info

    if context['WHAT'] == 'HOST':
        tmpl_text = tmpl_host_text
    else:
        tmpl_text = tmpl_service_text

    return substitute_context(tmpl_text, context)

def fetch_notification_context():
    context = {}
    for (var, value) in os.environ.items():
        if var.startswith("NOTIFY_"):
            context[var[7:]] = value
    return context

def send_telegram_message(bot, chat_id, my_text):
	bot.send_message(chat_id=chat_id, 
                 text=my_text, 
                 parse_mode=telegram.ParseMode.MARKDOWN)	



def main():
	"""Run the bot."""
	global update_id
    # Telegram Bot Authorization Token
	bot = telegram.Bot(telegram_bot_token)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None
        
	context = fetch_notification_context()
	#telegram_chatid = '123456789' #context.get('CONTACT_TELEGRAM_CHAT_ID') " Your Chat-ID - @idea: Register and deregister with bot somehow
    
	if not telegram_chatid: # e.g. empty field in user database
		sys.stdout.write("Cannot send Telegram message: Empty destination chat id")
		sys.exit(2)
        
	text = construct_message_text(context)
    
	send_telegram_message(bot, telegram_chatid, text)

main()



