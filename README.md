# Contents
### Program Overview
### Program features
### Running the application
#### Prerequisites
### Troubleshooting issues




## Program overview

This Python application provides a user interface for interpreting student data from a provided dataset.
A summary of overall student statistics is provided, in addition a search feature allows individual students to be identified


Program features

Menu:
The 'file' menu provides access to a bar chart. The information displayed is a collation of students by their country of birth
and ranked by the top 10 with the highest average grade score.

Search: 
The central results table is updated with relevant results as the user enters a search query, where the system is
highly confident in the match accuracy less relevant results will be removed.
By default, search is conducted on: 
 - student_id
 - first_name
 - last_name
 - email
 - country

Checkbox filters below the search box allow the user to exclude search columns from the query parameters. When searching
for 'China', email can be excluded from search to ensure that addresses containing that country are not included.
e.g. 
Student: 959
email: bghiraldimqm@china.com.cn
Country: Philippines

Stats summary:
The left hand pane list an aggregated summary of all imported student results

Results table:
Students can be selected by left-clicking the results table, the associated student will be presented on the right hand
'student profile' pane. Where multiple results are selected using SHIFT + Left Click - only the top result will be displayed

Student image:
By default a placeholder image will be present, where an image is generated the file is saved in the /StudentPhotos folder
of the program root directory. Images are saved under the student's ID, in the .jpg format.
To remove student images, they can be deleted from this folder - Ensuring that 'placeholder.jpg' remains.

Generate student photo
The supplied dataset does not provide student gender; therefore an API request is made to 'api.genderize.io' using the student's
first name, where a predicted gender is not available 'all' is used. An example is:
id: 3
name: Wandis
A further API request is made to this-person-does-not-exist.com with the associated gender and age bracket, saved to the 
aforementioned file location.

Student summary table
When selecting a student, their associated statistics are displayed on the right hand pane. Where lengthy values overflow 
their respective row, the user can expand the application window to fit their viewing requirements.

Student summary text
The selected student's grade is compared with the average grade for their country, the percentage increase of decrease is
displayed for the respective student. Whilst percentage calculations are standard, the following resource was utilised 
for the calculation logic: https://www.skillsyouneed.com/num/percent-change.html

## Running program
# Prerequisites



Troubleshooting





-- Required modules: / Prerequisites

-- Latest python interpreter from Python.org or Windows store (Install this first as packages seem to need re-installing after version update)
-- Pandas python package via pycharm, select latest version
-- numpy also could mention to install via pip install
pillow for images ?
-- addon, theFuzz for search, requests for API, matplot lib
-- import tkinter, however no install required as it's part of core Python stack
-- need git

can just hover over import and select 'install all missing packages'

-- need python3 interpreter downloaded and installed, restart pycharm after install
-- Add pythern interpreter, add existing.


MUST have file 'main.py' selected when pressing 'run', troubleshoot?