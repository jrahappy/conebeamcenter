from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_set",
        related_query_name="user",
    )

    is_consumer = models.BooleanField("Is Consumer", default=False)
    # False:CBCT, True:SAVVY
    whichapp = models.BooleanField("Which App", default=False)
    # False:Vendors, True:HH Members
    is_employee = models.BooleanField("Is Employee", default=False)
    # False:not agree, True:agree
    is_terms = models.BooleanField("Is Terms", default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    cellphone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        choices=[("Male", "Male"), ("Female", "Female")],
        max_length=10,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    suite = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    x_cordinate = models.FloatField(null=True, blank=True)
    y_cordinate = models.FloatField(null=True, blank=True)
    office_phone = models.CharField(max_length=20, null=True, blank=True)
    office_fax = models.CharField(max_length=20, null=True, blank=True)
    office_email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    whereiscomefrom = models.BooleanField("CBCT or SAVVY", default=False)
    extra_info1_str = models.CharField(max_length=20, null=True, blank=True)
    extra_info2_int = models.IntegerField(null=True, blank=True, default=0)
    extra_info3_bool = models.BooleanField("Extra info 3", default=False)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.category)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
