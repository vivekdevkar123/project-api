from django.contrib import admin
from account.models import Student
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class StudentModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base StudentModelAdmin
  # that reference specific fields on auth.User.


#   mobile_number = models.CharField(max_length=13)
#   is_active = models.BooleanField(default=False)
#   is_mentor = models.BooleanField(default=False)
#   is_admin = models.BooleanField(default=False)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

  list_display = ('reg_no', 'email', 'first_name', 'last_name','is_active', 'is_mentor')
  list_filter = ('is_admin','is_mentor',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('first_name','middle_name', 'last_name','mobile_number','section','year','semester',)}),
      ('Permissions', {'fields': ('is_admin','is_active', 'is_mentor',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. StudentModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'first_name', 'last_name','reg_no','mobile_number','is_mentor', 'password1', 'password2'),
      }),
  )
  search_fields = ('reg_no',)
  ordering = ('reg_no', 'id')
  filter_horizontal = ()


# Now register the new StudentModelAdmin...
admin.site.register(Student, StudentModelAdmin)