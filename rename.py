import os
import re

# Specify the directory path
directory = r'C:\Users\LGGRam\Desktop\august24\SSBacktest\data\binance\ETHUSDT'

# Iterate through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV and matches the MMDD pattern
    if filename.endswith('.csv') and re.match(r'\d{4}\.csv', filename):
        # Create the new filename
        new_filename = '2024' + filename
        
        # Construct full file paths
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} to {new_filename}')

print("Renaming complete.")