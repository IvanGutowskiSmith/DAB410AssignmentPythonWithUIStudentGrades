import numpy as np

# Grade boundaries
grade_pass_boundary = 40 # >= 40 is a pass
grade_a_minimum = 70 # greater than or eq to
grade_b_minimum = 60 # eq or greater than 60, less than 70
grade_c_minimum = 50

def average_attendance(data_frame):
    return round(data_frame["attendance"].mean(),2) # Using numpy's built in mean average to calculate result, rounded

def average_grade(data_frame):
    return round(data_frame["grade"].mean(),2)

def total_pass_fail_count(data_frame):
    # Count pass / fails
    total_pass_count = int() # Declare empty variable, 'none' would cause error, considered using zero however, may hide errors as program could produce false positives
    total_fail_count = int()

    for index,row in data_frame.iterrows():
        if row['grade'] >= grade_pass_boundary:
            total_pass_count += 1
        else:
            total_fail_count += 1

    return total_pass_count, total_fail_count # Return both as tuple

# Calculating grade count A,B,C
def grade_boundaries_count(data_frame):
    df = data_frame["grade"]
    a_trues = (df >= grade_a_minimum) # Could validate upper limit, however known presumptions are that grades cannot exceed 100%, which would again highest grade anyway
    b_trues = (df >= grade_b_minimum) & (df < grade_a_minimum) # Greater or eq 60, less than 70
    c_trues = (df >= grade_c_minimum) & (df < grade_b_minimum) # Greater or eq 50, less than 60

    grade_a_count = np.count_nonzero(a_trues)
    grade_b_count = np.count_nonzero(b_trues)
    grade_c_count = np.count_nonzero(c_trues)

    return grade_a_count,grade_b_count,grade_c_count

def average_country_grade(data_frame):
    return data_frame.groupby('country')['grade'].mean().to_dict()
