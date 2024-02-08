from django.db import models
from django.urls import reverse
from accounts.models import User
from icases.models import Product


class Manual(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    pdf_file = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    manual_name = models.ForeignKey(Manual, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    sub_text = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    tags = models.CharField(max_length=100, null=True, blank=True)
    ordery = models.IntegerField(default=0)
    orderx = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("support:article-detail", kwargs={"pk": self.pk})
