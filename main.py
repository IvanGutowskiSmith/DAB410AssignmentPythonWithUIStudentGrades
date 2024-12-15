import pandas as pd
#import datetime # Used for testing remove later when not needed
#print(datetime.datetime.now())

dataFrame = pd.read_csv('student_grades.csv')
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', None)

# Global Variables
TOTAL_STUDENT_COUNT = len(dataFrame) # Populate total student count on application start
GRADE_PASS_BOUNDARY = 40 # >= 40 is a pass

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






