import datetime
import json

door = "EG_FL_Haustuer"

file = open("..\Data\\" + door + "_Contact.json", "r")

jsontext = file.read()

file.close()

result = json.loads(jsontext)
values = result["results"][0]["series"][0]["values"]

for v in values:
	v[0] = datetime.datetime.fromisoformat(v[0].split(".")[0] + "+00:00").astimezone()
	#print(v[0])
	
#data ready

actualOpens = []

timedifsum = datetime.timedelta(0)
timedifcnt = 0

for i in range(1, len(values)):
	if values[i][1] and not values[i-1][1]:# and values[i][0].weekday() < 5:
		actualOpens.append(values[i])
		if(i < len(values)-1):
			if (values[i+1][0] - values[i][0]).total_seconds() < 3600:
				timedifsum += values[i+1][0] - values[i][0]
				#print(values[i+1][0] - values[i][0])
				timedifcnt += 1
			
print("Average time opened: " + str(datetime.timedelta(seconds = timedifsum.total_seconds()//timedifcnt)))

#for ao in actualOpens:
	#print(ao[0])
		
print("Number of Opens:" + str(len(actualOpens)))

timecounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for ao in actualOpens:
	timecounts[ao[0].hour//2] += 1
	
print(timecounts)

#"""

lastDate = datetime.date.min
firstOpens = []

for ao in actualOpens:
	if ao[0].date() > lastDate:
		if(ao[0].hour >= 5 and ao[0].hour < 10):
			lastDate = ao[0].date()
			firstOpens.append(ao)
			
secondsSum = 0

for fo in firstOpens:
	secondsSum += fo[0].second + fo[0].minute*60 + fo[0].hour*3600

secondsAvg = secondsSum//len(firstOpens)
			
print("Number of first Opens: " + str(len(firstOpens)))
print("Average Time: " + str(datetime.timedelta(seconds=secondsAvg)))

testDate = firstOpens[0][0].date()
opened = False

unopenedMorningDays = []

i = 0

while testDate <= firstOpens[-1][0].date() and i < len(firstOpens):
	if firstOpens[i][0].date() == testDate:
		opened = True
	if firstOpens[i][0].date() > testDate:
		if not opened:
			unopenedMorningDays.append(testDate)
		testDate += datetime.timedelta(days = 1)
		opened = False
	else:
		i += 1
		
print("Days without opening in morning: " + str(len(unopenedMorningDays)))

for umd in unopenedMorningDays:
	print(umd)

testDate = actualOpens[0][0].date()
opened = False

unopenedDays = []

i = 0

while testDate <= actualOpens[-1][0].date() and i < len(actualOpens):
	if actualOpens[i][0].date() == testDate:
		opened = True
	if actualOpens[i][0].date() > testDate:
		if not opened:
			unopenedDays.append(testDate)
		testDate += datetime.timedelta(days = 1)
		opened = False
	else:
		i += 1
		
print("Days without opening all day: " + str(len(unopenedDays)))

#"""