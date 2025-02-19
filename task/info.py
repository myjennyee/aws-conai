import pandas as pd

# Load the CSV file
file_path = r'C:\Users\sooji\Downloads\task\Wyzrs_WZT AI Development.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print("First few rows of the dataframe:")
print(data.head())

# Count the occurrences of each name in the 'Assignee' column
assignee_counts = data['Assignee'].value_counts()
# Display the counts
print("\nCounts of each Assignee:")
print(assignee_counts)

# Get basic information about the dataframe
print("\nDataframe Info:")
print(data.info())

# Check for missing values
print("\nMissing Values in Each Column:")
print(data.isnull().sum())

# Describe the data for basic statistical information
print("\nStatistical Description of Numeric Columns:")
print(data.describe())

# Task status distribution
status_counts = data['Status'].value_counts()
print("\nTask Status Distribution:")
print(status_counts)

# Total time spent on tasks
total_time_spent = data['Time Spent(m)'].sum()
print(f"\nTotal time spent on tasks: {total_time_spent} minutes")

# Average time spent per task
average_time_spent = data['Time Spent(m)'].mean()
print(f"Average time spent per task: {average_time_spent:.2f} minutes")

# Group by assignee and calculate total time spent
time_spent_by_assignee = data.groupby('Assignee')['Time Spent(m)'].sum()
print("\nTime Spent by Assignee:")
print(time_spent_by_assignee)

# Group by project and status to see the number of tasks in each status per project
project_status_counts = data.groupby(['Project', 'Status']).size().unstack(fill_value=0)
print("\nNumber of Tasks in Each Status per Project:")
print(project_status_counts) 
