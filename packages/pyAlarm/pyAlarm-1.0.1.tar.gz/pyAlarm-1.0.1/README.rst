Alarm in Python.

## INSTALLATION 

pip install pyAlarm

Functions :

getInput() :: returns Alarm and current Time.
runInBackground(Time,Alarm) :: Alarm & Time of type time.strftime("%H:%M")
checkYTfile() :: returns False if File not found , True if found.
runInteractive()
setPath() :: give complete path to a .txt file with youtube links as alarmVideos.


Import :

from alarm import begin


Use :

a,t = begin.getInput()
begin.runInBackground(t,a)
begin.checkYTfile()
begin.runInteractive()