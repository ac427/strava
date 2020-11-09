# strava

`activities_stream_runs.py` fetches the data of last month runs and plots

`activities_stream_ride.py` fetches the data of last year rids and plots ( check `after='last month' if you want to modify )

* Link to et secret https://www.strava.com/settings/api

#set up
```
pip3 install --user -r requirements.txt 
export STRAVA_SECRET=xxxxxxxx
```

Sample Run plot
![Sample Run Plot](https://raw.githubusercontent.com/ac427/strava/main/example.png)
Sample Ride plot
![Sample Ride Plot](https://raw.githubusercontent.com/ac427/strava/main/example_ride.png)
