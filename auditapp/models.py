from django.db import models

# Create your models here.


class Profile(models.Model):
    organisation_name = models.CharField(max_length=25)
    email_id = models.EmailField()
    country = models.CharField(max_length=25)

    def __str__(self):
        return str(self.organisation_name) + str(self.country)


class Audit(models.Model):
    operation_choices = (
        ("create", "create"),
        ("read", "read"),
        ("put", "put"),
        ("delete", "delete"),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    operation = models.CharField(choices=operation_choices, max_length=10)
    action = models.CharField(max_length=25)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.profile) + str(self.operation)


class Country(models.Model):
    name_of_the_country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name_of_the_country


# ☐ Api
# [{'id': < int >,: country_name: 'str', country_code: 'str'}]

class State(models.Model):
    name_of_the_state = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_of_the_state


class Tag(models.Model):
    tag_choices = (
        ("POE", "POE"),
        ("REG", "REG"),
    )
    name_of_the_tag = models.CharField(max_length=50, choices=tag_choices)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_of_the_tag


class URL(models.Model):

    url = models.URLField(max_length=200)
    name = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
