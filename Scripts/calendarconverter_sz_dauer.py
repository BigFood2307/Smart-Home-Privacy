import datetime

file = open("..\Data\Switch Events.ics", "r")

state = "ready"

dates = []
switches = []
states = []

for line in file:
	cleanline = line.strip()
	if state == "ready":
		if cleanline == "BEGIN:VEVENT":
			state = "event"
			#print("Event Start")
			continue
	if state == "event":
		if cleanline.startswith("DTSTART:"):
			newdate = datetime.datetime(int(cleanline[8:12]), int(cleanline[12:14]),int(cleanline[14:16]), int(cleanline[17:19]), int(cleanline[19:21]), int(cleanline[21:23])) - datetime.timedelta(weeks=2) + datetime.timedelta(hours=1)
			dates.append(newdate)
			#print(newdate.isoformat())
			continue
		if cleanline.startswith("DESCRIPTION:send "):
			newswitch = cleanline.split(" ")[1]
			newstate = (cleanline.split(" ")[2] == "ON")
			switches.append(newswitch)
			states.append(newstate)
			#print(newswitch + " was set to " + str(newstate))
		if cleanline=="END:VEVENT":
			state = "ready"
			#print("Event End")
			continue
		
offtimes = []

lastoff = datetime.datetime.min
for i in range(len(dates)):
	if switches[i] == "OG_SZ_SchalterSZ1_Power" and not states[i]:
		if(lastoff.date() < dates[i].date()) and lastoff != datetime.datetime.min and (lastoff.time() > datetime.time(20)):
			offtimes.append(lastoff)
		lastoff = dates[i]
		
ontimes = []

laston = datetime.datetime.min
for i in range(len(dates)):
	if (switches[i] == "OG_SZ_SchalterSZ1_Power") and states[i]:
		if(laston.date() < dates[i].date()) and (dates[i].time() < datetime.time(10) and (dates[i].time() > datetime.time(4, 30))):
			ontimes.append(dates[i])
		laston = dates[i]
		
offsum = 0
offsumweekday = 0
offlenweekday = 0
offsumweekend = 0
offlenweekend = 0
for o in offtimes:
	offsum += o.second + 60*o.minute + 3600*o.hour
	if(o.weekday() < 4 or o.weekday == 6):
		offsumweekday += o.second + 60*o.minute + 3600*o.hour
		offlenweekday += 1
	else:
		offsumweekend += o.second + 60*o.minute + 3600*o.hour
		offlenweekend += 1

seconds = (offsum//len(offtimes))
secondsweekday = offsumweekday//offlenweekday
secondsweekend = offsumweekend//offlenweekend
	
offavg = datetime.time(seconds//3600, (seconds//60)%60, seconds%60)
offavgweekday = datetime.time(secondsweekday//3600, (secondsweekday//60)%60, secondsweekday%60)
offavgweekend = datetime.time(secondsweekend//3600, (secondsweekend//60)%60, secondsweekend%60)

print("Avg overall: " + str(offavg))
print("Avg weekdays: " + str(offavgweekday))
print("Avg weekends: " + str(offavgweekend))
print()

onsum = 0
onsumwd = 0
onlenwd = 0
onsumwe = 0
onlenwe = 0

for o in ontimes:
	onsum += o.second + 60*o.minute + 3600*o.hour
	if(o.weekday() < 5):
		onsumwd += o.second + 60*o.minute + 3600*o.hour
		onlenwd += 1
	else:
		onsumwe += o.second + 60*o.minute + 3600*o.hour
		onlenwe += 1

seconds = (onsum//len(ontimes))
secondswd = onsumwd//onlenwd
secondswe = onsumwe//onlenwe
	
onavg = datetime.time(seconds//3600, (seconds//60)%60, seconds%60)
onavgwd = datetime.time(secondswd//3600, (secondswd//60)%60, secondswd%60)
onavgwe = datetime.time(secondswe//3600, (secondswe//60)%60, secondswe%60)

print("Avg overall: " + str(onavg))
print("Avg weekdays: " + str(onavgwd))
print("Avg weekends: " + str(onavgwe))