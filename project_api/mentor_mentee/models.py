from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Participant(models.Model):
    SEMESTER_CHOICES = [(str(i), str(i)) for i in range(1, 9)]
    BRANCH_CHOICES = [('cse', 'CSE'), ('ct', 'CT'), ('aids', 'AIDS')]
    MENTORING_PREFERENCE_CHOICES = [('mentor', 'Mentor'), ('mentee', 'Mentee')]
    HACKATHON_ROLE_CHOICES = [('team leader', 'Team Leader'), ('member', 'Member')]
    YES_NO_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    LEVEL_CHOICES = [('International', 'International'), ('National', 'National'), ('College', 'College'), ('Conferences', 'Conferences'), ('None', 'None')]
    LEARNING_STYLE_CHOICES = [('Hands_on', 'Hands-on'), ('Project_based', 'Project-based'), ('Discuss_oriented', 'Discuss-oriented')]

    # Personal Information
    name = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=20, primary_key=True)  # Primary key
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    mentoring_preferences = models.CharField(max_length=10, choices=MENTORING_PREFERENCE_CHOICES)
    previous_mentoring_experience = models.TextField(blank=True, null=True)
    tech_stack = models.TextField()
    areas_of_interest = models.TextField()

    # Research
    published_research_papers = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='None')
    proof_of_research_publications = models.BinaryField(blank=True, null=True)  # Store the file as a BLOB

    # Hackathon
    hackathon_participation = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    number_of_wins = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    number_of_participations = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    hackathon_role = models.CharField(max_length=20, choices=HACKATHON_ROLE_CHOICES)
    proof_of_hackathon_participation = models.BinaryField(blank=True, null=True)  # Store the file as a BLOB

    # Coding Competitions
    coding_competitions_participate = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    level_of_competition = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    number_of_coding_competitions = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    proof_of_coding_competitions = models.BinaryField(blank=True, null=True)  # Store the file as a BLOB

    # Academic Performance
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    sgpa = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    proof_of_academic_performance = models.BinaryField(blank=True, null=True)  # Store the file as a BLOB

    # Internship
    internship_experience = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    number_of_internships = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    internship_description = models.TextField(blank=True, null=True)
    proof_of_internships = models.BinaryField(blank=True, null=True)  # Store the file as a BLOB

    # Seminars & Workshops
    seminars_or_workshops_attended = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    describe_seminars_or_workshops = models.TextField(blank=True, null=True)

    # Extracurricular Activities
    extracurricular_activities = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    describe_extracurricular_activities = models.TextField(blank=True, null=True)
    proof_of_extracurricular_activities = models.BinaryField(blank=True, null=True)  # Store the file as a BLOB

    # Personal Development
    short_term_goals = models.TextField(blank=True, null=True)
    long_term_goals = models.TextField(blank=True, null=True)
    strengths_and_weaknesses = models.TextField(blank=True, null=True)
    preferred_learning_style = models.CharField(max_length=20, choices=LEARNING_STYLE_CHOICES)
    areas_for_personal_growth = models.TextField(blank=True, null=True)

    # Miscellaneous
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.registration_no})'
