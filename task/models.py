from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

#Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile_number, password):
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email = email, name=name, mobile_number=mobile_number)
        user.save()
        return user
    
    def create_superuser(self, email, name, mobile_number, password):
        user = self.create_user(email, name, mobile_number, password)
        user.is_admin = True
        user.is_active = True
        user.save()
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "mobile_number"]

    def __str__(self):
        return self.email

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    split_method = models.CharField(max_length=10, choices=[('equal', 'Equal'), ('exact', 'Exact'), ('percentage', 'Percentage')])
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, through='ExpenseSplit')

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_owed  = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    percentage_owed  = models.DecimalField(max_digits=5, decimal_places=2, null=True)

