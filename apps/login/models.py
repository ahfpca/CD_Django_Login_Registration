from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
date_reg_exp = re.compile('\d{4}-\d{2}-\d{2}')

# Create your models here.
class UserManager(models.Manager):
    def record_validator(self, postData):
        ageLimit = 12 # Minimum age to register

        errors = {}

        # Validate first_name
        first_name = postData['first_name'].strip()
        if len(first_name) < 1:
            errors['first_name'] = "First name is required!"
        elif len(first_name) < 2:
            errors['first_name'] = "First name should have at least 2 characters!"
        if not charCheckName(first_name):
            errors['first_name'] = "First name accept only alhpabeth and space!"

        # Validate last_name
        last_name = postData['last_name'].strip()
        if len(last_name) < 1:
            errors['last_name'] = "Last name is required!"
        elif len(last_name) < 2:
            errors['last_name'] = "Last name should have at least 2 characters!"
        if not charCheckName(last_name):
            errors['last_name'] = "Last name accept only alhpabeth and space!"
        
        # Validate email
        email = postData['email'].strip()
        if len(email) < 1:
            errors['email'] = "Email is required!"
        elif not email_regex.match(email):
            errors['email'] = "Email is not valid!"
        
        # Check for email uniqueness
        res = User.objects.filter(email = email).first()
        # print("=" * 80)
        # print(res)
        if res:
            errors['email'] = "This Email is already registered in our database!"

        # Validate Birth date
        birth_date = postData["birth_date"].strip()
        #print(f"[{birth_date}]")
        if len(birth_date) < 1:
            errors['birth_date'] = "Birth date is required!"
        elif not date_reg_exp.match(birth_date):
            errors['birth_date'] = "Birth date is incorrect!"
        else:
            try:
                brdate = datetime.strptime(birth_date, '%Y-%m-%d')

                curYear = datetime.now().year
                curMonth = datetime.now().month
                
                birthYear = brdate.year
                birthMonth = brdate.month

                if curYear < birthYear + ageLimit or (curYear == birthYear + ageLimit and curMonth < birthMonth):
                    errors['birth_date'] = f"You should be at least {ageLimit} years old to register."
            except:
                errors['birth_date'] = "Birth date is incorrect!"

        # Validate password
        passcode = postData["passcode"].strip()
        #print(f"[{passcode}]")
        if len(passcode) < 8:
            errors['passcode'] = "Password should be 8 to 20 characters!"
        elif not charCheckPassword(passcode):
            errors['passcode'] = "Password should contain at least 1 upper case, 1 lower case, 1 number, and 1 special character!"

        # Validate confirm password
        pass_confirm = postData["pass_confirm"]
        if passcode != pass_confirm:
            errors['pass_confirm'] = "Password and its confirm are not matching"

        return errors


class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    user_uniq = models.CharField(max_length = 255, default = None, null = True, blank = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 255)
    passcode = models.CharField(max_length = 255)
    birth_date = models.CharField(max_length = 10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __repr__(self):
        return "<Blog object: {} {}>".format(self.first_name, self.last_name)


def charCheckName(name):
    for c in name:
        if not c.isalpha() and not c.isspace():
            return False

    return True


def charCheckPassword(pwd):
    result = True
    upper = 0
    lower = 0
    number = 0
    nonalphanum = 0

    for c in pwd:
        if c.isupper():
            upper += 1
        if c.islower():
            lower += 1
        if c.isnumeric():
            number += 1
        if not c.isspace() and not c.isalnum():
            nonalphanum += 1

    if upper == 0 or lower == 0 or number == 0 or nonalphanum == 0:
        return False

    return result
