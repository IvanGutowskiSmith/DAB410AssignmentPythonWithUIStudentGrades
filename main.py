import pandas as pd
import numpy as np # np is alias, not needed but this is best practice
import tkinter as tk
import datetime # Used for testing remove later when not needed
#print(datetime.datetime.now())

dataFrame = pd.read_csv('student_grades.csv')
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', None)

# Global Variables
TOTAL_STUDENT_COUNT = len(dataFrame) # Populate total student count on application start
GRADE_PASS_BOUNDARY = 40 # >= 40 is a pass
GRADE_A_MINIMUM = 70 # greater than or eq to
GRADE_B_MINIMUM = 60 # eq or greater than 60, less than 70
GRADE_C_MINIMUM = 50

print("Total Student count: "+ str(TOTAL_STUDENT_COUNT))

averageAttendance = dataFrame["attendance"].mean() # Using Panda's built in mean average to calculate result, restricted to desired column for attendance
print("Average grade is:",str(round(dataFrame["grade"].mean(),2)),"%") # Panda to average column 'grade', round to two significant figures, convert, concatenate within a string to print

# Count pass / fails
runningTotalPassCount = int() # Declare empty variable, 'none' would cause error, considered using zero however, may hide errors as program would run
runningTotalFailCount = int()



for index,row in dataFrame.iterrows():
    rowGrade = row['grade'] # Could combine this into if statement, however easier to debug if value is extracted to variable before being compared
    if rowGrade >= GRADE_PASS_BOUNDARY:
        runningTotalPassCount = runningTotalPassCount + 1 # Python does not have ++ operator to increment
    else:
        runningTotalFailCount = runningTotalFailCount + 1


print("Total Pass: ", str(runningTotalPassCount))
print("Total Fail: ",str(runningTotalFailCount))


# Calculating grade count A,B,C

df = dataFrame["grade"]
aTrues = (df >= GRADE_A_MINIMUM) # Could validate upper limit, however known presumptions are that grades cannot exceed 100%
bTrues = (df >= GRADE_B_MINIMUM) & (df < GRADE_A_MINIMUM) # Greater or eq 60, less than 70
cTrues = (df >= GRADE_C_MINIMUM) & (df < GRADE_B_MINIMUM) # Greater or eq 50, less than 60

print("Grade A count: ",np.count_nonzero(aTrues))
print("Grade B count: ",np.count_nonzero(bTrues))
print("Grade C count: ",np.count_nonzero(cTrues))




