# Contents
### [Program Overview](#program-overview)
### [Program Features](#program-features)
#### [Menu](#menu)
#### [Search](#search)
#### [Stats Summary](#stats-summary)
#### [Results Table](#results-table)
#### [Student Image](#student-image)
#### [Student Summary Table](#student-summary-table)
#### [Student Summary Text](#student-summary-text)
### [Running Program](#running-program)
#### [Prerequisites](#prerequisites)
#### [Installing Python Packages](#installing-python-packages)

## Program Overview
This Python application provides a user interface for interpreting student data from a provided dataset `student_grades.csv` in the program root directory.  
A summary of overall student statistics is provided, in addition, a search feature allows individual students to be identified.

## Program Features
![image](https://github.com/user-attachments/assets/6ed99b46-c9b7-4363-910e-ef99fe8136b4)

### 1. Menu
The 'File' menu provides access to a bar chart. The information displayed is a collation of students by their country of birth and ranked by the top 10 with the highest average grade score.

### 2. Search
The central results table updates dynamically as the user enters a query. Less relevant results are removed when the system is highly confident in the match accuracy (100% fuzzy search match).  
By default, searches are conducted on:
- student_id  
- first_name  
- last_name  
- email  
- country  

Checkbox filters allow users to exclude speciffic columns from the search criteria. For example, searching for 'China' can exclude email to prevent results appearing for:

Student: 959

Email: bghiraldimqm@**china**.com.cn

Country: Philippines


### 3. Stats Summary
The left-hand pane lists an aggregated statistical summary of all imported student results.

### 4. Results Table
Students can be selected by left-clicking the results table. The associated student is displayed in the 'Student Profile' pane. If multiple results are selected using SHIFT + Left Click, only the top result is displayed.

### 5. Student Image
A placeholder image is displayed by default. When a student image is generated, it is saved to the `/StudentPhotos` folder under the student’s ID as a .jpg file.  
To remove student images, delete them from this folder while ensuring `placeholder.jpg` is not removed.

### 6. Generate Student Photo
The dataset does not include student gender. Therefore, an API request is made to `api.genderize.io` using the student’s first name. If gender is not available, "all" is used.  

For example:

ID: 3

Name: Wandis
Is not recognised by the genderize.io api, despite returning a 200 (success) status code the gender field will return 'none' 

A second API request is made to `this-person-does-not-exist.com` with the predicted gender and age bracket. The generated image is saved in the studentPhotos folder previously mentioned.

### 7. Student Summary Table
When selecting a student, their statistics appear in the right-hand pane. If values overflow their row, the application window can be resized for better viewing.

### 8. Student Summary Text
The student’s grade is compared with their country's average grade, displaying the percentage increase or decrease in a text summary.  
Standard percentage calculation was referenced from: [skillsyouneed.com](https://www.skillsyouneed.com/num/percent-change.html).

## Running Program

### Prerequisites
- PyCharm IDE installed  
- Python 3.13 or greater (Download from [python.org](https://www.python.org/downloads/) or Microsoft Store)  
- Obtain program files: Download via Git clone or .zip from GitHub, then open the  
  `DAB410AssignmentPythonWithUIStudentGrades` folder in PyCharm.  
![image](https://github.com/user-attachments/assets/71c1d042-1081-424a-b183-f63895b22d0c)
 

### Installing Python Packages
Packages can be installed in multiple ways:
- Open main.py, hover over missing imports, and use "Install package" from the context menu.
![image](https://github.com/user-attachments/assets/46bd3e73-b7d3-4884-b692-e9e8822101c6)

- OR run the following command for each missing package:
```
pip install package_name
```
## Running Program
Within pycharm the **main.py** module must be selected, then click run from the GUI.
![image](https://github.com/user-attachments/assets/8b204d5a-1cb2-44e8-9121-2cf8499e2d7f)
