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
root.configure(background='brown') # May remove later, here as it may show gaps in frames
root.title('Student Grade Manager. Student ID: 2310700')
appFont = 'Calibri'

#style=ttk.Style(root)
#style.theme_use('vista') # Revisit, no styles that looked better than default

# Main layout widgets
menu_banner_frame = ttk.Frame(root)

main_frame_left = ttk.Frame(root)
main_frame_left_top = ttk.Frame(main_frame_left)
main_frame_left_middle = ttk.Frame(main_frame_left)
main_frame_left_bottom = ttk.Frame(main_frame_left)

main_frame_centre = ttk.Frame(root)

main_frame_right = ttk.Frame(root)

# Place main layout (Single fixed menu frame along top, main frame divided into 3 columns L:25%, C:50%, R:25%
menu_banner_frame.place(x = 0,y = 0, relwidth = 1, height = 25)
main_frame_left.place(x = 0,y = 25, relwidth = 0.2, relheight = 1)
main_frame_centre.place(relx = 0.2,y = 25, relwidth = 0.6, relheight = 1)
main_frame_right.place(relx = 0.8,y = 25, relwidth = 0.2, relheight = 1)

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

# Left student Search frame (2 wide 1 deep)
main_frame_left_top.columnconfigure(0, weight =2) # 2/3rds dedicated to text entry field
main_frame_left_top.columnconfigure(1, weight = 1)
main_frame_left_top.rowconfigure(0,weight = 1)

left_menu_search_textEntry.grid(row=0,column=0, sticky = 'ew', padx = 5)
left_menu_search_btn.grid(row=0,column=1)

# Left stats Summary frame (2 wide, 7 deep)
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

# Left summary charts frame

# Placeholder colour to show area this frame covers
ttk.Label(main_frame_left_bottom, background = 'lightBlue').pack(expand = True, fill = 'both')





# Middle search results frame
#ttk.Label(main_frame_centre, background = 'orange').pack(expand = True, fill = 'both')

# TODO Possibly have columns created dynamically from the data file, may avoid errors this way if a column name is edited, order changed or removed

columns = ('studentId', 'firstName', 'lastName', 'age', 'email', 'country', 'attendance', 'assignmentCompleted', 'grade')
table = ttk.Treeview(main_frame_centre, columns=columns, show='headings')

# Adjust column widths and alight text to centre
for col in columns:
    table.column(col, minwidth=30, width=90, anchor='center')
table.column('studentId',width=30) #Made ID and age columns narrower
table.column('age',width=30)

# Adding column titles to table
table.heading('studentId',text = 'Id')
table.heading('firstName',text = 'First Name')
table.heading('lastName',text = 'Last Name')
table.heading('age',text = 'Age')
table.heading('email',text = 'Email')
table.heading('country',text = 'Country')
table.heading('attendance',text = 'Attendance %')
table.heading('assignmentCompleted',text = 'Assignment Completed?')
table.heading('grade',text = 'Grade')
table.pack(expand = True, fill = 'both')

# Add values into Treeview table
for index,row in dataFrame.iterrows():
    student_id = row['student_id']
    first_name = row['first_name']
    last_name = row['last_name']
    age = row['age']
    email = row['email']
    country = row['country']
    attendance = row['attendance']
    assignmentCompleted = row['assignment_completed']
    grade = row['grade']

    studentData = (student_id,first_name,last_name,age,email,country,attendance,assignmentCompleted,grade)
    table.insert(parent = '', index = student_id, values = studentData) # Using student ID as the row index as it keeps order logical and value is unique

# Table selection event
def clicked_item(_): # Underscore means we do not care abut the value
    row_ids = table.selection()
    print(row_ids[0]) # Select only first tuple ID if multiple are selected with shift + click
    print(table.item(row_ids[0])['values']) # Print data from row to console
table.bind('<<TreeviewSelect>>',clicked_item)


# TODO add scroll bar, top menu and print student results to right hand side. Possibly edit values or atleast delete student




#table.insert(parent = '',index = 0,values = ('118','Bob','Bobbins','22','bob@email.com','England','98','True','56')) # Parent is empty string as there are no sub items, the table starts with '' as the default parent


# Right frame



# Run UI
root.mainloop()












