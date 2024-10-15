from django.core.management.base import BaseCommand
import pandas as pd
from mentor_mentee.models import Participant

class Command(BaseCommand):
    help = 'Imports participant data from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Path to your Excel file
        file_path = 'D:/project-api/project_api/mentor_mentee/extended_form_data_database_style.xlsx'
        # Load the Excel data
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            participant = Participant(
                name=row['name'],
                registration_no=row['registration_no'],
                semester=row['semester'],
                branch=row['branch'],
                mentoring_preferences=row['mentoring_preferences'],
                previous_mentoring_experience=row.get('previous_mentoring_experience', ''),
                tech_stack=row['tech_stack'],
                areas_of_interest=row['areas_of_interest'],
                published_research_papers=row['published_research_papers'],
                hackathon_participation=row['hackathon_participation'],
                number_of_wins=row['number_of_wins'] if pd.notna(row['number_of_wins']) else 0,
                number_of_participations=row['number_of_participations'] if pd.notna(row['number_of_participations']) else 0,
                hackathon_role=row.get('hackathon_role', None),
                coding_competitions_participate=row['coding_competitions_participate'],
                number_of_coding_competitions=row['number_of_coding_competitions'] if pd.notna(row['number_of_coding_competitions']) else 0,
                cgpa=row['cgpa'],
                sgpa=row['sgpa'],
                internship_experience=row['internship_experience'],
                number_of_internships=row['number_of_internships'] if pd.notna(row['number_of_internships']) else 0,
                internship_description=row.get('internship_description', None),
                proof_of_internships=row.get('proof_of_internships', None),
                seminars_or_workshops_attended=row.get('seminars_or_workshops_attended', None),
                describe_seminars_or_workshops=row.get('describe_seminars_or_workshops', None),
                extracurricular_activities=row.get('extracurricular_activities', None),
                describe_extracurricular_activities=row.get('describe_extracurricular_activities', None),
                proof_of_extracurricular_activities=row.get('proof_of_extracurricular_activities', None),
                short_term_goals=row.get('short_term_goals', None),
                long_term_goals=row.get('long_term_goals', None),
                strengths_and_weaknesses=row.get('strengths_and_weaknesses', None),
                preferred_learning_style=row['preferred_learning_style'],
                areas_for_personal_growth=row.get('areas_for_personal_growth', None),
                date=pd.to_datetime(row['date'])
            )
            # Save the participant to the database
            participant.save()

        self.stdout.write(self.style.SUCCESS("Data import completed successfully!"))
