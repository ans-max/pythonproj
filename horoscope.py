#!/usr/bin/env python3
#Webscraping
#pulls the horroscope

import urllib.request, urllib.error, urllib.parse
import re, argparse,datetime
from bs4 import BeautifulSoup as soup
from datetime import datetime, timedelta

def Download_Page(url, user_agent='fatso', num_retries=2):
	#print 	url
	headers = {'User-agent':user_agent}
	request = urllib.request.Request(url, headers=headers)
	try:
		#print 'Downloading:',url
		html = urllib.request.urlopen(request).read()

	except urllib.error.URLError as e:
		#print "Sorry No horoscope, Kindly check the details provided:", e.reason
		html = None
		if num_retries > 0:
			if hasattr(e,'code') and 500 <= e.code < 600:
				#retry 5xx http errors
				return download(url, user_agent, num_retries - 1)
	return html

def from_Horoscope_com(time = "today", sign = "aquarius"):
	'''Pull horoscope from horoscope.com'''
	sign_dict = {"aries":"1","taurus":"2","gemini":"3","cancer":"4",
	"leo":"5","virgo":"6","libra":"7","scorpio":"8",
	"sagittarius":"9","capricorn":"10","aquarius":"11","pisces":"12"}

	base_url = "https://www.horoscope.com/us/horoscopes/general/"
	if time == 'today':
		fetch_url = base_url + "horoscope-general-daily-today.aspx?sign="+ sign_dict[sign]
	elif time == 'yesterday':
		fetch_url = base_url + "horoscope-general-daily-yesterday.aspx?sign="+ sign_dict[sign]
	else:
		fetch_url = base_url + "horoscope-general-daily-tomorrow.aspx?sign="+ sign_dict[sign]
	htm = Download_Page(fetch_url)
	if htm != None:
		data = soup(htm, 'lxml')
		tr = data.find("div",{"class":"main-horoscope"}).find("p")
		return tr
	else:
		return 0

def from_Astrology_com(time = "today", sign = "aquarius"):
	''' Pull horoscope from astrology.com'''
	base_url = 'https://www.astrology.com/horoscope/daily'
	fetch_url = base_url+ '/' + time + '/' + str(sign) + '.html'
	htm = Download_Page(fetch_url)
	if htm != None:
		data = soup(htm, 'lxml')
		tr = data.find("div", {"class":"grid grid-right-sidebar primis-rr"}).find("p")
		return tr
	else:
		return 0

def from_GaneshaSpeaks(time = "today", sign = "aquarius"):
	''' Pull horoscope from ganeshaspeaks.com'''
	base_url = "https://www.ganeshaspeaks.com/horoscopes/"
	if time == 'today':
		fetch_url = base_url + "daily-horoscope/" + sign + "/"
	elif time == 'yesterday':
		fetch_url = base_url + "yesterday-horoscope/" + sign + "/"
	else:
		fetch_url = base_url + "tomorrow-horoscope/" + sign + "/"
	htm = Download_Page(fetch_url)
	if htm != None:
		data = soup(htm, 'lxml')
		tr = data.find("div",{"class":"row card-padding-20 container-fluid-xs margin-bottom-xs-0"}).find("p",{"class":"margin-top-xs-0"})
		return tr
	else:
		return 0
def cal_date(day):
	now = datetime.now()
	if day == "tomorrow":
		return now + timedelta(days = 1)
	elif day == "yesterday":
		return now - timedelta(days = 1)
	else:
		return now


def main():
	'Main function to call the other functions'
	parser = argparse.ArgumentParser(description='Display the daily horoscope based on time and sign')
	parser.add_argument('-s', '--sign', help='enter the full sun sign', default='aquarius')
	parser.add_argument('-d', '--day', help='enter yesterday,today or tommorrow', default='today')
	args = parser.parse_args()
	#passing the args to horroscope calling functions
	prophecy_date = cal_date(args.day)
	bejan_info = from_GaneshaSpeaks(args.day, args.sign)
	astro_info = from_Astrology_com(args.day, args.sign)
	horo_info = from_Horoscope_com(args.day, args.sign)

	if bejan_info == 0 or astro_info == 0:
		print("Sorry No horoscope, Kindly check the details provided: %(day)s , %(sign)s" %{'day':args.day, 'sign':args.sign})
	else:
		print("\n{}:\n".format(str(args.sign).capitalize()))
		print(prophecy_date.strftime("%b, %d %Y:\n"))
		print("#From ganeshaspeaks.com for {}\n".format(args.sign))
		print(bejan_info.text.strip(), '\n')
		print("#From astrology.com for {}\n".format(args.sign))
		print(astro_info.text.split(":")[1].strip(), '\n')
		print("#From horoscope.com for {}\n".format(args.sign))
		print(horo_info.text.split("-")[1].strip(), '\n')

if __name__ == '__main__':
	main()
