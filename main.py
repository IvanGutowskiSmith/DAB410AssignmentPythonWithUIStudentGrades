from re import search

import pandas as pd
import numpy as np # np is alias, not needed but this is best practice

import tkinter as tk
from tkinter import ttk
#import datetime # Used for testing remove later when not needed
#print(datetime.datetime.now())


# Setup UI
window = tk.Tk()
window.title('Student Grade Manager')
window.geometry('1280x720') # 16:9 aspect ratio that should fit on most screens

appFont = 'Calibri'

# Main packs
left_filter_pane = ttk.Frame(master = window)
center_results_pane = ttk.Frame(master = window)
right_student_info_pane = ttk.Frame(master = window)

# Main pack layouts
left_filter_pane.pack(side = 'left')

# Title text
stats_Summary = ttk.Label(master = window, text = 'Student Grade Summaries', font = appFont,borderwidth=2, relief='groove') # Label widget, can add size and bold to appFont
stats_Summary.pack()

# Student search
search_frame = ttk.Frame(master = left_filter_pane) # Creating frame for search box widgets
search_box = ttk.Entry(master = search_frame) # lives inside the search frame, 'Entry' used as it's single line and not multiline input
search_button = ttk.Button(master = search_frame, text = 'Search')
# Student search layout

search_frame.pack(side = 'top') # Higher level pack that contains below search box and search button
search_box.pack(side = 'left', padx = 10) # Side argument places both on same line
search_button.pack(side = 'left', padx = 5) # Pad puts gap on x axis to space between search box and button




# Run UI
window.mainloop()







# Import file / logic

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




