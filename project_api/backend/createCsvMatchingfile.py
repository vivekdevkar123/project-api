import csv
import requests

# API request (replace with actual API URL)
url = 'http://localhost:5000/match'  # Replace with your endpoint
response = requests.get(url)
data = response.json()

# Reformat matches into mentor-mentee dictionary
mentor_mentees = {}
for match in data['matches']:
    mentor, mentee = match
    if mentor not in mentor_mentees:
        mentor_mentees[mentor] = []
    mentor_mentees[mentor].append(mentee)

# Write to CSV file
with open('mentor_mentee_matches.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Mentor', 'Mentees'])  # Header
    
    for mentor, mentees in mentor_mentees.items():
        writer.writerow([mentor, ', '.join(mentees)])

print("CSV file created successfully!")
