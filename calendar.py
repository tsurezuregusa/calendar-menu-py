#!/usr/bin/env python3

# <bitbar.title>Calendar & Time</bitbar.title>
# <bitbar.version>0.1</bitbar.version>
# <bitbar.author.github>tsurezuregusa</bitbar.author.github>
# <bitbar.desc>Display calendar, world time and sun/moon information</bitbar.desc>
# <bitbar.dependencies>python3; pip: ephem</bitbar.dependencies>

# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

# <swiftbar.schedule>* * * * *</swiftbar.schedule>

import re
import math
from dateutil import tz
import datetime
import locale
import ephem

localoffset = datetime.timedelta(hours=9)
locale.setlocale(locale.LC_TIME, "ja_JP")

holidays = ['2021-01-01','2021-01-11','2021-02-11','2021-02-23','2021-03-20','2021-04-29','2021-05-03','2021-05-04','2021-05-05','2021-07-22','2021-07-23','2021-08-08','2021-09-20','2021-09-23','2021-11-03','2021-11-23']

places = [
	{
		'name': "Tokyo",
		'tz': "Asia/Tokyo",
		'lat': '35.664167',
		'lon': '139.698611',
		'home': True
	},
	{
		'name': "Paris",
		'tz': "Europe/Paris",
		'lat': '48.864716',
		'lon': '2.349014',
		'home': False
	},{
		'name': "Melbourne",
		'tz': "Australia/Melbourne",
		'lat': '-37.840935',
		'lon': '144.946457',
		'home': False
	}
]

now = datetime.datetime.now()
dymdt = (now-localoffset).strftime("%Y/%m/%d %H:%M:%S")
dymdty = (now-localoffset-datetime.timedelta(days=1)).strftime("%Y/%m/%d %H:%M:%S")
enow = ephem.Date(dymdt)

def hm(f):
	t = f * 24
	h = int(t)
	m = int((t % 1) * 60)
	s = str(h).zfill(2) + ":" + str(m).zfill(2)
	return s

def ms(f):
	t = f * 24 * 60
	m = int(t)
	s = int((t % 1) * 60)
	o = str(m) + "′" + str(s) + "″"
	if f > 0:
		return "+" + o
	else:
		return o

def degstr(rad):
	return str(int(round(math.degrees(float(rad)),0)))+"˚"

def calendar():
	w = int(now.strftime("%w")) - 7
	if w < 0:
		w += 7
	date = now - datetime.timedelta(days=w) - datetime.timedelta(days=6)
	dates = []
	for i in range(0,42,7):
		week = []
		for j in range (7):
			if date - now < datetime.timedelta(hours=24) and now - date < datetime.timedelta(hours=24):
				week.append(("*"+date.strftime("%-d")+"*").rjust(4))
			elif any(date.strftime("%Y-%m-%d") == d for d in holidays):
				week.append(("-"+date.strftime("%-d")+"-").rjust(4))
			else:
				week.append((" "+date.strftime("%-d")+" ").rjust(4))
			date += datetime.timedelta(days=1)
		dates.append(' '.join(week)+"|font=Menlo size=14 color=darkgray trim=false\n")
	if locale.getlocale(locale.LC_TIME)[0] == "ja_JP":
		days = ["  月      火      水      木      金      土      日|size=17 color=gray trim=false"]
	else:
		days = ["  ".join([datetime.date(2001, 1, i).strftime('%a') for i in range(1, 8)]) + "|font=Menlo color=gray"]
	calendar = days + dates
	return "\n".join(calendar)

print(now.strftime("%a %-d · %H:%M"))
print("---")
print(calendar())
print("---")

def riseblue(x):
	place.date = x
	sun.compute(place)
	return sun.alt - ephem.degrees('-8')

def risegold0(x):
	place.date = x
	sun.compute(place)
	return sun.alt - ephem.degrees('-6')

def risegold1(x):
	place.date = x
	sun.compute(place)
	return sun.alt - ephem.degrees('6')

def setblue(x):
	place.date = x + ephem.hour * 12
	sun.compute(place)
	return sun.alt - ephem.degrees('-8')

def setgold0(x):
	place.date = x + ephem.hour * 12
	sun.compute(place)
	return sun.alt - ephem.degrees('-6')

def setgold1(x):
	place.date = x + ephem.hour * 12
	sun.compute(place)
	return sun.alt - ephem.degrees('6')

for p in places:
	zone = tz.gettz(p['tz'])
	offset = zone.utcoffset(now)
	if offset < datetime.timedelta(hours=0):
		offtxt = "-" + str(datetime.timedelta(hours=0)-offset).split(":")[0]
	else:
		offtxt = "+" + str(offset).split(":")[0]
	# eoff = int(str(offset).split(":")[0]) * ephem.hour + int(str(offset).split(":")[1]) * ephem.minute
	local = offset - localoffset
	hour = int((now+local).strftime("%H"))
	
	midnight = (now - datetime.timedelta(hours=24) + offset).strftime("%Y/%m/%d 0:00")
	if p['home']:
		menu = ""
	else:
		menu = "--"
	
	place = ephem.Observer()
	place.lat = p['lat']
	place.lon = p['lon']
	place.elevation = 40
	place.horizon = '0'
	sun = ephem.Sun(place)
	moon = ephem.Moon(place)
	
	if sun.alt > 0:
		sunnow = ('%s %4s %s' % ((now+local).strftime("%d %H:%M"),degstr(sun.az),degstr(sun.alt)))
	else:
		sunnow = (now+local).strftime("%d %H:%M") + "    "
	moonaltnow = float(moon.alt)
	moonaznow = float(moon.az)
	
	moondays = enow - ephem.previous_new_moon(enow)
	illumination = moon.moon_phase*100
	
	phase = [
		{
			'p': '◯',
			'd': ephem.localtime(ephem.next_new_moon(dymdt))
		},
		{
			'p': '◑',
			'd': ephem.localtime(ephem.next_first_quarter_moon(dymdt))
		},
		{
			'p': '●',
			'd': ephem.localtime(ephem.next_full_moon(dymdt))
		},
		{
			'p': '◐',
			'd': ephem.localtime(ephem.next_last_quarter_moon(dymdt))
		}
	]
	phase += [
		{
			'p': '◯',
			'd': ephem.localtime(ephem.next_new_moon(phase[0]['d'].strftime("%Y/%m/%d %H:%M:%S")))
		},
		{
			'p': '◑',
			'd': ephem.localtime(ephem.next_first_quarter_moon(phase[1]['d'].strftime("%Y/%m/%d %H:%M:%S")))
		},
		{
			'p': '●',
			'd': ephem.localtime(ephem.next_full_moon(phase[2]['d'].strftime("%Y/%m/%d %H:%M:%S")))
		},
		{
			'p': '◐',
			'd': ephem.localtime(ephem.next_last_quarter_moon(phase[3]['d'].strftime("%Y/%m/%d %H:%M:%S")))
		}
	]
	phasesort = sorted(phase, key=lambda k: k['d'])[:5]
	
	if sun.alt > 0:
		sunrise = place.previous_rising(sun, start=dymdt)
		sunset = place.next_setting(sun, start=dymdt)
		yestsunrise = place.previous_rising(sun, start=dymdty)
		yestsunset = place.previous_setting(sun, start=dymdt)
		color = "goldenrod"
	else:
		if hour >= 12:
			sunrise = place.previous_rising(sun, start=dymdt)
			sunset = place.previous_setting(sun, start=dymdt)
			yestsunrise = place.previous_rising(sun, start=dymdty)
			yestsunset = place.previous_setting(sun, start=dymdty)
		else:
			sunrise = place.next_rising(sun, start=dymdt)
			sunset = place.next_setting(sun, start=dymdt)
			yestsunrise = place.previous_rising(sun, start=dymdt)
			yestsunset = place.previous_setting(sun, start=dymdt)
		color = "steelblue"
	
	noon = place.previous_transit(sun, start=dymdt)
	if enow - noon > ephem.hour * 24:
		noon = place.next_transit(sun, start=dymdt)
	
	moonrise = place.previous_rising(moon, start=dymdt)
	if enow - moonrise > ephem.hour * 24:
		moonrise = place.next_rising(moon, start=dymdt)
	moonset = place.previous_setting(moon, start=dymdt)
	if moonrise - moonset > 0:
		moonset = place.next_setting(moon, start=dymdt)
	
	sunrisetime = (ephem.to_timezone(sunrise,ephem.UTC)+offset).strftime("%H:%M")
	place.date = sunrise
	sun.compute(place)
	sunriseaz = degstr(sun.az)
	
	x = place.date
	ephem.newton(riseblue,x,x+0.01)
	sunriseblue = (ephem.to_timezone(place.date,ephem.UTC)+offset).strftime("%H:%M")
	ephem.newton(risegold0,x,x+0.01)
	sunrisegold0 = (ephem.to_timezone(place.date,ephem.UTC)+offset).strftime("%H:%M")
	ephem.newton(risegold1,x,x+0.01)
	sunrisegold1 = (ephem.to_timezone(place.date,ephem.UTC)+offset).strftime("%H:%M")
	
	ephem.newton(setblue,x,x+0.01)
	sunsetblue = (ephem.to_timezone(place.date,ephem.UTC)+offset).strftime("%H:%M")
	ephem.newton(setgold0,x,x+0.01)
	sunsetgold0 = (ephem.to_timezone(place.date,ephem.UTC)+offset).strftime("%H:%M")
	ephem.newton(setgold1,x,x+0.01)
	sunsetgold1 = (ephem.to_timezone(place.date,ephem.UTC)+offset).strftime("%H:%M")
	
	noontime = (ephem.to_timezone(noon,ephem.UTC)+offset).strftime("%H:%M")
	place.date = noon
	sun.compute(place)
	noonaz = degstr(sun.az)
	noonalt = degstr(sun.alt)
	
	sunsettime = (ephem.to_timezone(sunset,ephem.UTC)+offset).strftime("%H:%M")
	place.date = sunset
	sun.compute(place)
	sunsetaz = degstr(sun.az)
	
	yestday = yestsunset - yestsunrise
	today = sunset - sunrise
	
	todaystr = hm(today)
	yestdiff = ms(today - yestday)
	
	if p['home']:
		print("%s %s |color=darkgray" % (p['name'],offtxt))
		print("%s %7s %s|font=Menlo color=%s" % (todaystr,yestdiff,sunnow,color))
	else:
		print("%s %s |color=%s" % (p['name'],offtxt,color))
		print("%s |font=Menlo color=%s" % ((now+local).strftime("%d %H:%M"),color))
		print("--%s %7s %s|font=Menlo color=%s" % (todaystr,yestdiff,sunnow,color))
	
	if moonaltnow > 0:
		print('%s%27s %3s %5s %2s%%%s' % (menu,degstr(moonaznow),degstr(moonaltnow),round(moondays,1),int(round(illumination)),"|font=Menlo color=silver trim=false"))
	else:
		print('%s%37s %2s%%%s' % (menu,round(moondays,1),int(round(illumination)),"|font=Menlo color=silver trim=false"))
	
	if not p['home']:
		print('-----')
	
	print('%s\033[31m\033[34m%s  \033[33m%s     \033[31m%s %4s  \033[33m%s| font=Menlo ansi=true' % (menu,sunriseblue,sunrisegold0,sunrisetime,sunriseaz,sunrisegold1))
	print('%s\033[31m                 %s %4s|font=Menlo ansi=true' % (menu,noontime,noonalt))
	print('%s\033[31m       \033[33m%s\033[37m     \033[31m%s %4s  \033[33m%s  \033[34m%s|font=Menlo ansi=true' % (menu,sunsetgold1,sunsettime,sunsetaz,sunsetgold0,sunsetblue))
	
	moonrisetime = (ephem.to_timezone(moonrise,ephem.UTC)+offset).strftime("%d %H:%M")
	place.date = moonrise
	moon.compute(place)
	moonriseaz = degstr(moon.az)
	moonsettime = (ephem.to_timezone(moonset,ephem.UTC)+offset).strftime("%d %H:%M")
	place.date = moonset
	moon.compute(place)
	moonsetaz = degstr(moon.az)
	
	if not p['home']:
		print('-----')
	print('%s %21s %4s|font=Menlo color=steelblue trim=false' % (menu,moonrisetime,moonriseaz))
	print('%s %21s %4s|font=Menlo color=steelblue trim=false' % (menu,moonsettime,moonsetaz))
	
	if p['home']:
		s = ""
		for ph in phasesort:
			s += ph['p'] + " " + ph['d'].strftime("%-m/%-d") + "   "
		print("%s|font=Menlo color=silver" % (s))
		print('---')

print('---')
print("UTC|color=gray")
print((now-offset).strftime("%d %H:%M")+"|font=Menlo color=gray")