#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A library that provides functionality to the @RandomUtils_bot
# Copyright (C) 2017-2018
# Javier Gines Sanchez <software@javisite.com>
#


import logging																## System module
import os
if not os.path.exists(os.path.dirname(__file__) + os.sep+'.logs' + os.sep):
		os.makedirs(os.path.dirname(__file__) + os.sep+'.logs' + os.sep)
logFile= os.path.dirname(__file__) + os.sep+'.logs' + os.sep+ 'logCoreBot.log'
try:
	logging.basicConfig(
	filename=logFile,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
	)
except Exception as e:
	print("Se ha generado la siguiente excepción:\n\n"+str(e)+"\n\nCorrijala para ejecutar el programa.")
	os._exit(1)

logging.info(('-'*30)+' Bot Starting '+('-'*30))

from sys import argv										## System module
from subprocess import call									## System module
from time import sleep														## System module
# Usefull for /restartB
if(len(argv)>1):
	sleep(2)
	call("kill -9 " + str(argv[1]), shell=True)
	logging.info('Bot restarting complete.')
	sleep(2)


from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters

import Functions.basicData as bd
import Commands.basicCommands as bc
import Commands.randomCommands as rc
import Commands.utilsCommands as uc

import Commands.inlineCommands as iq


try:
	token_file = open("token.txt", 'r')
except Exception as e:
	logging.error("Exception Handler:"+str(e))
	os._exit(1)

updater = Updater(token_file.read().splitlines()[0], workers=200)
token_file.close()
dispatcher = updater.dispatcher
dispatcher.add_error_handler(bd.basicErrorTelegramHandler)


# Initialize "Command" handlers
# Basic Commands
start_handler = CommandHandler(list(['start','help']), bc.start, pass_args=False, allow_edited=True)
dispatcher.add_handler(start_handler)
restart_handler = CommandHandler(list(['restartP','rebootP']), bc.restartP, pass_args=False, allow_edited=True)
dispatcher.add_handler(restart_handler)
stop_handler = CommandHandler('stopP', bc.stopP, pass_args=False, allow_edited=True)
dispatcher.add_handler(stop_handler)
leave_handler = CommandHandler('leave', bc.leaveGroup, pass_args=False, allow_edited=True)
dispatcher.add_handler(leave_handler)
changelog_handler = CommandHandler('changelog', bc.changelog, pass_args=False, allow_edited=True)
dispatcher.add_handler(changelog_handler)
contact_handler = CommandHandler('contact', bc.contact, pass_args=True, allow_edited=True)
dispatcher.add_handler(contact_handler)
logging.info('Basic commands loaded correctly.')

# Utils Commands
update_handler = CommandHandler('updateP', uc.updateP, pass_args=False, allow_edited=True)
dispatcher.add_handler(update_handler)
speak_handler = CommandHandler('speakP', uc.speakP, pass_args=True, allow_edited=True)
dispatcher.add_handler(speak_handler)
download_handler = CommandHandler('downloadP', uc.downloadP, pass_args=True, allow_edited=True)
dispatcher.add_handler(download_handler)
getlog_handler = CommandHandler('getLogP', uc.getLogP, allow_edited=True)
dispatcher.add_handler(getlog_handler)
clearLog_handler = CommandHandler('clearlogP', uc.clearLogP, allow_edited=True)
dispatcher.add_handler(clearLog_handler)
logging.info('Utils commands loaded correctly.')


# Random Commands
flip_handler = CommandHandler('flip', rc.flip, pass_args=False, allow_edited=True)
dispatcher.add_handler(flip_handler)
randomNumber_handler = CommandHandler('random', rc.randomNumber, pass_args=True, allow_edited=True)
dispatcher.add_handler(randomNumber_handler)
shortLink_handler = CommandHandler('shortLink', rc.shortLink, pass_args=True, allow_edited=True)
dispatcher.add_handler(shortLink_handler)
remindMe_handler = CommandHandler('remindMe', rc.remindMe, pass_args=False, allow_edited=True)
dispatcher.add_handler(remindMe_handler)
stopwatch_handler = CommandHandler('stopwatch', rc.stopwatch, pass_args=False, allow_edited=True)
dispatcher.add_handler(stopwatch_handler)
countdown_handler = CommandHandler('countdown', rc.countdown, pass_args=True, allow_edited=False)
dispatcher.add_handler(countdown_handler)
newVote_handler = CommandHandler('newVote', rc.newVote, pass_args=False, allow_edited=True)
dispatcher.add_handler(newVote_handler)
secretMessage_handler = CommandHandler('secretMessage', rc.secretMessage, pass_args=False, allow_edited=True)
dispatcher.add_handler(secretMessage_handler)
anonymousMessage_handler = CommandHandler('anonymousMessage', rc.anonymousMessage, pass_args=False, allow_edited=True)
dispatcher.add_handler(anonymousMessage_handler)

case_handler = CommandHandler('case', rc.case, pass_args=False, allow_edited=True)
dispatcher.add_handler(case_handler)
imgur_handler = CommandHandler('imgur', rc.imgur, pass_args=False, allow_edited=True)
dispatcher.add_handler(imgur_handler)
note_handler = CommandHandler('note', rc.note, pass_args=False, allow_edited=True)
dispatcher.add_handler(note_handler)
logging.info('Random commands loaded correctly.')


# Forward Messages
forwardMessages_handler = MessageHandler(Filters.forwarded, rc.forwardMessage)
dispatcher.add_handler(forwardMessages_handler)


# Random Inline
dispatcher.add_handler(InlineQueryHandler(iq.inlinequery))

updater.start_polling(poll_interval = 1.0, timeout=20, read_latency=5, clean=True)
logging.info('MainBot Completly Loaded.')
logging.info('Bot Working.')
updater.bot.sendMessage(chat_id=bd.chatIDDeveloper, text="Bot Iniciado", disable_notification=True)

updater.idle()
