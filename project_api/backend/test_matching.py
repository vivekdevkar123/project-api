from flask import Flask, jsonify
import requests
from collections import defaultdict
from itertools import cycle

app = Flask(__name__)

# API URL for fetching student data
LIST_PARTICIPANTS_API = 'http://127.0.0.1:8000/api/mentor_mentee/list_participants/'

def get_students_data():
    """Fetch student data from the external API."""
    try:
        response = requests.get(LIST_PARTICIPANTS_API)
        response.raise_for_status()  # Raise an error for bad responses
        students = response.json()
        return students
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []  # Return an empty list in case of error

def evaluate_student(student):
    """Score students dynamically based on their achievements."""
    score = 0
    
    # Higher semester students get preference for being mentors
    if int(student['semester']) >= 5:
        score += (int(student['semester']) - 4) * 10
    
    # Previous mentoring experience
    if student['previous_mentoring_experience']:
        score += 10

    # Score based on hackathon participation
    if student['hackathon_participation'] == 'National':
        score += 15 + int(student['number_of_wins']) * 5  # Wins add more points
    elif student['hackathon_participation'] == 'International':
        score += 20 + int(student['number_of_wins']) * 10

    # Score for coding competitions
    if student['coding_competitions_participate'] == 'yes':
        score += 15 + int(student['number_of_coding_competitions']) * 5  # Add points for each competition

    # Add CGPA/SGPA to the score (scaled to 10 points)
    score += float(student['cgpa']) * 2  # Scale CGPA to a maximum of 20
    score += float(student['sgpa']) * 1.5  # Scale SGPA to a maximum of 15
    
    # Extra points for internship experience
    if student['internship_experience'] == 'yes':
        score += 20
    
    # Score for seminars and workshops
    if student['seminars_or_workshops_attended'] == 'yes':
        score += 10
    
    # Extra points for extracurricular activities
    if student['extracurricular_activities'] == 'yes':
        score += 10

    return score

def has_common_interests(mentor, mentee):
    """Check if mentor and mentee share common tech stack or areas of interest."""
    mentor_tech_stack = set(mentor['tech_stack'].split(', '))
    mentee_tech_stack = set(mentee['tech_stack'].split(', '))
    mentor_interests = set(mentor['areas_of_interest'].split(', '))
    mentee_interests = set(mentee['areas_of_interest'].split(', '))
    
    return bool(mentor_tech_stack & mentee_tech_stack or mentor_interests & mentee_interests)

def match_mentors_mentees(students):
    """Match mentors with mentees dynamically with fallback matching."""
    mentors = []
    mentees = []
    matches = []
    
    # Separate students into mentor and mentee lists based on semester
    for student in students:
        if int(student['semester']) >= 5:
            mentors.append(student)
        mentees.append(student)  # Everyone can be a mentee
    
    # Sort mentors by their evaluated score
    mentors = sorted(mentors, key=evaluate_student, reverse=True)
    
    # Dictionary to count mentees per mentor (max 3 mentees per mentor)
    mentor_mentee_count = defaultdict(int)
    
    # First match based on common tech stack or areas of interest
    unmatched_mentees = []
    for mentee in mentees:
        matched = False
        for mentor in mentors:
            if mentor_mentee_count[mentor['name']] < 3 and has_common_interests(mentor, mentee):
                matches.append((mentor['name'], mentee['name']))
                mentor_mentee_count[mentor['name']] += 1
                matched = True
                break
        
        if not matched:
            unmatched_mentees.append(mentee)
    
    # Fallback: Assign remaining unmatched mentees to mentors
    if unmatched_mentees:
        mentor_cycle = cycle(mentors)  # Cycle through mentors to ensure even distribution
        for mentee in unmatched_mentees:
            mentor = next(mentor_cycle)
            while mentor_mentee_count[mentor['name']] >= 3:
                mentor = next(mentor_cycle)
            matches.append((mentor['name'], mentee['name']))
            mentor_mentee_count[mentor['name']] += 1

    return matches

@app.route('/match', methods=['GET'])
def match():
    """Endpoint to trigger mentor-mentee matching."""
    students = get_students_data()  # Fetch the real data from API
    if not students:
        return jsonify({"error": "Could not fetch student data"}), 500

    matches = match_mentors_mentees(students)
    return jsonify({"matches": matches})

if __name__ == '__main__':
    app.run(debug=True)
