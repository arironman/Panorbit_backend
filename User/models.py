from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, gender, phone_number, otp, password=None):
        if not email and not phone_number:
            raise ValueError('Either Email or Phone Number field must be set')
        if email:
            email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            otp=otp
        )
        
        if password is None:
            password = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, gender, phone_number, otp, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            otp=otp,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def authenticate(self, email_or_phone, otp, request=None):
        try:
            validate_email(email_or_phone)
            user = self.get(email=email_or_phone)
        except ValidationError:
            user = self.get(phone_number=email_or_phone)

        if user:
            print(user.is_admin)
            print(otp)
            if user.is_admin and user.check_password(otp):
                return user
            if user.check_otp(otp):
                return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'phone_number', 'otp']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def check_otp(self, otp):
        # return self.otp == otp and self.otp_created_at + timezone.timedelta(minutes=5) > timezone.now()
        return self.otp == str(otp)

    def set_otp(self, otp):
        self.otp = otp
        self.otp_created_at = timezone.now()
        self.save()

    def set_password(self, password):
        self.password = password
        self.save()

    def check_password(self, password):
        return self.password == password
        

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
