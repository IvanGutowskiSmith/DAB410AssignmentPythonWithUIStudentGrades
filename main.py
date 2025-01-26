from re import search
from tkinter.constants import DISABLED, NORMAL

import pandas as pd
import numpy as np # np is alias, not needed but this is best practice
import requests

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from thefuzz import fuzz, process
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

COLUMN_TITLES = tuple(dataFrame.columns) # Dynamically extract column titles from data file

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



def search_student_event(event=None): # Triggered by search; none is required to accept bindings from key release
    value_to_search = left_menu_search_textEntry.get()  # TODO combine into method if not re-used much

    rank_dict = {} # Create dictionary to store similarity %
    highest_accuracy_value = 0

    for indexValue, rows in dataFrame.iterrows():

        key_stats_combined = str(rows["student_id"]) + rows["first_name"] + rows["last_name"]+ rows["email"]+ rows["country"] # Combine key columns into string variable

        similarity_value = fuzz.partial_ratio(value_to_search.lower(),key_stats_combined.lower())

        # Add studentId and similarity % to a dictionary
        rank_dict[str(rows["student_id"])] = similarity_value

        # Record highest accuracy value
        if similarity_value > highest_accuracy_value:
            highest_accuracy_value = similarity_value

    # Reduce results if 100% accuracy results present
    if highest_accuracy_value == 100:
        for stu_id, accuracy in list(rank_dict.items()):  # Have to convert dictionary to list on the fly or error: "dictionary changed size during iteration"
            if accuracy < highest_accuracy_value:
                del rank_dict[stu_id]  # Remove search results below 100% accuracy


    order_search_results = dict(sorted(rank_dict.items(), key=lambda x: x[1], reverse=True)) # Returns ordered dictionary (not allow duplicates) of IDs to display in search results
    students_list_table_update_on_search(order_search_results)






    #print(process.extract(value_to_search, dataFrame["first_name"], limit=5, scorer=fuzz.token_sort_ratio))


####################### UI


# Setup UI
root = tk.Tk()
root.geometry('1280x720') # 16:9 aspect ratio that should fit on most screens
root.minsize(640,360)
root.iconbitmap('favicon.ico')
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
main_frame_right_top = ttk.Frame(main_frame_right)
main_frame_right_middle = ttk.Frame(main_frame_right)
main_frame_right_bottom = ttk.Frame(main_frame_right)

topMenuHeight = 25

# Place main layout (Single fixed menu frame along top, main frame divided into 3 columns L:25%, C:50%, R:25%
menu_banner_frame.place(x = 0,y = 0, relwidth = 1, height = topMenuHeight)
main_frame_left.place(x = 0,y = topMenuHeight, relwidth = 0.2, relheight = 1)
main_frame_centre.place(relx = 0.2,y = topMenuHeight, relwidth = 0.6, relheight = 1)
main_frame_right.place(relx = 0.8,y = topMenuHeight, relwidth = 0.2, relheight = 1)

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
left_menu_search_textEntry.bind("<KeyRelease>", search_student_event)

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
main_frame_left_top.columnconfigure(0, weight =1)
main_frame_left_top.rowconfigure(0,weight = 1)

left_menu_search_textEntry.grid(row=0,column=0, sticky = 'ew', padx = 5)

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


# Setup all students table

table = ttk.Treeview(main_frame_centre, columns=COLUMN_TITLES, show='headings')

# Adjust column widths and alight text to centre
for col in COLUMN_TITLES:
    table.column(col, minwidth=30, width=90, anchor='center')
table.column('student_id',width=60) #Made ID and age columns narrower
table.column('age',width=30)

# Adding column titles to table
for title in COLUMN_TITLES:
    table.heading(title,text = title)
table.pack(expand = True, fill = 'both')



def students_list_table_update_on_search(ordered_dict):
    # Empty table if data present
    for i in table.get_children():
        table.delete(i)

    table_row_number = 1
    for id_to_add_to_table in ordered_dict.keys():
        student_list_table_add_row(id_to_add_to_table,table_row_number)
        table_row_number += 1 # Iterate column id by 1

def student_list_table_add_row(id_to_add, table_position):
    # Student ID and table location are offset by 1 (header row) so have to -1 from student_Id for data row ID

    # This may be verbose, however it allows me to be clear about what data is obtained from where
    student_id = dataFrame.iloc[int(id_to_add)-1,0]
    first_name = dataFrame.iloc[int(id_to_add)-1,1]
    last_name = dataFrame.iloc[int(id_to_add)-1,2]
    age = dataFrame.iloc[int(id_to_add)-1,3]
    email = dataFrame.iloc[int(id_to_add)-1,4]
    country = dataFrame.iloc[int(id_to_add)-1,5]
    attendance = dataFrame.iloc[int(id_to_add)-1,6]
    assignment_completed = dataFrame.iloc[int(id_to_add)-1,7]
    grade = dataFrame.iloc[int(id_to_add)-1,8]

    student_data = (student_id, first_name, last_name, age, email, country, attendance, assignment_completed, grade)
    # Add row to search results table of students
    table.insert(parent='', index=table_position, values=student_data)

def students_list_table_add_all():
    count = 1
    for count,rows in dataFrame.iterrows():
        student_list_table_add_row(rows['student_id'],count)
        count += 1 # Iterate column id by 1

# On startup populate table
students_list_table_add_all()

# TODO add scroll bar, top menu and print student results to right hand side. Possibly edit values or atleast delete student



## Right frame
# Right frame top

def save_image_from_url(student_id, image_url):
    destination_path = 'StudentPhotos\\' + str(student_id) + '.jpg'
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            file.write(response.content)
            print('Ai image downloaded and saved in: ' + destination_path)
    else:
        print('Download ai image failed for URL: '+ image_url)


#Despite button being below student image in UI, we need button to exist in code before student image, so that logic can enable/disable the button
def btn_generate_ai_student_image():
    # Predict gender from name
    predicted_gender = 'male' # Put any gender so program may still work if gender prediction fails

    url = 'https://api.genderize.io?name=' + str(currently_selected_first_name) # Not sure if required but ensured this was a string
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        predicted_gender = data['gender']
        print('Predicted gender for name: ' + currently_selected_first_name)
        print(predicted_gender)
    else:
        print('could not determine gender') # TODO improve error handling
        return

    # Determine age bracket - None of the students are over 25, however logic will remain if required
    age = int(currently_selected_age)

    age_bracket = 'all'
    if age <= 18:
        age_bracket = '12-18'
    elif age <= 25:
        age_bracket = '19-25'
    elif age <= 35:
        age_bracket = '26-35'
    elif age <= 50:
        age_bracket = '35-50' # Request API has error here were it requests boundary of range below (35)
    else:
        age_bracket = '50' # request just states 50

    print('Age bracket: ' + age_bracket)

    # compose URL for ai image request
    url = 'https://this-person-does-not-exist.com/new?time=1737815809253&gender=' + predicted_gender + '&age=' + age_bracket + '&etnic=all'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        ai_image_url = 'https://this-person-does-not-exist.com/img/' + data['name']

        print("Ai image url: " + ai_image_url)
        save_image_from_url(currently_selected_student_id, ai_image_url)
        update_student_image(currently_selected_student_id)
    else:
        print("could not obtain AI image") # TODO improve error handling
        return
    #



generate_student_image_button = ttk.Button(main_frame_right_top, text = 'Generate Ai Image', command = btn_generate_ai_student_image, state=DISABLED)
generate_student_image_button.pack(side = "bottom")



student_image = None
def update_student_image(student_id):
    global student_image
    # Delete prior image if it exists
    if student_image is not None:
        student_image.destroy()
        student_image = None

    # Update student image: if not found add placeholder image and 'enable AI image' button
    try:
        image_original = Image.open('StudentPhotos\\' + str(student_id) + '.jpg').resize((200, 200))  # Double brackets is the size property, source Ai generated images are 1024x1024  1:1
        generate_student_image_button.config(state=DISABLED)
    except:
        print("could not find image, using placeholder")
        image_original = Image.open('StudentPhotos\\placeholder.jpg').resize((200, 200))
        generate_student_image_button.config(state=NORMAL)
    image_tk = ImageTk.PhotoImage(image_original)
    student_image = ttk.Label(main_frame_right_top, image=image_tk)
    student_image.image = image_tk  # Save a reference to prevent garbage collection
    student_image.pack(expand=True, fill='both', padx = 20, pady = 20)








# Right frame middle

studentSummaryTable = ttk.Treeview(main_frame_right_middle, columns=('col1','col2'),show='headings')

# Variables for currently selected student
currently_selected_student_id = ''
currently_selected_first_name = ''
currently_selected_age = ''


# Table row selection event
def clicked_student_update_summary_table(_): # Underscore means we do not care abut the value
    global currently_selected_student_id
    global currently_selected_first_name
    global currently_selected_age
    # Obtain selected item from main search results table
    selected_item_row_id = table.selection()

    # As main search results change / are deleted, skip student summary table from updating if entries are deleted (avoid out of range errors)
    if not selected_item_row_id or selected_item_row_id[0] not in table.get_children():
        return  # Exit with no changes made

    row_data = table.item(selected_item_row_id[0])['values'] # Select only first tuple ID if multiple are selected with shift + click
    print(row_data) # Print selected student data to console

    # Empty studentSummaryTable if values present. Without this new data only added to top of table, with prior results collated below
    for item in studentSummaryTable.get_children():
        studentSummaryTable.delete(item)

    count = 0
    for row in row_data:
        studentSummaryTable.insert(parent='', index=[count], values=(COLUMN_TITLES[count], row_data[count]))
        # Update global variables for 'selected student'
        match COLUMN_TITLES[count]:
            case 'student_id':
                currently_selected_student_id = row_data[count]
            case 'first_name':
                currently_selected_first_name = row_data[count]
            case 'age':
                currently_selected_age = row_data[count]
        count = count + 1

    update_student_image(str(row_data[0]))



table.bind('<<TreeviewSelect>>', clicked_student_update_summary_table)

studentSummaryTable.column(0,minwidth=30, width=90, anchor='w') # Adjust table column size and place
studentSummaryTable.pack()

# Student image

#Right Frame UI
main_frame_right_top.place(x = 0,rely = 0, relwidth = 1, relheight = 0.33)
main_frame_right_middle.place(x = 0,rely = 0.33, relwidth = 1, relheight = 0.33)
main_frame_right_bottom.place(x = 0,rely = 0.66, relwidth = 1, relheight = 0.33)

#ttk.Label(main_frame_right_top, background = 'blue').pack(expand = True, fill = 'both')
#ttk.Label(main_frame_right_middle, background = 'green').pack(expand = True, fill = 'both')
#ttk.Label(main_frame_right_bottom, background = 'orange').pack(expand = True, fill = 'both')





# Run UI
root.mainloop()












