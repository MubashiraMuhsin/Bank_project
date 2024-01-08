from django.db import models


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dist = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
