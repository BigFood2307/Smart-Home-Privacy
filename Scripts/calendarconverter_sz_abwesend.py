import datetime

file = open("..\Data\Switch Events.ics", "r")

state = "ready"

dates = []
switches = []
states = []

for line in file:
	#Zeilenweise Analyse der Kalenderdatei
	cleanline = line.strip()
	if state == "ready":
		if cleanline == "BEGIN:VEVENT":
			state = "event"
			#print("Event Start")
			continue
	if state == "event":
		if cleanline.startswith("DTSTART:"):
			#Hier ist das Datum gespeichert, die 2 Wochen Verschiebung für die Anwesenheitssimulation, sowie eine Anpassung an die Zeitzone werden hier beachtet.
			newdate = datetime.datetime(int(cleanline[8:12]), int(cleanline[12:14]),int(cleanline[14:16]), int(cleanline[17:19]), int(cleanline[19:21]), int(cleanline[21:23])) - datetime.timedelta(weeks=2) + datetime.timedelta(hours=1)
			dates.append(newdate)
			#print(newdate.isoformat())
			continue
		if cleanline.startswith("DESCRIPTION:send "):
			#Die Daten, welcher Schater geschalten wurde und welchen Status er nun hat kommen in einem festen Format
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

#Das letzte Schalten eines Bestimmten Schalters pro Tag wird gesucht
lastoff = datetime.datetime.min
for i in range(len(dates)):
	if switches[i] == "OG_SZ_SchalterSZ1_Power" and not states[i]:
		if(lastoff.date() < dates[i].date()) and lastoff != datetime.datetime.min and (lastoff.time() > datetime.time(20)):
			offtimes.append(lastoff)
		lastoff = dates[i]
		
day = datetime.date(2019, 10, 12)
emptydays = []

i = 0
found = False

#Tage, an denen das Licht abends nicht geschaltet wurde werden notiert
while day < dates[-1].date():
	if(i >= len(offtimes)):
		break
	if day == offtimes[i].date():
		found = True
	if offtimes[i].date() > day:
		if not found:
			emptydays.append(day + datetime.timedelta(days = 1))
		found = False
		day += datetime.timedelta(days = 1)
		continue
	i += 1
	
for d in emptydays:
	print(d)
	
print("\n\n")

#for o in offtimes:
	#print(o)
