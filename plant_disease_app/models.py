from django.db import models

# Create your models here.

class DiseaseInfo(models.Model):
    disease_name = models.CharField(max_length=100)
    description = models.TextField()
    possible_steps = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.disease_name

class SupplementInfo(models.Model):
    disease_name = models.CharField(max_length=100)
    supplement_name = models.CharField(max_length=100)
    supplement_image = models.URLField()
    buy_link = models.URLField()

    def __str__(self):
        return f"{self.disease_name} - {self.supplement_name}"