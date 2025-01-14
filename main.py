from re import search

import pandas as pd
import numpy as np # np is alias, not needed but this is best practice

import tkinter as tk
from tkinter import ttk
#import datetime # Used for testing remove later when not needed
#print(datetime.datetime.now())


##########################LOGIC

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

AVERAGE_ATTENDANCE = round(dataFrame["attendance"].mean(),2) # Using Panda's built in mean average to calculate result, rounded
AVERAGE_GRADE = round(dataFrame["grade"].mean(),2)
print("Average grade is:",str(AVERAGE_GRADE),"%") # Panda to average column 'grade', round to two significant figures, convert, concatenate within a string to print

# Count pass / fails
runningTotalPassCount = int() # Declare empty variable, 'none' would cause error, considered using zero however, may hide errors as program would run
runningTotalFailCount = int()



for index,row in dataFrame.iterrows():
    rowGrade = row['grade'] # Could combine this into if statement, however easier to debug if value is extracted to variable before being compared
    if rowGrade >= GRADE_PASS_BOUNDARY:
        runningTotalPassCount = runningTotalPassCount + 1 # Python does not have ++ operator to increment
    else:
        runningTotalFailCount = runningTotalFailCount + 1

TOTAL_PASS_COUNT = runningTotalPassCount
TOTAL_FAIL_COUNT = runningTotalFailCount
print("Total Pass: ", str(TOTAL_PASS_COUNT))
print("Total Fail: ",str(TOTAL_FAIL_COUNT))


# Calculating grade count A,B,C

df = dataFrame["grade"]
aTrues = (df >= GRADE_A_MINIMUM) # Could validate upper limit, however known presumptions are that grades cannot exceed 100%
bTrues = (df >= GRADE_B_MINIMUM) & (df < GRADE_A_MINIMUM) # Greater or eq 60, less than 70
cTrues = (df >= GRADE_C_MINIMUM) & (df < GRADE_B_MINIMUM) # Greater or eq 50, less than 60

GRADE_A_COUNT = np.count_nonzero(aTrues)
GRADE_B_COUNT = np.count_nonzero(bTrues)
GRADE_C_COUNT = np.count_nonzero(cTrues)
print("Grade A count: ",GRADE_A_COUNT)
print("Grade B count: ",GRADE_B_COUNT)
print("Grade C count: ",GRADE_B_COUNT)






####################### UI


# Setup UI
root = tk.Tk()
root.geometry('1280x720') # 16:9 aspect ratio that should fit on most screens
root.minsize(640,360)
root.title('Student Grade Manager. Student ID: 2310700')
appFont = 'Calibri'


# Main layout widgets
menu_banner_frame = ttk.Frame(root)

main_frame_left = ttk.Frame(root)
main_frame_left_top = ttk.Frame(main_frame_left)
main_frame_left_middle = ttk.Frame(main_frame_left)
main_frame_left_bottom = ttk.Frame(main_frame_left)

main_frame_centre = ttk.Frame(root)
main_frame_centre_top = ttk.Frame(main_frame_centre)
main_frame_centre_results_body = ttk.Frame(main_frame_centre)

main_frame_right = ttk.Frame(root)

# Place main layout (Single fixed menu frame along top, main frame divided into 3 columns L:25%, C:50%, R:25%
menu_banner_frame.place(x = 0,y = 0, relwidth = 1, height = 25)
main_frame_left.place(x = 0,y = 25, relwidth = 0.25, relheight = 1)
main_frame_centre.place(relx = 0.25,y = 25, relwidth = 0.5, relheight = 1)
main_frame_right.place(relx = 0.75,y = 25, relwidth = 0.25, relheight = 1)

ttk.Label(menu_banner_frame, background = 'red').pack(expand = True, fill = 'both')
#ttk.Label(main_frame_left, background = 'green').pack(expand = True, fill = 'both')
#ttk.Label(main_frame_centre, background = 'grey').pack(expand = True, fill = 'both')
#ttk.Label(main_frame_right, background = 'blue').pack(expand = True, fill = 'both')

# Left column frames
main_frame_left_top.place(x = 0,y = 0, relwidth = 1, relheight = 0.1)
main_frame_left_middle.place(x = 0,rely = 0.1, relwidth = 1, relheight = 0.4)
main_frame_left_bottom.place(x = 0,rely = 0.5, relwidth = 1, relheight = 0.5)


# Left grid frames
# Search Widgets
left_menu_search_textEntry = ttk.Entry(main_frame_left_top)
left_menu_search_btn = ttk.Button(main_frame_left_top,text = 'Search')

# Stats widgets
label_total_student_count_title = ttk.Label(main_frame_left_middle,text = 'total_student_count')
label_total_student_count_value = ttk.Label(main_frame_left_middle,text = TOTAL_STUDENT_COUNT)
label_avg_grade_title = ttk.Label(main_frame_left_middle,text = 'avg_grade')
label_avg_grade_value = ttk.Label(main_frame_left_middle,text = str(AVERAGE_GRADE) + "%")
label_avg_attendance_title = ttk.Label(main_frame_left_middle,text = 'avg_attendance')
label_avg_attendance_value = ttk.Label(main_frame_left_middle,text = AVERAGE_ATTENDANCE)
label_total_passes_title = ttk.Label(main_frame_left_middle,text = 'total_passes')
label_total_passes_value = ttk.Label(main_frame_left_middle,text = TOTAL_PASS_COUNT)
label_total_fails_title = ttk.Label(main_frame_left_middle,text = 'total_fails')
label_total_fails_value = ttk.Label(main_frame_left_middle,text = TOTAL_FAIL_COUNT)
label_grades_a_title = ttk.Label(main_frame_left_middle,text = 'grades_a')
label_grades_a_value = ttk.Label(main_frame_left_middle,text = GRADE_A_COUNT)
label_grades_b_title = ttk.Label(main_frame_left_middle,text = 'grades_b')
label_grades_b_value = ttk.Label(main_frame_left_middle,text = GRADE_B_COUNT)
label_grades_c_title = ttk.Label(main_frame_left_middle,text = 'grades_c')
label_grades_c_value = ttk.Label(main_frame_left_middle,text = GRADE_C_COUNT)

# Student Search frame (2 wide 1 deep)
main_frame_left_top.columnconfigure(0, weight =2) # 2/3rds dedicated to text entry field
main_frame_left_top.columnconfigure(1, weight = 1)
main_frame_left_top.rowconfigure(0,weight = 1)

left_menu_search_textEntry.grid(row=0,column=0, sticky = 'ew', padx = 5)
left_menu_search_btn.grid(row=0,column=1)

# Stats Summary frame (2 wide, 7 deep)
main_frame_left_middle.columnconfigure((0,1), weight =1) # Use tuple to save duplicate rows of code
main_frame_left_middle.rowconfigure((0,1,2,3,4,5,6),weight = 1)

label_total_student_count_title.grid(row=0,column=0)
label_total_student_count_value.grid(row=0,column=1)
label_avg_grade_title.grid(row=1,column=0)
label_avg_grade_value.grid(row=1,column=1)
label_avg_attendance_title.grid(row=2,column=0)
label_avg_attendance_value.grid(row=2,column=1)
label_total_fails_title.grid(row=3,column=0)
label_total_fails_value.grid(row=3,column=1)
label_total_passes_title.grid(row=4,column=0)
label_total_passes_value.grid(row=4,column=1)
label_grades_a_title.grid(row=5,column=0)
label_grades_a_value.grid(row=5,column=1)
label_grades_b_title.grid(row=6,column=0)
label_grades_b_value.grid(row=6,column=1)
label_grades_c_title.grid(row=7,column=0)
label_grades_c_value.grid(row=7,column=1)

# Summary charts frame





# Middle frame search results

# Left column frames
main_frame_centre_top.place(x = 0,y = 0, relwidth = 1, relheight = 0.1)
main_frame_centre_results_body.place(x = 0,rely = 0.1, relwidth = 1, relheight = 0.9)


# Centre grid frames
# Search results Widgets
label_total_student_count_title = ttk.Label(main_frame_left_middle,text = 'total_student_count')




# Run UI
root.mainloop()












