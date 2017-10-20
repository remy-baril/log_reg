from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime
from time import strftime,localtime

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regValidation(self, post):
        first_name = post['first_name']
        last_name = post['last_name']
        email = post['email'].lower()
        password = post['password']
        cpass = post['cpass']
        errors = []

        ##CHECK MOST STRICT VALS FIRST

        ## first name vals
        if len(first_name) < 1:
            errors.append('Must enter first name')
        elif len(first_name) < 2:
            errors.append('First name must be at least 2 letters')
        elif not first_name.isalpha():
            errors.append('First name must contain letters only')

        ## last name vals
        if len(last_name) < 1:
            errors.append('Must enter last name')
        elif len(last_name) < 2:
            errors.append('Last name must be at least 2 letters')
        elif not last_name.isalpha():
            errors.append('Last name must contain letters only')

        ## email vals
        if len(email) < 1:
            errors.append('Must enter email')
        elif not EMAIL_REGEX.match(email):
            errors.append('Email is not in valid format')

        ## password vals
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        elif password != cpass:
            errors.append('Passwords must match')

        ## checks whether email has already been registered 
        if not errors:
            users = self.filter(email=email)
            if users:
                errors.append('This email has already been registered')

        return {'status': len(errors) == 0, 'errors':errors} #this says return a dictionary of the "errors" array and a status. If the length of arrays is 0

        def createUser(self,post):
            first_name = req.post['first_name']
            last_name = req.post['last_name']
            email = req.post['reg_email'].lower()
            password = bcrypt.hashpw(req.post['reg_password'].encode(), bcrypt.gensalt())
            return self.create(first_name = first_name, email = email, last_name = last_name, password = password)
            ## ^ puts into in database query 'create' and enters everything into database

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager() ##connects an instance of UserManager to User model overwriting hidden objects key w new one

    def __str__(self):
        return 'Name: {} {}, Email: {}'.format(self.first_name,self.last_name,self.email)


