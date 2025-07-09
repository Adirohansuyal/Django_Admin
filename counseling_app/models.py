from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

class PersonalInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.full_name

class MarksEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    def __str__(self):
        return f"{self.subject} - {self.marks_obtained}/{self.total_marks}"

class SeatAllotment(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.course} ({self.seat_number})"

class Payment(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_receipt = models.FileField(upload_to='payments/')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.is_verified else 'Pending'}"

class AdminUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AdminUserManager()

    def __str__(self):
        return self.email
