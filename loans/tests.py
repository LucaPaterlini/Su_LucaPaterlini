# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from loans.models import User, Report, Loan
from django.core.exceptions import ValidationError

class UserTest(TestCase):
    # Checks all the expected invalid parameters for users
    def test_create_not_valid_user(self):
        with self.assertRaises(ValidationError):
            u = User()
            u.Name = ''
            u.save()

        with self.assertRaises(ValidationError):
            u = User()
            u.Name = '5'*256
            u.save()
    #Checks all the expected valid parameters for users
    def test_create_valid_user(self):
        u = User()
        u.Name = 'Luca'
        u.save()

class LoanTest(TestCase):
    # Checks all the expected invalid parameters for a loan
    def test_create_not_valid_loan(self):
        with self.assertRaises(ValidationError):
            l = Loan()
            l.Currency = 'bananan'
            l.Loan = 2
            l.save()
        with self.assertRaises(ValidationError):
            l = Loan()
            l.Currency = 'USD'
            l.Loan = -1
            l.save()

        with self.assertRaises(ValidationError):
            l = Loan()
            l.Currency = 'bananan'
            l.Loan = -1
            l.save()

    #Checks all the expected valid parameters for a loan
    def test_create_valid_loan(self):
        l = Loan()
        l.Currency = 'GBP'
        l.Loan = 10
        l.save()


class ReportTest(TestCase):
    # Checks all the expected invalid parameters for a loan
    def test_create_not_valid_report(self):
        with self.assertRaises(ValidationError):
            l = Report()
            l.Title = ''
            l.save()
        with self.assertRaises(ValidationError):
            l = Report()
            l.Title = 'hello'
            l.Body = ''
            l.save()
        with self.assertRaises(ValueError):
            l = Report()
            l.Title = 'hello'
            l.Body = ''
            l.Author = 1
            l.save()
        with self.assertRaises(ValueError):
            l = Report()
            l.Title = 'hello'
            l.Body = ''
            l.Loans = 3
            l.save()
        with self.assertRaises(ValueError):
            l = Report()
            l.Title = 'hello'
            l.Body = 'l'*(5*2**20+1)
            l.Loans = 3
            l.save()

    # Checks expected valid cases
    def test_create_valid_report(self):
        u = User();u.Name="Luca";u.save()
        l = Loan();l.Currency = 'GBP';l.Loan = 10;l.save()
        r = Report();r.Title="Super Important Report"
        r.Body = "Medium text"*200
        r.Author = u
        r.save()
        r.Loans.add(l)
        r.save()


class RelationsTest(TestCase):
    # Write a test case that ensures the relationships work as expected
    def test_username_by_currency_gbp(self):
        # inserting data
        u = User();u.Name="Luca";u.save()
        l = Loan();l.Currency = 'GBP';l.Loan = 10;l.save()
        r = Report();r.Title="Super Important Report"
        r.Body = "Medium text"*200
        r.Author = u
        r.save()
        r.Loans.add(l)
        r.save()
        # making the required query
        user = User.objects.get(report__Loans__Currency="GBP")
        self.assertEquals(user.Name,"Luca")

    # Write a test case for finding all reports that a loan belongs to
    def test_allreports_single_loan(self):
        # inserting data
        u = User();u.Name="Luca";u.save()
        l = Loan();l.Currency = 'GBP';l.Loan = 10;l.save()
        # inserting first report
        r = Report();r.Title="Super Important Report"
        r.Body = "Medium text"*200
        r.Author = u;r.save();r.Loans.add(l)
        # inserting second report
        r1 = Report();r1.Title = "Less Important Report"
        r1.Body = "Short text";r1.Author = u
        r1.save();r1.Loans.add(l);r1.save()
        # making the required query
        reports = list(Report.objects.filter(Loans=1))
        self.assertEquals(reports[0].Title, "Super Important Report")
        self.assertEquals(reports[1].Title, "Less Important Report")

    # Write a test case for calculating the sum of all loans that went into a specific report
    def test_sum_loans_single_report(self):
        # inserting data
        u = User();u.Name = "Luca";u.save()
        l = Loan();l.Currency = 'GBP';l.Loan = 10;l.save()
        l1 = Loan();l1.Currency = 'USD';l1.Loan = 30;l1.save()
        l2 = Loan();l2.Currency = 'JPY';l2.Loan = 30;l2.save()
        l3 = Loan();l3.Currency = 'JPY';l3.Loan = 30;l3.save()
        # creating a report

        r = Report();r.Title = "Money Report"
        r.Body = "text";r.Author = u;
        r.save();r.Loans.add(l,l1,l2,l3);r.save();
        self.assertEquals(r.sum_loans(), '{"JPY": 60.0, "USD": 30.0, "GBP": 10.0}')


