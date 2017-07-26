# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
import json


def validate_name(name):
    if not(0 < len(name) <= 255):
        raise ValidationError(
             unicode(name)+" is not a string with a length between 1 and 255 characters')"
     )


def validate_body(body):
    if not(0 < len(body) <= 5*2**20):
        raise ValidationError(
             unicode(body)+" is not a string with a length between 1 and 5MB characters')"
     )


def validate_loan(loan):
    if loan < 1:
        raise ValidationError(
             unicode(loan)+" is not an integer greater than 0')"
     )


def validate_author(auth):
    if not (type(auth) is int):
        raise ValidationError("Not a User")


# User Model
class User(models.Model):
    Name = models.CharField(max_length=255,validators=[validate_name])

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id


# Loan Model
class Loan(models.Model):
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen')
    )
    Currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    Loan = models.IntegerField(validators=[validate_loan])
    # It's represented using cents to not incur with the
    # floating point loss of precision

    def __unicode__(self):
        return self.id

    def save(self, *args, **kwargs):
        self.full_clean()
        self.Loan = int(self.Loan*100)
        super(Loan, self).save(*args, **kwargs)


# Report Model
class Report(models.Model):

    Title = models.CharField(max_length=255,validators=[validate_name])
    Body = models.CharField(max_length=5*2**20,validators=[validate_body])
    Author = models.ForeignKey(User, on_delete=models.CASCADE,validators=[validate_author])
    Loans = models.ManyToManyField(Loan)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Report, self).save(*args, **kwargs)

    def sum_loans(self):
        dictionary_currencies ={"USD":0.0,"JPY":0.0,"GBP":0.0}
        for item in list(self.Loans.all()):
            dictionary_currencies[item.Currency] += item.Loan*0.01
        return json.dumps(dictionary_currencies)
