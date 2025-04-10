import sys
import os
import pandas as pd

# Solve ModuleNotFoundError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import module
from developer_experience_engineer_python.data_transformations.job_duration_calculator import read_log_file, measure_duration

# Test that duration is correctly calculated
def test_duration_calculator():
    # Sample data
    log_data = """
    11:40:51,scheduled task 996,START,90962
    11:42:46,scheduled task 996,END,90962
    12:00:00,scheduled task 1001,START,90963
    """

    test_file_path = r'C:\Users\ciula\PycharmProjects\LSEG_Romania\developer_experience_engineer_python\resources\input\test_logs.log'
    output_file_path = r'C:\Users\ciula\PycharmProjects\LSEG_Romania\developer_experience_engineer_python\resources\output\test_output.csv'

    with open(test_file_path, 'w') as f:
        f.write(log_data)

    # Read test log file and calculate duration
    df = read_log_file(test_file_path)
    df_with_durations = measure_duration(df)

    # Save the result to CSV and read it
    df_with_durations.to_csv(output_file_path, index=False)
    output_df = pd.read_csv(output_file_path)

    # Convert duration column to Timedelta to ensure correct comparison
    output_df['duration'] = pd.to_timedelta(output_df['duration'])

    # Check duration for job with START and END -> PID 90962
    job_996 = output_df[output_df['PID'] == 90962]
    assert job_996['duration'].iloc[0] == pd.Timedelta('0 days 00:01:55'), "The duration for job 996 is incorrect"

    # Check duration for job with START but no END -> PID 90963
    job_1001 = output_df[output_df['PID'] == 90963]
    assert pd.isnull(job_1001['duration'].iloc[0]), f"The duration for job 1001 should be NaN, but got: {job_1001['duration'].iloc[0]}"

    # Clean up test files
    os.remove(test_file_path)
    os.remove(output_file_path)