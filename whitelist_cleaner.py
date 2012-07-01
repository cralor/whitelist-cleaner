import time
import os
 
serverlog = raw_input("Path to log file: ")
print ">>>>WARNING! BACK UP YOUR WHITELIST BEFORE USING THIS!<<<<"
whitelist = raw_input("Path to whitelist file: ")
temp = raw_input("Enter a path to a temp file to store data: ")
print "All players who have not played since this date will be deleted"
expiration_date = raw_input("Expiration date (Year-month-day ex:2012-03-18): ")
exact_expiration = time.mktime(time.strptime(expiration_date,"%Y-%m-%d"))
log_file = open(serverlog, "r")
whitelist_file = open(whitelist, "r")
 
start = time.time()
good_players = []
lastLoginsPerPlayer = {}
 
def filter_logs(logs, temp):
    tempFile = open(temp, "a")
    for line in logs.readlines():
        if 'lost connection' in line:
            if '/' not in line:
                tempFile.write(line)
 
def getTrueTime(logTime):
    return time.mktime(time.strptime(logTime, "%Y-%m-%d"))
 
def getLastLogins(temp, LLPP):
    tempFile = open(temp, "r")
    for line in tempFile.readlines():
        line = line.split(" ")
        player = line[3]
        currentTime = getTrueTime(line[0])
        try:
            oldTime = LLPP[player]
            if old < currentTime:
                LLPP[player] = currentTime
        except:
            LLPP[player] = currentTime
         
def writeNewWhiteList(good, whitelist_path):
    os.remove(whitelist_path)
    newWhiteList = open(whitelist_path, "a")
    for player in good:
        newWhiteList.write(player + "\n")
 
filter_logs(log_file, temp)
getLastLogins(temp, lastLoginsPerPlayer)
 
 
for player in whitelist_file.readlines():
    player = player.strip("\n")
    try:
        last_logout = lastLoginsPerPlayer[player]
        if last_logout > exact_expiration:
            good_players.append(player)
    except:
        print "Looks like " + player + " never logged in... Are you sure your log file is complete?"
        good_players.append(player)
 
writeNewWhiteList(good_players, whitelist)
os.remove(temp)
print "Time elapsed: " + str(time.time() - start) + " seconds."