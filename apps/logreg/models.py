from __future__ import unicode_literals
import re, datetime, bcrypt
from django.db import models

class UserManager(models.Manager):



    def login(self, guest):
        echeck = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = []
        if not guest['email'] or not guest['password']:
            errors.append('no_entry')
            return ( False , errors )
        if not echeck.match(guest['email']):
            errors.append('invalid_em')
            return ( False , errors )

        try:
            dbUser = User.objects.filter( email = guest['email'].lower() )
            dbPass = str(dbUser[0].password)
            guestPass = str(guest['password'])
            if bcrypt.hashpw(guestPass, dbPass) == dbPass :

                return ( True , dbUser )
            else:
                errors.append('abs_pw')
                return (False, errors)
        except:
            errors.append('abs_em')
            return (False, errors)

        # if not errors == []:
        #     return ( False , errors )

    def register(self, guest):
        echeck = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pwnmcheck = re.compile(r'.{8}?')
        pwccheck = re.compile(r'.*\d.*[A-Z].*|.*[A-Z].*\d.*')
        fncheck = re.compile(r'[a-zA-Z-]')
        lncheck = re.compile(r'[a-zA-Z-]')
        dbUsers = User.objects.all()

        errors = []
        dbEmailCheck = User.objects.filter( email = guest['email'].lower() )
        if dbEmailCheck :
            errors.append('invalid_em')
            return (False , errors)
        if not guest['first_name'] or not guest['last_name'] or not guest['email'] or not guest['password'] or not guest['confirm'] or not guest['birthdate']:
            errors.append('no_entry')
            return ( False , errors )
        if not fncheck.match(guest['first_name']) :
            errors.append('invalid_fn')
        if len(guest['first_name']) < 2 :
            errors.append('short_fn')
        if len(guest['last_name']) < 2 :
            errors.append('short_ln')
        if not lncheck.match(guest['last_name']) :
            errors.append('invalid_ln')
        if not echeck.match(guest['email']):
            errors.append('invalid_em')
        if not pwnmcheck.match(guest['password']):
            errors.append('short_pw')
        if not pwccheck.match(guest['confirm']):
            errors.append('invalid_pw')
        if not guest['password'] == guest['confirm']:
            errors.append('pwcnf_unmatch')
        try:
            datetime.datetime.strptime(guest['birthdate'], '%Y-%m-%d')
            if datetime.datetime.strptime(guest['birthdate'], '%Y-%m-%d') > datetime.datetime.today():
                errors.append('future_baby')
        except ValueError:
            errors.append('invalid_bd')
        if errors == []:
            hashedpw = bcrypt.hashpw(guest['password'].encode(),bcrypt.gensalt())
            User.objects.create( first_name = guest['first_name'].lower(), last_name = guest['last_name'].lower(), email = guest['email'].lower(), password = hashedpw, birthdate = guest['birthdate'] )
            return (True)
        else:
            print '********'
            return (False, errors)
        return (False, errors)


class User(models.Model):
    first_name = models.CharField( max_length = 50 )
    last_name = models.CharField( max_length = 50 )
    email = models.EmailField( max_length = 50 )
    password = models.CharField( max_length = 255, default = 0 )
    birthdate = models.DateField( max_length = 50 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    objects = UserManager()
