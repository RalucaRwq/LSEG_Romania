import sys
import os
import pandas as pd

# Solve ModuleNotFoundError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import module
from developer_experience_engineer_python.data_transformations.job_duration_calculator import read_log_file

# Test that function returns a DataFrame with the expected columns
def test_return_data_frame():
    valid_file_path = r'C:\Users\ciula\PycharmProjects\LSEG_Romania\developer_experience_engineer_python\resources\input\logs.log'

    df = read_log_file(valid_file_path)

    assert isinstance(df, pd.DataFrame), f'Expected pandas DataFrame, but got {type(df)}'

    expected_columns = ['timestamp', 'job_description', 'status', 'PID']

    # Check if the DataFrame contains the expected columns
    assert all(column in df.columns for column in expected_columns), f'Expected columns {expected_columns}, but got {df.columns}'