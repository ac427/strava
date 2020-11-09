#!/bin/env pyton3

""" Plots strava data of last month runs """
import os
import math
from stravaio import strava_oauth2
from stravaio import StravaIO
from matplotlib import pyplot as plt

SECRET = os.environ['STRAVA_SECRET']

TOKEN = strava_oauth2(client_id=55889, client_secret=SECRET)

CLIENT = StravaIO(access_token=TOKEN['access_token'])

A_IDS = []
META = {}


def closest(lst, k):
    """ returns closest value to k in list """
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-k))]


def start_time(activity):
    """ fetches start_time for the activity """
    for value in LIST_ACTIVITIES:
        if str(activity) in value.map.id:
            return value.start_date.strftime("%b%d")
    return 0000


LIST_ACTIVITIES = CLIENT.get_logged_in_athlete_activities(after='last month')

ATHLETE_ID = LIST_ACTIVITIES[0].athlete.id
for item in LIST_ACTIVITIES:
    if item.type == 'Run':
        A_IDS.append(item.id)


for a_id in A_IDS:
    x_axis = []
    a_time = []
    a_altitude = []
    a_cadence = []
    a_heartrate = []
    a_stream = CLIENT.get_activity_streams(a_id, ATHLETE_ID)
    total_distance = a_stream.distance[-1]*0.00062137
    distance = a_stream.distance
    # a_distance = [i * 0.00062137 for i in distance]
    # lets plot the first 3 miles
    for i in range(math.floor(total_distance)):
        closest_mile_value = closest(distance, i*1609.34)
        index = distance.index(closest_mile_value)
        # convert to miles
        a_altitude.append(a_stream.altitude[index])
        a_cadence.append(a_stream.cadence[index])
        a_heartrate.append(a_stream.heartrate[index])
        a_time.append(a_stream.time[index]/60)
    time_per_mile = ([y - x for x, y in zip(a_time, a_time[1:])])
    time_per_mile.insert(0, 0)
    a_date = start_time(a_id)
    META[a_id] = {"date": a_date, "mile_time": time_per_mile, "time": a_time,
                  "heartrate": a_heartrate, "cadence": a_cadence, "altitude": a_altitude}


FIG, AXS = plt.subplots(2, 2)
AXS[0, 0].set_title('time/mile')
for values in META.values():
    AXS[0, 0].plot(range(len(values['mile_time'])),
                   values['mile_time'], label=values['date'])
AXS[0, 0].legend(loc='best')
AXS[0, 1].set_title('Heartrate')
for values in META.values():
    AXS[0, 1].scatter(range(len(values['heartrate'])),
                      values['heartrate'], label=values['date'])
AXS[0, 1].legend(loc='best')
AXS[1, 0].set_title('cadence')
for values in META.values():
    AXS[1, 0].plot(range(len(values['cadence'])),
                   values['cadence'], label=values['date'])
AXS[1, 0].legend(loc='best')
AXS[1, 1].set_title('altitude')
for values in META.values():
    AXS[1, 1].plot(range(len(values['altitude'])),
                   values['altitude'], label=values['date'])
AXS[1, 1].legend(loc='best')
plt.show()
