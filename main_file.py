"""
Name   : MultiChannel Poster
Author : Gauthamram Ravichandran

If you need anyother bot, ping me in telegram @Ys0Seri0us (That's two zer0s, not O's)
or by mail : 20rgr12@gmail.com
"""
# ---- MODULE IMPORTS ---- #
from telegram.ext import Defaults
from telegram import ParseMode
from telegram.ext import Updater, messagequeue as mq
from telegram.utils.request import Request
import pytz
from sys import exc_info
from logging import ERROR, basicConfig, getLogger, INFO, DEBUG
# ---- CUSTOM IMPORTS ---- #
from common.common_stuffs import MQBot
from const.CONFIG import TG

from handlers import Handlers

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=ERROR,
            filename = f'logs.log')

logger = getLogger()


def register_err( update, context ) :
	type, value, traceback = exc_info()
	for admin in TG.ADMINS:
			if traceback:
				context.bot.send_message(chat_id = admin,
				                         text = f"""
			ERROR : {context.error}
			FILE : {traceback.tb_frame.f_locals.get('__file__', "unknown")}
			LINE : {traceback.tb_lineno}
			USERID : {update.effective_user.id}
			USERNAME : {update.effective_user.username or update.effective_user.first_name}
			INPUT TXT : {update.effective_message.text}
			CALLBACK DATA : {update.callback_query}
			""")
			else:
				context.bot.send_message(chat_id = admin,
				                         text = f"""ERROR : {context.error}""")


hndlrs_to_add = [Handlers.add_channel, Handlers.rm_chnl, Handlers.add_group, Handlers.get_group,
                 Handlers.list_group, Handlers.remove_group, Handlers.start, Handlers.broadcast]


def main():
	defaults = Defaults(parse_mode = ParseMode.HTML, disable_web_page_preview = True,
	                    tzinfo = pytz.timezone('Asia/Kolkata'))
	
	updater = Updater(bot = MQBot(token = TG.BOTTOKEN,
	                              request = Request(con_pool_size = 10),
	                              mqueue = mq.MessageQueue(all_burst_limit = 30,
	                                                       all_time_limit_ms = 1000),
	                              defaults = defaults),
	                  use_context = True)  # , persistence = my_persistence)
	# job_queue = updater.job_queue
	d = updater.dispatcher
	for hndlr in hndlrs_to_add:
		d.add_handler(hndlr)
	d.add_error_handler(register_err)
	
	if TG.PORT_NUM != 0:
		updater.start_webhook(listen = '127.0.0.1',
		                      port = TG.PORT_NUM,
		                      url_path = f"{TG.BOTTOKEN.replace(':', '')}")
		updater.bot.set_webhook(url = f"https://{TG.IP_ADDR}:443/{TG.BOTTOKEN.replace(':', '')}",
		                        certificate = open('cert.pem', 'rb'))
	else:
		updater.start_polling()
		updater.idle()


if __name__ == "__main__":
	main()
