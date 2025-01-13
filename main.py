from re import search

import pandas as pd
import numpy as np # np is alias, not needed but this is best practice

import tkinter as tk
from tkinter import ttk
#import datetime # Used for testing remove later when not needed
#print(datetime.datetime.now())


# Setup UI
root = tk.Tk()
root.geometry('1280x720') # 16:9 aspect ratio that should fit on most screens
root.minsize(640,360)
root.title('Student Grade Manager. Student ID: 2310700')
appFont = 'Calibri'


# Main layout widgets
menu_frame = ttk.Frame(root)
main_frame_left = ttk.Frame(root)
main_frame_centre = ttk.Frame(root)
main_frame_right = ttk.Frame(root)

# Place main layout
menu_frame.place(x = 0,y = 0, relwidth = 1, height = 25)
main_frame_left.place(x = 0,y = 25, relwidth = 0.25, relheight = 1)
main_frame_centre.place(relx = 0.25,y = 25, relwidth = 0.5, relheight = 1)
main_frame_right.place(relx = 0.75,y = 25, relwidth = 0.25, relheight = 1)

ttk.Label(menu_frame, background = 'red').pack(expand = True, fill = 'both')
ttk.Label(main_frame_left, background = 'green').pack(expand = True, fill = 'both')
ttk.Label(main_frame_centre, background = 'grey').pack(expand = True, fill = 'both')
ttk.Label(main_frame_right, background = 'blue').pack(expand = True, fill = 'both')







































#root.columnconfigure(0, weight=1, uniform = 'a') # index, weight, uniformity ensures equal column widths
#root.columnconfigure(1, weight=2, uniform = 'a')
#root.columnconfigure(2, weight=1, uniform = 'a')
#root.rowconfigure(0, weight=1,minsize = 25)
#root.rowconfigure(1, weight=20, uniform = 'b')
#
## Add a Frame widget
#frame = tk.Frame(root, bg = 'Green')
#
#label_1 = ttk.Label(frame, background = 'black', text = 'Menu')
#label_1.grid(column=0, row=0, sticky='NEWS', columnspan = 1)
#
#
#
#
#
#
#
#
#
#
#label_Top_Menu = ttk.Label(root, background = 'darkRed', text = 'Menu')
#label_Top_Menu.grid(column=0, row=0, sticky='NEWS', columnspan = 3)
#
#label_LeftFilters = ttk.Label(root, background = 'darkGreen', text = 'Left Menu')
#label_LeftFilters.grid(column=0, row=1, sticky='NEWS')
#
#label_Central_Results = ttk.Label(root, background = 'lightBlue', text = 'Central Results')
#label_Central_Results.grid(column=1, row=1, sticky='NEWS')
#
#label_Right_Student_Info = ttk.Label(root, background = 'lightGreen', text = 'Student Info')
#label_Right_Student_Info.grid(column=2, row=1, sticky='NEWS')
#
#
## Layout inside a frame
#search_frame = ttk.Frame(root)
#search_frame.columnconfigure(0, weight=1, uniform = 'a')
#search_frame.columnconfigure(1, weight=1, uniform = 'a')
#search_frame.rowconfigure(0, weight=1, uniform = 'b')
#
#search_Box = ttk.Label(search_frame, background = 'Grey', text = 'Search Box')
#search_Box.grid(column=2, row=1, sticky='NEWS')
#
#
#label_LeftFilters.columnconfigure(0, weight=1, uniform = 'a')
#label_LeftFilters.columnconfigure(1, weight=1, uniform = 'a')
#root.rowconfigure(0, weight=1, uniform = 'b')
#
#search_Box = ttk.Label(label_LeftFilters, background = 'Grey', text = 'Search Box')
#
#


# root.columnconfigure(0, weight=1, uniform = 'a') # index, weight, uniformity ensures equal column widths
# root.columnconfigure(1, weight=2, uniform = 'a')
# root.columnconfigure(2, weight=1, uniform = 'a')
# root.rowconfigure((0,1,2,3), weight=1, uniform = 'b') # Can use tuple to save duplicate lines of code, 4 rows created


# Frame for student search
#searchLabelFrame = ttk.LabelFrame(root,text='Search label Frame') # Frame to contain search elements
#.grid(column=0,row=0,sticky = 'NEWS') # place frame in grid
# Search box
#search_entry = ttk.Entry(root) #creating single line text entry box, with searchLabelFrame as parent
#search_entry.grid(column=0,row=0,sticky = 'we')
# Search btn
#search_btn = ttk.Button(root, text='Search for student')
#search_btn.grid(column=0,row=0,sticky = 'e',padx = 5)




# Run UI
root.mainloop()







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




