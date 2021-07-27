#
# Analyze Sussex County, DE AUXCOMM Volunteer Reporting Hours
import os
import csv # needed to initially correct record errors before analysis
import pandas as pd
import datetime as dt
from datetime import timedelta
#
def writeLine(line):
    print(f"{line}")
    if rptFileName != '':
        reportLine.write(line + '\n')    
#
dashes = "-" * 55
cPath = os.getenv('USERPROFILE') + '/onedri~1/amateu~1/races-~1/2021_m~1/'
currentPathFileList = os.listdir(path = cPath)
csvFileList = []
#
for fileName in currentPathFileList:
#
# Check extension of fileName
    extIdx = fileName.find('.')
    if fileName[extIdx:] == '.csv':
        csvFileList.append(fileName) # copy all .csv filenames to csvFileList
#
# Display an indexed list of CSV files in the current path
print("Select a .CSV file to analyze:\n")
for fileIdx in range(len(csvFileList)):
    print(f" [{fileIdx + 1}] ..... {csvFileList[fileIdx]}")
#
validInput = False
while not validInput:
    fileNum = input("\nEnter the file number to analyze:> ")
    try:
        fileNum = int(fileNum)
    except ValueError:  # user did not enter a number
        fileNum = 0     # intentionally fail condition test
    if fileNum > len(csvFileList) or fileNum < 1:
        validInput = False
    else:
        fileNum -= 1
        validInput = True
#
print(f"Repairing {csvFileList[fileNum]} .....")
csvFile = csvFileList[fileNum]
#
# Read csv records into a list
surveyRecord = []
with open(cPath + csvFile, newline = '') as msRpt:
    surveyFile = csv.reader(msRpt)
    for record in surveyFile:
        surveyRecord.append(record)
#
# Check each Activity Record for these specific errors ---
for record in range(len(surveyRecord)):
#
# --- Make all callsigns upper-case in field #1 'Callsign', trim leading spaces, & trim trailing spaces
    if record > 0:  # Skip the header row
        surveyRecord[record][1] = surveyRecord[record][1].upper()
        surveyRecord[record][1] = surveyRecord[record][2].strip()

#
# --- Check for negative values in field #4 'Volunteer Activity Hours'
#    try:
#        volActyHrs = float(actyRecord[record][4])
#    except ValueError:
#        continue    # move on to the next record - most likely occurred in record #0 (header record)
#    if volActyHrs < 0:
#        actyRecord[record][4] = str(abs(volActyHrs))
#

#
# --- Check for '\n' & replace with ' | ' in field #5 'Details'
    if '\n' in surveyRecord[record][6]:
        surveyRecord[record][6] = surveyRecord[record][6].replace('\n', ' | ')
#
# Overwrite the csv file with the corrected records
with open(cPath + csvFile, 'w', newline = '') as msRpt:
    surveyFile = csv.writer(msRpt)
    for record in range(len(surveyRecord)):
        surveyFile.writerow([surveyRecord[record][0],surveyRecord[record][1],surveyRecord[record][2],surveyRecord[record][3],surveyRecord[record][4],surveyRecord[record][5],surveyRecord[record][6],surveyRecord[record][7],surveyRecord[record][8]])
#
# read csv file into a pandas dataframe
print("Reading SCAUXCOMM Membership Survey Dataset...")
msr = pd.read_csv(cPath + csvFile)
#
print(f"Read {len(msr)} records...\n")
print(f"{dashes}")
#
# Does the user want to send the report to a .txt file?
rptFileName = input("Enter a filename for the summary report or press [Enter] for screen only: ")
if rptFileName != '':
    reportLine = open(cPath + rptFileName + '.txt','w')
#
rightNow = dt.datetime.now()
currentDate = str(rightNow)[:10]
currentTime = '@' + str(rightNow)[11:16]
#
# Generate report headers
rptStartDate = csvFile[24:29]
rptEndDate = csvFile[38:43]
rptYear = csvFile[18:23]
#
writeLine("Sussex County, Delaware AUXCOMM")
writeLine(f"Membership Survey Report for {rptStartDate}{rptYear} to {rptEndDate}{rptYear}")
writeLine(f"Generated from {len(msr)} records at: {currentDate} {currentTime}\n")
#
# Membership Survey Keys (Column Headers)
# 'Submitted At' ------------------------------ timestamp of report submission
# 'Callsign' ---------------------------------- callsign of person submitting the report
#
# 'Band Capabilities' ------------------------- [ ] HF      [ ] VHF     [ ] UHF     [ ] Digital
#
# 'When were you last active on the air?' --    [ ] Today   [ ] This Week   [ ] This Month
#                                               [ ] Last 6 months           [ ] Last Year
#
# 'What has been your level of on-the-air activity during the pandemic?'
#                                               [ ] More Active since COVID began
#                                               [ ] About the same level of activity
#                                               [ ] Less Active since COVID began
#
# 'What is your favorite AUXCOMM activity? (Check all that apply)'
#                                               [ ] Training Drills/Exercises
#                                               [ ] Open Operating Night
#                                               [ ] Public Service Events
#                                               [ ] Membership Meetings
#                                               [ ] Educational Seminars
#                                               [ ] Other
#
# 'What would you like to see us do in the future?'
# 'Locale' -------------------- Region where report originated
# 'Submission Source' --------- website where report originated
#
# Report Summary Requirements:
# Count 'Band Capabilities' responses:                                                      (total # HF; total # VHF; total # UHF; total # Digital)
# Count 'When were you last active on the air?' responses:                                  (total # Today; etc)
# Count 'What has been your level of on-the-air activity during the pandemic?' responses:   (total # More Active...; etc)
# Count 'What is your favorite AUXCOMM activity?' responses:                                (total # Training; etc)
# List 'What would you like to see us do in the future?' responses
#
columnHeaders = ('Submitted At',
                 'Callsign',
                 'Band Capabilities',
                 'When were you last active on the air?',
                 'What has been your level of on-the-air activity during the pandemic?',
                 'What is your favorite AUXCOMM activity? (Check all that apply)',
                 'What would you like to see us do in the future?',
                 'Locale',
                 'Submission Source')
#
bandCapabilitiesLabels = ('HF',
                          'VHF',
                          'UHF',
                          'Digital')
longestBandCapability = len(bandCapabilitiesLabels[3])
capabilitiesCount = dict.fromkeys(bandCapabilitiesLabels,0)
#
lastActiveTimeframeLabels = ('Today',
                              'This Week',
                              'This Month',
                              'Last 6 months',
                              'Last Year')
longestActiveTimeframe = len(lastActiveTimeframeLabels[3])
timeFrameCount = dict.fromkeys(lastActiveTimeframeLabels,0)
#
activityLevelLabels = ('More Active since COVID began',
                        'About the same level of activity',
                        'Less Active since COVID began')
longestActivityLevel = len(activityLevelLabels[1])
actyLevelCount = dict.fromkeys(activityLevelLabels,0)
#
favAuxCommActivitiesLabels = ('Training Drills/Exercises',
                              'Open Operating Night',
                              'Public Service Events',
                              'Membership Meetings',
                              'Educational Seminars',
                              'Other')
longestAuxCommActy = len(favAuxCommActivitiesLabels[0])
auxCommActyCount = dict.fromkeys(favAuxCommActivitiesLabels,0)
#
futureActivitiesList = []   # store all responses for 'What would you like to see us do in the future?' here
#
# Extract data from each dataframe record
for idx in range(len(msr)):
#
# Retrieve record fields
#    submissionTimeStamp = msr.get(columnHeaders[0])[idx]
    bandCapabilities = msr.get(columnHeaders[2])[idx]
    lastActiveTimeframe = msr.get(columnHeaders[3])[idx]
    activityLevel = msr.get(columnHeaders[4])[idx]
    favAuxCommActy = msr.get(columnHeaders[5])[idx]
    futureActivitiesList.append(msr.get(columnHeaders[6])[idx])
#
# Update band capabilities count dictionary
    for capability in bandCapabilitiesLabels:
        count = 0
        if capability in bandCapabilities:
            count = int(capabilitiesCount.get(capability)) + 1  # Add old dictionary value to count
            capabilitiesCount.update({capability:count})        # Update dictionary with new value
#
    for timeframe in lastActiveTimeframeLabels:
        count = 0
        if timeframe in lastActiveTimeframe:
            count = int(timeFrameCount.get(timeframe)) + 1      # Add old dictionary value to count
            timeFrameCount.update({timeframe:count})            # Update dictionary with new value
#
    for actyLevel in activityLevelLabels:
        count = 0
        if actyLevel in activityLevel:
            count = int(actyLevelCount.get(actyLevel)) + 1      # Add old dictionary value to count
            actyLevelCount.update({actyLevel:count})            # Update dictionary with new value
#
    for favActy in favAuxCommActivitiesLabels:
        count = 0
        if favActy in favAuxCommActy:
            count = int(auxCommActyCount.get(favActy)) + 1      # Add old dictionary value to count
            auxCommActyCount.update({favActy:count})            # Update dictionary with new value
#
# Generate report
writeLine("Band Capabilities Summary:")
for capability in bandCapabilitiesLabels:
    capblty = capability + (' ' * (longestActivityLevel - len(capability)))
    count = capabilitiesCount.get(capability)
    writeLine(f"{capblty}  :  {count} records [{count/len(msr)*100:5.1f}%]")
writeLine(f"{dashes}")
#
writeLine("Last Active Timeframe Summary:")
for timeFrame in lastActiveTimeframeLabels:
    tmFrm = timeFrame + (' ' * (longestActivityLevel - len(timeFrame)))
    count = timeFrameCount.get(timeFrame)
    writeLine(f"{tmFrm}  :  {count} records [{count/len(msr)*100:5.1f}%]")
writeLine(f"{dashes}")
#
writeLine("Activity Level Summary:")
for activityLevel in activityLevelLabels:
    actyLvl = activityLevel + (' ' * (longestActivityLevel - len(activityLevel)))
    count = actyLevelCount.get(activityLevel)
    writeLine(f"{actyLvl}  :  {count} records [{count/len(msr)*100:5.1f}%]")
writeLine(f"{dashes}")
#
writeLine("Favorite AUXCOMM Activity Summary:")
for favoriteActivity in favAuxCommActivitiesLabels:
    favActy = favoriteActivity + (' ' * (longestActivityLevel - len(favoriteActivity)))
    count = auxCommActyCount.get(favoriteActivity)
    writeLine(f"{favActy}  :  {count} records [{count/len(msr)*100:5.1f}%]")
writeLine(f"{dashes}")
#
writeLine("Future Activities Suggestions:")
for suggestion in futureActivitiesList:
    writeLine(f"{suggestion}")
writeLine(f"{dashes}")
#
# End report, close report file
if rptFileName != '': reportLine.close()
