from tkinter.constants import DISABLED, NORMAL
import pandas as pd # pd is alias, not needed but this is best practice
import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from thefuzz import fuzz, process # For search result comparison
from matplotlib import pyplot as plt # Generate table
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import statistics # Import pre-calculated statistics from statistics.py


# Import file
data_frame = pd.read_csv('student_grades.csv')
pd.set_option('display.width', 400) # Used more for initial debugging, ensures all rows and columns are displayed when data_frame rows are printed to console
pd.set_option('display.max_columns', None)

# ====================================================
# Global Variables
# ====================================================

total_student_count = len(data_frame) # Populate total student count on application start
column_titles = tuple(data_frame.columns) # Dynamically extract column titles from data file

# Obtain pre-calculated statistics from statistics.py
average_attendance = statistics.average_attendance(data_frame)
average_grade = statistics.average_grade(data_frame)
total_pass_count = statistics.total_pass_fail_count(data_frame)[0] # 0 Gets first returned value
total_fail_count = statistics.total_pass_fail_count(data_frame)[1] # second returned value is fail count
grade_a_count = statistics.grade_boundaries_count(data_frame)[0] # Returns first item which is a count
grade_b_count = statistics.grade_boundaries_count(data_frame)[1]
grade_c_count = statistics.grade_boundaries_count(data_frame)[2]
average_grade_per_country = statistics.average_grade(data_frame)


# ====================================================
# Button Functions
# Some logic functions are defined first as they are used later in code for the user interface buttons, however other functions that require UI placement are defined once the UI is created,
# functions are ordered by UI placement, starting top left
# ====================================================

# Navigation menu dropdown
def navigation_drop_down_clicked(_):
    if drop_down.get() == menu_options[0]: # First option: graph
        avg_grade_bar_chart_new_window() # Load 'Top 10 countries' graph
        drop_down.set("File") # Re-set dropdown back to 'file' to make it look like a menu :)
    elif drop_down.get() == menu_options[1]: # Exit option
        exit(1)

# Load bar chart in new window: - UI was too crowded for a graph in remaining space
def avg_grade_bar_chart_new_window():
    new_window = tk.Toplevel(root) # Creating new window for bar chart
    new_window.minsize(640, 480)
    new_window.iconbitmap('favicon.ico')

    # Creating bar chart
    fig, ax = plt.subplots()
    bar_chart_canvas = FigureCanvasTkAgg(fig,master = new_window)
    bar_chart_canvas.get_tk_widget().pack()
    # Bar chart
    plt.style.use('fivethirtyeight')
    # Order by highest grade, seems to make a list of tuples which is hard to process
    l = dict(sorted(average_grade_per_country.items(),key=lambda x:x[1], reverse=True))

    # Due to the vast number of countries present, results would not easily display on a single bar chart. So have decided to list the top 10 countries by grade.
    # This requires ordering dictionary by grade, then selecting the top 10. Deleting (shrinking) dictionary whilst iterating caused errors and possible risk of IDs changing,
    #  so ordered by grade, then added top 10 to a new dictionary
    top_10_countries = {} # New empty dictionary
    count = 0
    for x,y in l.items():
        if count < 10:
            top_10_countries[x]=y
        count += 1

    countries_x = top_10_countries.keys()
    grades_y = top_10_countries.values()

    # Configuring chart
    plt.bar(countries_x,grades_y, color = 'LightBlue', label='Grade')
    plt.title('Top 10 countries by average grade')
    plt.xlabel('Country')
    plt.ylabel('Grade')

    plt.xticks(rotation=20) # Slanting country names on bottom axis for improved readability
    plt.tight_layout()
    bar_chart_canvas.draw()


def search_student_event(event=None): # Triggered by search; 'none' is required to accept bindings from key release
    value_to_search = left_menu_search_textEntry.get()  # Although used once, keeping the search result visible helps future debugging

    rank_dict = {} # Create dictionary to store search similarity %
    highest_accuracy_value = 0 # Initialising variable, running total of highest score as results are iterated through

    # Search is conducted on the values of specific columns, combining values of all columns into a single string for each row, which is then iteratively compared against user's search text
    for indexValue, rows in data_frame.iterrows():
        key_stats_combined = str(rows["student_id"]) + rows["first_name"] + rows["last_name"] # Concatenate key column values into string variable

        # Use checkboxes to determine if email and country are included in search scope, checked (1) by default, user can uncheck (0)
        if filter_email_state.get() == 1: # Include eMail in search query
            key_stats_combined = key_stats_combined + rows["email"] # Append email to search string
        if filter_country_state.get() == 1: # Include country in search query
            key_stats_combined = key_stats_combined + rows["country"]

        similarity_value = fuzz.partial_ratio(value_to_search.lower(),key_stats_combined.lower()) # Use fuzz to score similarity between search term and row value(s)

        # Add studentId and similarity % to a dictionary
        rank_dict[str(rows["student_id"])] = similarity_value

        # Record highest accuracy value
        if similarity_value > highest_accuracy_value:
            highest_accuracy_value = similarity_value

    # Reduce results if search items with 100% accuracy present
    if highest_accuracy_value == 100:
        for stu_id, accuracy in list(rank_dict.items()):  # Have to convert dictionary to list or error: "dictionary changed size during iteration"
            if accuracy < highest_accuracy_value:
                del rank_dict[stu_id]  # Remove any search results below 100% accuracy

    order_search_results = dict(sorted(rank_dict.items(), key=lambda x: x[1], reverse=True)) # Returns ordered dictionary of IDs to display in search results
    students_list_table_update_on_search(order_search_results)




# ====================================================
# User Interface
# ====================================================

root = tk.Tk()
root.geometry('1280x720') # 16:9 aspect ratio that should fit on most screens
root.minsize(1024,576)
root.iconbitmap('favicon.ico') # System tray icon
root.title('Student Grade Manager. Student ID: 2310700') # Window title
# Could define a style, however little improvement over default

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
# Place main layout (Single fixed menu frame along top, main frame divided into 3 columns L:20%, C:60%, R:20%
menu_banner_frame.place(x = 0,y = 0, relwidth = 1, height = topMenuHeight)
main_frame_left.place(x = 0,y = topMenuHeight, relwidth = 0.2, relheight = 1)
main_frame_centre.place(relx = 0.2,y = topMenuHeight, relwidth = 0.6, relheight = 1)
main_frame_right.place(relx = 0.8,y = topMenuHeight, relwidth = 0.2, relheight = 1)

# Left column frames
main_frame_left_top.place(x = 0,y = 0, relwidth = 1, relheight = 0.2)
main_frame_left_middle.place(x = 0,rely = 0.2, relwidth = 1, relheight = 0.6)
main_frame_left_bottom.place(x = 0,rely = 0.8, relwidth = 1, relheight = 0.1)

# Navigation menu
menu_options = ["Top performing countries graph","Exit"]
drop_down = ttk.Combobox(menu_banner_frame, values = menu_options, state="readonly")
drop_down.set("File")
drop_down.pack(padx = 5,side = tk.LEFT)
drop_down.bind("<<ComboboxSelected>>", navigation_drop_down_clicked)


# Left grid frames
# Search Widgets

# Pre-tick search checkboxes
filter_email_state = tk.IntVar(value=1)
filter_country_state = tk.IntVar(value=1)

left_menu_search_Label = ttk.Label(main_frame_left_top, text= 'Search by ID, name(s) email and country')
left_menu_search_textEntry = ttk.Entry(main_frame_left_top)
left_menu_search_textEntry.bind("<KeyRelease>", search_student_event)
left_menu_search_filter_title = ttk.Label(main_frame_left_top, text= 'Include in search:')
left_menu_search_filter_email = tk.Checkbutton(main_frame_left_top, text='Email',variable = filter_email_state,onvalue=1, offvalue=0, command=search_student_event)
left_menu_search_filter_country = tk.Checkbutton(main_frame_left_top, text='Country',variable = filter_country_state,onvalue=1, offvalue=0, command=search_student_event)

# Stats widgets
label_total_student_count_title = ttk.Label(main_frame_left_middle,text = 'total_student_count')
label_total_student_count_value = ttk.Label(main_frame_left_middle, text = total_student_count)
label_avg_grade_title = ttk.Label(main_frame_left_middle,text = 'avg_grade')
label_avg_grade_value = ttk.Label(main_frame_left_middle, text =str(average_grade) + "%")
label_avg_attendance_title = ttk.Label(main_frame_left_middle,text = 'avg_attendance')
label_avg_attendance_value = ttk.Label(main_frame_left_middle, text = average_attendance)
label_total_passes_title = ttk.Label(main_frame_left_middle,text = 'total_passes')
label_total_passes_value = ttk.Label(main_frame_left_middle, text = total_pass_count)
label_total_fails_title = ttk.Label(main_frame_left_middle,text = 'total_fails')
label_total_fails_value = ttk.Label(main_frame_left_middle, text = total_fail_count)
label_grades_a_title = ttk.Label(main_frame_left_middle,text = 'grades_a')
label_grades_a_value = ttk.Label(main_frame_left_middle, text = grade_a_count)
label_grades_b_title = ttk.Label(main_frame_left_middle,text = 'grades_b')
label_grades_b_value = ttk.Label(main_frame_left_middle, text = grade_b_count)
label_grades_c_title = ttk.Label(main_frame_left_middle,text = 'grades_c')
label_grades_c_value = ttk.Label(main_frame_left_middle, text = grade_c_count)

# Left student Search frame
main_frame_left_top.columnconfigure(0, weight =1)
main_frame_left_top.rowconfigure(0,weight = 1)

left_menu_search_Label.grid(row=0,column=0, sticky = 'ew', padx = 5)
left_menu_search_textEntry.grid(row=1,column=0, sticky = 'ew', padx = 5)
left_menu_search_filter_title.grid(row=2,column=0, sticky = 'w', padx = 5, pady =5 )
left_menu_search_filter_email.grid(row=3,column=0, sticky = 'w', padx = 5)
left_menu_search_filter_country.grid(row=4,column=0, sticky = 'w', padx = 5)

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

# Setup default UI state
left_menu_search_textEntry.focus() # As no 'search' button is present, pre-focus search text entry for user to conduct search whilst typing

# ====================================================
# Functions continued
# ====================================================

# Students list table is the central display for all or searched students
# Setup 'all students' table
table = ttk.Treeview(main_frame_centre, columns=column_titles, show='headings')

# Adjust column widths and alight text to centre
for col in column_titles:
    table.column(col, minwidth=30, width=90, anchor='center')
table.column('student_id',width=60) #Made ID and age columns narrower
table.column('age',width=30)

# Adding column titles to table
for title in column_titles:
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
    student_id = data_frame.iloc[int(id_to_add) - 1,0]
    first_name = data_frame.iloc[int(id_to_add) - 1,1]
    last_name = data_frame.iloc[int(id_to_add) - 1,2]
    age = data_frame.iloc[int(id_to_add) - 1,3]
    email = data_frame.iloc[int(id_to_add) - 1,4]
    country = data_frame.iloc[int(id_to_add) - 1,5]
    attendance = data_frame.iloc[int(id_to_add) - 1,6]
    assignment_completed = data_frame.iloc[int(id_to_add) - 1,7]
    grade = data_frame.iloc[int(id_to_add) - 1,8]

    student_data = (student_id, first_name, last_name, age, email, country, attendance, assignment_completed, grade)
    # Add row to search results table of students
    table.insert(parent='', index=table_position, values=student_data)

def students_list_table_add_all():
    count = 1
    for count,rows in data_frame.iterrows():
        student_list_table_add_row(rows['student_id'],count)
        count += 1 # Iterate column id by 1

# On startup populate table
students_list_table_add_all()


## Right frame
# Right top frame

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

    try:
        url = 'https://api.genderize.io?name=' + str(currently_selected_first_name)  # Not sure if required but ensured this was a string
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            predicted_gender = data['gender']
            print('Predicted gender for name: ' + currently_selected_first_name)
            print(predicted_gender)
        else:
            print('could not get response from gender API') # TODO improve error handling
            return

        if predicted_gender is None: # e.g. Student 3 'Wanids' fails gender prediction
            predicted_gender = 'all'
            print('Gender not determined, defaulting to any')
    except requests.exceptions.RequestException as e:
        print("Error etching gender data"+ str(e))

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
    url = 'https://this-person-does-not-exist.com/new?time=1737815809253&gender=' + str(predicted_gender) + '&age=' + age_bracket + '&etnic=all'
    print('Request image using parameters: ' + url)
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



generate_student_image_button = ttk.Button(main_frame_right_top, text = 'Generate student photo', command = btn_generate_ai_student_image, state=DISABLED)
generate_student_image_button.pack(side = "bottom", pady = 5)



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
currently_selected_student_id = 0
currently_selected_first_name = ''
currently_selected_age = 0
currently_selected_country = ''
currently_selected_grade = 0
average_grade_per_country = statistics.average_country_grade(data_frame) # Empty dictionary


def student_performance_summary_text_update():
    global performance_summary
    new = float(currently_selected_grade) # Student grade
    original = float(average_grade_per_country[currently_selected_country]) # Average grade for their country

    # Calculate student grade vs their country average. Used: https://www.skillsyouneed.com/num/percent-change.html
    # New number - Original number
    difference = new - original
    # Divide increase by original number then x 100 | Negative = percentage decrease
    percent_difference = ( difference / original ) * 100
    percent_difference = round(percent_difference,2) # Rounded on this line as the ',2' for rounding makes the calculation above confusing to read
    print(percent_difference)

    # Delete existing summary
    performance_summary.destroy()

    if percent_difference >= 0: # Considering 0 positive
        print("positive")
        performance_summary = ttk.Label(main_frame_right_bottom, text=currently_selected_first_name + " has a test grade "+ str(percent_difference) + '% higher than the average for their home country of '+currently_selected_country, foreground='Green', wraplength = 250)
    else:
        print("negative")
        performance_summary = ttk.Label(main_frame_right_bottom, text=currently_selected_first_name + " has a test grade "+ str(percent_difference) + '% below the average for their home country of '+currently_selected_country, foreground='DarkRed',  wraplength = 250)

    # Place updated summary label
    performance_summary.config(justify="center",font=('Helvetica bold', 12)) # Justify centre reduces variation in text movement between student selection
    performance_summary.pack()


# Table row selection event
def clicked_student_update_summary_table(_): # Underscore means we do not care abut the value
    global currently_selected_student_id
    global currently_selected_first_name
    global currently_selected_age
    global currently_selected_country
    global currently_selected_grade

    selected_item_row_id = table.selection() # Obtain selected item from main search results table

    # As main search results change / are deleted, skip student summary table from updating if entries are deleted (avoid out of range errors)
    if not selected_item_row_id or selected_item_row_id[0] not in table.get_children():
        return  # Exit with no changes made

    row_data = table.item(selected_item_row_id[0])['values'] # Select only first tuple ID if multiple are selected with shift + click

    # Empty studentSummaryTable if values present. Without this new data only added to top of table, with prior results collated below
    for item in studentSummaryTable.get_children():
        studentSummaryTable.delete(item)

    #Populate student summary table and save key values to global variables
    count = 0
    for row in row_data:
        studentSummaryTable.insert(parent='', index=[count], values=(column_titles[count], row_data[count]))
        match column_titles[count]:
            case 'student_id':
                currently_selected_student_id = row_data[count]
            case 'first_name':
                currently_selected_first_name = row_data[count]
            case 'age':
                currently_selected_age = row_data[count]
            case 'country':
                currently_selected_country = row_data[count]
            case 'grade':
                currently_selected_grade = row_data[count]
        count = count + 1

    update_student_image(str(currently_selected_student_id))
    student_performance_summary_text_update()


table.bind('<<TreeviewSelect>>', clicked_student_update_summary_table)

studentSummaryTable.column(0,minwidth=30, width=90, anchor='w') # Adjust table column size and place
studentSummaryTable.pack()

# Student image

#Right Frame UI
main_frame_right_top.place(x = 0,rely = 0, relwidth = 1, relheight = 0.33)
main_frame_right_middle.place(x = 0,rely = 0.33, relwidth = 1, relheight = 0.33)
main_frame_right_bottom.place(x = 0,rely = 0.66, relwidth = 1, relheight = 0.33)


performance_summary = ttk.Label(main_frame_right_bottom, text='Select student ...',  foreground='Grey')
performance_summary.pack()

# Run UI
root.mainloop()












