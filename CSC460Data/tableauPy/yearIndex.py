# Literally just makes a .csvfile
import csv

# Define the filename
filename = "tableauData/years.csv"

# Create and write to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["years"])
    
    # Write the numbers from 1 to 100
    for year in range(1, 101):
        writer.writerow([year])

print(f"CSV file '{filename}' created successfully!")
