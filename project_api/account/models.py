from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

#  Custom User Manager
class StudentManager(BaseUserManager):
  def create_user(self, email, first_name,last_name,mobile_number,reg_no, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          first_name=first_name,
          last_name=last_name,
          mobile_number=mobile_number,
          reg_no=reg_no,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user
  
  def create_superuser(self,email,password,**other_fields):
    other_fields.setdefault('is_admin',True)
    other_fields.setdefault('is_active',True)
    
    if not email:
        raise ValueError(("Users must have an email address"))
    
    email=self.normalize_email(email)
    user=self.model(email=email,**other_fields)
    user.set_password(password)
    user.save()
    return user

class Student(AbstractBaseUser):
  
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  first_name = models.CharField(max_length=200)
  middle_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  mobile_number = models.CharField(max_length=13)
  reg_no = models.CharField(max_length=8)
  is_active = models.BooleanField(default=True)
  is_mentor = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = StudentManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name','mobile_number','reg_no']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin