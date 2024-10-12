from django.contrib import admin
from .models import Participant

class ParticipantAdmin(admin.ModelAdmin):
    # Fields to display in the list view in the admin interface
    list_display = ('name', 'registration_no', 'branch', 'semester', 'mentoring_preferences', 'cgpa', 'sgpa')
    
    # Fields that can be searched in the search box
    search_fields = ('name', 'registration_no', 'branch', 'mentoring_preferences')

    # Filter options in the admin panel
    list_filter = ('branch', 'mentoring_preferences', 'semester')

    # Fields to display in the detail/edit view
    readonly_fields = ('display_proof_of_research_publications', 'display_proof_of_hackathon_participation', 
                       'display_proof_of_coding_competitions', 'display_proof_of_academic_performance',
                       'display_proof_of_internships', 'display_proof_of_extracurricular_activities')

    # Method to handle file fields and display file presence
    def display_proof_of_research_publications(self, obj):
        if obj.proof_of_research_publications:
            return "Research Proof Uploaded"
        return "No File"
    
    def display_proof_of_hackathon_participation(self, obj):
        if obj.proof_of_hackathon_participation:
            return "Hackathon Proof Uploaded"
        return "No File"
    
    def display_proof_of_coding_competitions(self, obj):
        if obj.proof_of_coding_competitions:
            return "Coding Competition Proof Uploaded"
        return "No File"

    def display_proof_of_academic_performance(self, obj):
        if obj.proof_of_academic_performance:
            return "Academic Proof Uploaded"
        return "No File"

    def display_proof_of_internships(self, obj):
        if obj.proof_of_internships:
            return "Internship Proof Uploaded"
        return "No File"

    def display_proof_of_extracurricular_activities(self, obj):
        if obj.proof_of_extracurricular_activities:
            return "Extracurricular Proof Uploaded"
        return "No File"

    # Custom labels for the file display fields
    display_proof_of_research_publications.short_description = 'Proof of Research Publications'
    display_proof_of_hackathon_participation.short_description = 'Proof of Hackathon Participation'
    display_proof_of_coding_competitions.short_description = 'Proof of Coding Competitions'
    display_proof_of_academic_performance.short_description = 'Proof of Academic Performance'
    display_proof_of_internships.short_description = 'Proof of Internships'
    display_proof_of_extracurricular_activities.short_description = 'Proof of Extracurricular Activities'

admin.site.register(Participant, ParticipantAdmin)
