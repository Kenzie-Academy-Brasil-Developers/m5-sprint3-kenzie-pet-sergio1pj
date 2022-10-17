from django.db import models

class SexChoices(models.TextChoices):
    Macho = "Macho"
    Femea = "Femea"
    Default = "Não informado"

class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=15, choices=SexChoices.choices, default=SexChoices.Default)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="animals")
    traits = models.ManyToManyField("traits.Trait", related_name="animals")

