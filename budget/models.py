from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)


class Budget(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Operation(models.Model):
    datetime = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    budget = models.ForeignKey(Budget, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    is_recurring = models.BooleanField()
    is_income = models.BooleanField()
    comment = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.pk)
