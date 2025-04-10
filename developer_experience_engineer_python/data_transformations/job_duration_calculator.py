import pandas as pd
import os

# Read CSV file and add column names
def read_log_file(file_path):
    column_names = ['timestamp', 'job_description', 'status', 'PID']

    # Read the CSV file
    df = pd.read_csv(file_path, header=None, names=column_names)

    # Data cleaning
    df['status'] = df['status'].str.strip()

    # Convert timestamp into a time format
    df['timestamp'] = pd.to_timedelta(df['timestamp'])

    return df

# Measure duration of each job based on START and END
def measure_duration(df):
    # Filter START and END
    starts = df[df['status'] == 'START'][['PID', 'timestamp', 'job_description']].rename(columns={'timestamp': 'start_time'})
    ends = df[df['status'] == 'END'][['PID', 'timestamp']].rename(columns={'timestamp': 'end_time'})

    # Dictionary for storing duration per PID
    durations_dict = {}

    # Measure duration of each active job
    for pid in starts['PID'].unique():
        # Get start time and job_description for this PID
        start_time, job_description = starts[starts['PID'] == pid][['start_time', 'job_description']].iloc[0]

        # Get end time for this PID (if available)
        end_time = ends[ends['PID'] == pid]['end_time'].iloc[0] if not ends[ends['PID'] == pid].empty else None

        # Calculate duration if an END exists, otherwise mark it as empty
        if end_time is not None:
            duration = end_time - start_time
        else:
            duration = None

        # Determine the status based on duration
        status = ''
        if duration is not None:
            # Convert the duration to minutes
            duration_minutes = duration.total_seconds() / 60.0
            if duration_minutes > 10:
                status = 'error'  # Job took longer than 10 minutes
            elif duration_minutes > 5:
                status = 'warning'  # Job took longer than 5 minutes
            # Else mark it as empty

        # Format start_time, end_time and duration to HH:MM:SS
        start_time = str(start_time).split(' ')[-1]
        end_time = str(end_time).split(' ')[-1] if end_time is not None else ''
        duration = str(duration).split(' ')[-1] if end_time != '' else ''

        # Store duration and status in the dictionary
        durations_dict[pid] = {
            'job_description': job_description,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'status': status
        }

    # Create new DataFrame with one row per PID
    result = []
    for pid, times in durations_dict.items():
        result.append([
            pid, times['job_description'], times['start_time'], times['end_time'],
            times['duration'], times['status']
        ])

    result_df = pd.DataFrame(result, columns=['PID', 'job_description', 'start_time', 'end_time', 'duration', 'status'])

    return result_df

# Pass arguments
input_file_path = r'C:\Users\ciula\PycharmProjects\LSEG_Romania\developer_experience_engineer_python\resources\input\logs.log'
input_df = read_log_file(input_file_path)

df_with_durations = measure_duration(input_df)

# Save to CSV output file
output_file_path = r'C:\Users\ciula\PycharmProjects\LSEG_Romania\developer_experience_engineer_python\resources\output\job_duration_report.csv'
df_with_durations.to_csv(output_file_path, index=False)

# Checks
pd.set_option('display.max_rows', None)
print(df_with_durations)
