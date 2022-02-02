from cmath import nan
from itertools import islice
import json
#from threading import local
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import datetime
from dateutil import tz

with open('testdata.json') as f:
    data=json.load(f)
sample = data['captured_data']['hr']['ticks']
rrdata = data['captured_data']['hr']['RR in ms']
starttime_utc=data['Start_date_time']
sleep_position=data['captured_data']['slp']['sleep pos']
sleep_ticks=data['captured_data']['slp']['ticks']
#print(sample)
#print(starttime_utc)

d1 = datetime.datetime.strptime(starttime_utc,"%Y-%m-%dT%H:%M:%SZ")
new_format = "%Y-%m-%d %H:%M:%S"
d1.strftime(new_format)

from_zone=tz.tzutc()
to_zone=tz.tzlocal()
d1=d1.replace(tzinfo=from_zone)
local_time=d1.astimezone(to_zone)
#local_time.strftime(new_format)
#print(local_time)



#1 #2
rr_interval_in_seconds=[]
heartrate_in_bpm=[]
for i in range(0,len(sample)-1):
    rr_interval_in_seconds.append(abs(float(sample[i+1])-float(sample[i]))/512)
    try:
        #heartrate_in_bpm.append(60/(rr_interval_in_seconds[i]))
        heartrate_value=60/(rr_interval_in_seconds[i])
    except ZeroDivisionError:
        #heartrate_in_bpm.append(0)
        heartrate_value=0
    if 30<=heartrate_value<=240:
        heartrate_in_bpm.append(heartrate_value)
    else:
        heartrate_in_bpm.append(float("nan"))


    

print("RR Interval In Seconds: ", rr_interval_in_seconds)
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")




new_datetime=[]

sampletemp=list(np.float_(sample)/512)
sleep_pos_ticks=list(np.float_(sleep_ticks)/512)
rrdata_in_sec=list(np.float_(rrdata)/1000)

for i in range(0,len(sampletemp)):
    added_seconds = datetime.timedelta(0, sampletemp[i])
    new_datetime.append(local_time + added_seconds)

#print(new_datetime)





heartrate_in_bpm.insert(0,0)
rr_interval_in_seconds.insert(0,0)
#print(len(heartrate_in_bpm))
#print(sampletemp)

print("Heart Rate In BPM: ",heartrate_in_bpm) 

#3 #4



heartrate_in_bpm_temp=[]
sampletemp_temp=[]
new_datetime_temp=[]
for i in range(0,len(heartrate_in_bpm)):
    if np.isnan(heartrate_in_bpm[i]):
        continue
    else:
        heartrate_in_bpm_temp.append(heartrate_in_bpm[i])
        sampletemp_temp.append(sampletemp[i])
        new_datetime_temp.append(new_datetime[i])




plt.plot(new_datetime_temp[1:150],heartrate_in_bpm_temp[1:150])
plt.show()




func=interp1d(sampletemp_temp,heartrate_in_bpm_temp,kind="slinear")
x1=np.linspace(0,3600,20)
y1=np.array([func(x) for x in x1])

plt.plot(x1,y1,"ro:")
plt.show()



#5

loose_contact_time=0
total_loose_contact_time=0

#print(rrdata_in_sec)

for i in range(1,len(rrdata_in_sec)):
    if rrdata_in_sec[i]==0:
        j=0
        while sleep_pos_ticks[j]<sampletemp[i]:
            j=j+1
        if sleep_position[j]==5 or sleep_position[j]==7 or sleep_position[j]==8 or sleep_position[j]==9:
            loose_contact_time=sampletemp[i]-sampletemp[i-1]
        total_loose_contact_time=total_loose_contact_time+loose_contact_time


print("Total loose contact time",total_loose_contact_time," seconds")


#6


def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]

blocklist = list(divide_chunks(sleep_position, 30))


hravg=[]
for i in range(len(blocklist)):
    hr=[]
    for j in range(len(blocklist[i])):
        if blocklist[i][j]==5 or blocklist[i][j]==7 or blocklist[i][j]==8 or blocklist[i][j]==9:
            k=0
            while sleep_pos_ticks[30*i+j]>=sampletemp[k]:
                k=k+1
            hr.append(heartrate_in_bpm[k])
            #print(heartrate_in_bpm[k])
    if(len(hr)!=0):
        hravg.append(sum(hr)/len(hr))
    else:
        hravg.append(0)

#print(hravg)



dip=hravg[1]-hravg[0]
for i in range(1,len(hravg)):
    temp_dip=hravg[i]-hravg[i-1]
    if temp_dip<dip:
        dip=temp_dip
   
print("Biggest dip",dip)


#7

count_hr=0
for i in range(0,len(hravg)):
    if hravg[i]>80:
        count_hr=count_hr+1

print("Number of avg HR above 80bpm",count_hr)



#8
supine_hr=[]
prone_hr=[]
for i in range(0,len(sleep_position)):
    if sleep_position[i]==5:   #supine
        k=0
        while sleep_pos_ticks[i]>=sampletemp[k]:
            k=k+1
        if np.isnan(heartrate_in_bpm[k]):
            continue
        else:
            supine_hr.append(heartrate_in_bpm[k])
    if sleep_position[i]==9:   #prone
        k=0
        while sleep_pos_ticks[i]>=sampletemp[k]:
            k=k+1
        if np.isnan(heartrate_in_bpm[k]):
            continue
        else:   
            prone_hr.append(heartrate_in_bpm[k])

#print(supine_hr)
#print(prone_hr)
if len(supine_hr)!=0:
    supine_avg=sum(supine_hr)/len(supine_hr)
if len(prone_hr)!=0:
    prone_avg=sum(prone_hr)/len(prone_hr)


print("Difference in avg HR between supine and prone: ",supine_avg-prone_avg,"bpm")





