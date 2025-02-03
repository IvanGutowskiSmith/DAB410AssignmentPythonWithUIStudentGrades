import pandas as pd
from statistics import * # Import all the functions used by the main program

# Run all unit tests: Right click empty space in this file, select 'run python tests'

# Mock data frame for simplified test results, ensured that mock data evaluates the boundaries of most function outputs
mocked_data_frame = pd.DataFrame({
    "country": ["Slovenia", "Poland", "Poland"],
    "attendance": [20.22, 50.55, 60.66],
    "grade": [50.55, 65.55, 75.55]
})

# Each output is manually calculated, and placed as the answer. These unit tests then validate the code's calculations
# against the manually verified result

def test_average_attendance():
    assert average_attendance(mocked_data_frame) == 43.81 # Manually calculated

def test_average_grade():
    assert average_grade(mocked_data_frame) == 63.88 # Manually calculated to 63.883 reoccurring

def test_total_pass_fail_count():
    assert total_pass_fail_count(mocked_data_frame) == (3,0) # (Passes,Fails) Above 40 is a pass so all are above that

def test_grade_boundaries_count():
    assert grade_boundaries_count(mocked_data_frame) == (1,1,1) # Returned values: (A's, B's, C's) | Boundaries are: 50 to 60 is C | 60 to 70 is B | 70+ is A | Test data has 1 value per grade boundary

def test_average_country_grade():
    assert average_country_grade(mocked_data_frame) == {'Poland': 70.55, 'Slovenia': 50.55} # Poland present twice so average of those two grades, Slovenia once so just that grade