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
		
switchtimes = []
switchstates = []

for i in range(len(dates)):
	if switches[i] == "EG_WZ_SchalterKO1_Power":
		switchtimes.append(dates[i])
		switchstates.append(states[i])

durations = []
		
for i in range(1, len(switchtimes)):
	if (not switchstates[i]) and switchstates[i-1]:
		durations.append(switchtimes[i]-switchtimes[i-1])

#statistics

seconds = 0

#        <1m <10m <1h rest
counts = [0, 0,   0,  0]

for d in durations:
	seconds += d.total_seconds()
	if d.total_seconds() < 60: counts[0] += 1
	elif d.total_seconds() < 600: counts[1] += 1
	elif d.total_seconds() < 3600: counts[2] += 1
	else: counts[3] += 1

print("Average time spent: " + str(datetime.timedelta(seconds=seconds//len(durations))))

for c in counts:
	print(c)
