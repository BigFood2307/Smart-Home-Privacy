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
		
switchtimes = []
switchstates = []

#Begrenzung der Daten auf einen Schalter und einen bestimmten Zeitraum
for i in range(len(dates)):
	if switches[i] == "EG_WC_SchalterWC1_Power":
		if dates[i] > datetime.datetime(2019, 10, 12):
			switchtimes.append(dates[i])
			switchstates.append(states[i])

durations = []
durationtimes = []
		
#Filtern auf Daten, bei denen der Schalter ausgeschaltet wurde.
for i in range(1, len(switchtimes)):
	if (not switchstates[i]) and switchstates[i-1]:
		durations.append(switchtimes[i]-switchtimes[i-1])
		durationtimes.append(switchtimes[i-1])

#statistics, Wann wurde der Schalter wie oft gedrückt und wie lange war er an

seconds = 0

#        <1m <10m <1h <12h rest
counts = [0, 0,   0,  0,   0]
timecounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

i = 0

for d in durations:
	#print(d)
	timecounts[durationtimes[i].hour//2] += 1
	seconds += d.total_seconds()
	if d.total_seconds() < 60: counts[0] += 1
	elif d.total_seconds() < 600: counts[1] += 1
	elif d.total_seconds() < 3600: counts[2] += 1
	elif d.total_seconds() < 43200: counts[3] += 1
	else: counts[4] += 1
	i += 1

print("Average time spent: " + str(datetime.timedelta(seconds=seconds//len(durations))))

for c in counts:
	print(c)
	
print(len(durations))
print(timecounts)
