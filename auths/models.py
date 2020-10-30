from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from auths.managers import UserManager


# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    # choices
    GENDERS = [('male','MALE'),('female','FEMALE')]
    CHOICES = [('farmer','FARMER'),('dealer','DEALER')]

    # user info
    email = models.EmailField(_('email address'),unique=True)
    first_name = models.CharField(_('first name'),max_length=30,blank=True)
    second_name = models.CharField(_('second name'),max_length=30,blank=True)
    avatar = models.ImageField(upload_to='avatars/',null=True,blank=True)
    gender = models.CharField(choices=GENDERS,default='male',max_length=6)
    role = models.CharField(choices=CHOICES,default='farmer',max_length=6)
    

    # user permission info 
    is_active = models.BooleanField(_('active'),default=True)
    is_staff = models.BooleanField(_('staff'),default=True)
    date_joined = models.DateTimeField(_('date joined'),auto_now_add=True)

    # required settings
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name,self.second_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name



