import csv
import re
import os

# Path to the input journal file
journal_file_path = r'C:\Users\sooji\Downloads\Revit\journal.0062.txt'
# Path to the output CSV file
output_csv_path = r'C:\Users\sooji\Downloads\Revit\chunked_journal.csv'

# Regular expression pattern to match lines starting with ' and a letter
pattern = re.compile(r"^\s*'?\s*([CEAH]) ")

# Function to write all chunks to the CSV file
def write_chunks(chunks):
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Entries'])
        for category, entries in chunks:
            writer.writerow([category] + ['\n'.join(entries)])

# Read the journal file and chunk the data
chunks = []
current_category = None
current_entries = []

with open(journal_file_path, 'r') as file:
    for line in file:
        match = pattern.match(line)
        if match:
            # If a new category is found, finalize the current chunk (if any)
            if current_category is not None:
                chunks.append((current_category, current_entries))
            # Start a new chunk for the current category
            current_category = match.group(1)
            current_entries = [line.strip()]
        elif line.startswith("' 0:"):
            # Handle lines starting with "' 0:" separately
            if current_category is not None:
                chunks.append((current_category, current_entries))
            current_category = "Other0"
            current_entries = [line.strip()]
        else:
            # Continue adding lines to the current chunk
            if current_category is not None:
                current_entries.append(line.strip())

# Add the last chunk to the list
if current_category is not None:
    chunks.append((current_category, current_entries))

# Write all chunks to the CSV file
write_chunks(chunks)

print(f"Journal entries have been chunked and written to {output_csv_path}")
