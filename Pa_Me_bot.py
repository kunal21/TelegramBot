from telegram.ext import (Updater,CommandHandler,MessageHandler,Filters,CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,text="Welcome to the news BOT\nEnter '/help' for more information about the BOT'")
    

def stocks(bot,update,args):
	url = ' '.join(args)
	htmltext = urllib.request.urlopen("https://in.finance.yahoo.com/q?s="+url)
	soup = BeautifulSoup(htmltext)
	for stock in soup.find_all('span',{'id':"yfs_l84_"+(url).lower()}):
		stock_list = (stock.getText())
		bot.sendMessage(chat_id=update.message.chat_id,text="Latest stock price of "+url+" is "+stock_list)		
	
def helps(bot,update):
	bot.sendMessage(chat_id=update.message.chat_id,text="Enter '/stocks symbol' to know the latest stock prices.\nEnter '/news website_categroy' for quick review of the news.\nEnter '/temp cityname' to know the current temperature.")


	
def news(bot,update,args):
	string = ' '.join(args)
	replaced_url = (string.replace('_',' ')).split(' ')
	if replaced_url[0] == 'espn' and replaced_url[1] == 'cricket':
		url = "https://www."+replaced_url[0]+".in/"+replaced_url[1]
		htmltext = urllib.request.urlopen(url)
		soup = BeautifulSoup(htmltext)
		for news in soup.find_all('p',{"class":"contentItem__subhead contentItem__subhead--story"}):
			news_reader = news.getText()
			bot.sendMessage(chat_id=update.message.chat_id,text=news_reader)
	elif replaced_url[0] == 'espn' and replaced_url[1] == 'football':
		url = "https://www."+replaced_url[0]+".in/"+replaced_url[1]
		htmltext = urllib.request.urlopen(url)
		soup = BeautifulSoup(htmltext)
		for news in soup.find_all('p',{"class":"contentItem__subhead contentItem__subhead--story"}):
			news_reader = news.getText()
			bot.sendMessage(chat_id=update.message.chat_id,text=news_reader)
	elif replaced_url[0] == 'cricbuzz':
		url = "https://www."+replaced_url[0]+".com"
		htmltext = urllib.request.urlopen(url)
		soup = BeautifulSoup(htmltext)
		for news in soup.find_all('div',{"class":"cb-nws-intr"}):
			news_reader = news.getText()
			bot.sendMessage(chat_id=update.message.chat_id,text=news_reader)
		
def temp(bot,update,args):
	query = ''.join(args)
	url = "http://forecast.infoweather.today/?option=weather&net="+query
	htmltext = urllib.request.urlopen(url)
	soup = BeautifulSoup(htmltext)
	for temper in soup.find_all('div',{"class":"temperature celsius-degree"}):
		print("hello")
		current_temp = temper.extract()
		bot.sendMessage(chat_id=update.message.chat_id,text="Temperature of "+query+" is "+current_temp)
		


updater = Updater(token="297569448:AAHvzah64XrIb6qSnhdSvgOahLLijaExm-0")
dispatcher = updater.dispatcher

stocks_handler = CommandHandler('stocks', stocks, pass_args=True)
start_handler = CommandHandler('start',start)
help_handler = CommandHandler('help',helps)
news_handler = CommandHandler('news',news,pass_args=True)
temperature_handler = CommandHandler('temp',temp,pass_args=True)



dispatcher.add_handler(start_handler)
#dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(stocks_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(news_handler)
dispatcher.add_handler(temperature_handler)



updater.start_polling()
updater.idle()