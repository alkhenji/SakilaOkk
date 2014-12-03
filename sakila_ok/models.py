# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'actor'

class ActorInfo(models.Model):
    actor_id = models.IntegerField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    film_info = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'actor_info'

class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=20)
    city = models.ForeignKey('City')
    postal_code = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'address'

class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'category'

class CategoryActorCount(models.Model):
    name = models.CharField(max_length=25)
    actorname = models.CharField(db_column='ActorName', max_length=91) # Field name made lowercase.
    count_fa_actor_id_field = models.BigIntegerField(db_column='COUNT(FA.actor_id)') # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    class Meta:
        managed = False
        db_table = 'category_actor_count'

class City(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=50)
    country = models.ForeignKey('Country')
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'city'

class Country(models.Model):
    country_id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'country'

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    store = models.ForeignKey('Store')
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(Address)
    active = models.IntegerField()
    create_date = models.DateTimeField()
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'customer'

class CustomerList(models.Model):
    customer_list_id = models.IntegerField(db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=91)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(db_column='zip code', max_length=10, blank=True) # Field renamed to remove unsuitable characters.
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    notes = models.CharField(max_length=6)
    sid = models.IntegerField(db_column='SID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'customer_list'

class Film(models.Model):
    film_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.TextField(blank=True) # This field type is a guess.
    language = models.ForeignKey('Language', related_name='filmslanguage')
    original_language = models.ForeignKey('Language', blank=True, null=True)
    rental_duration = models.IntegerField()
    rental_rate = models.DecimalField(max_digits=4, decimal_places=2)
    length = models.IntegerField(blank=True, null=True)
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.CharField(max_length=5, blank=True)
    special_features = models.CharField(max_length=54, blank=True)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'film'

class FilmActor(models.Model):
    actor = models.ForeignKey(Actor)
    film = models.ForeignKey(Film)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'film_actor'

class FilmCategory(models.Model):
    film = models.ForeignKey(Film)
    category = models.ForeignKey(Category)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'film_category'

class FilmList(models.Model):
    fid = models.IntegerField(db_column='FID', blank=True, null=True) # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=5, blank=True)
    actors = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'film_list'

class FilmText(models.Model):
    film_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'film_text'

class Inventory(models.Model):
    inventory_id = models.IntegerField(primary_key=True)
    film = models.ForeignKey(Film)
    store = models.ForeignKey('Store')
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'inventory'

class Language(models.Model):
    language_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'language'

class NicerButSlowerFilmList(models.Model):
    fid = models.IntegerField(db_column='FID', blank=True, null=True) # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=5, blank=True)
    actors = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'nicer_but_slower_film_list'

class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer)
    staff = models.ForeignKey('Staff')
    rental = models.ForeignKey('Rental', blank=True, null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField()
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'payment'

class Rental(models.Model):
    rental_id = models.IntegerField(primary_key=True)
    rental_date = models.DateTimeField()
    inventory = models.ForeignKey(Inventory)
    customer = models.ForeignKey(Customer)
    return_date = models.DateTimeField(blank=True, null=True)
    staff = models.ForeignKey('Staff')
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'rental'

class SalesByFilmCategory(models.Model):
    category = models.CharField(max_length=25)
    total_sales = models.DecimalField(max_digits=27, decimal_places=2, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sales_by_film_category'

class SalesByStore(models.Model):
    store = models.CharField(max_length=101)
    manager = models.CharField(max_length=91)
    total_sales = models.DecimalField(max_digits=27, decimal_places=2, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sales_by_store'

class Staff(models.Model):
    staff_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    address = models.ForeignKey(Address)
    picture = models.TextField(blank=True)
    email = models.CharField(max_length=50, blank=True)
    store = models.ForeignKey('Store')
    active = models.IntegerField()
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=40, blank=True)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'staff'

class StaffList(models.Model):
    staff_list_id = models.IntegerField(db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=91)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(db_column='zip code', max_length=10, blank=True) # Field renamed to remove unsuitable characters.
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    sid = models.IntegerField(db_column='SID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'staff_list'

class Store(models.Model):
    store_id = models.IntegerField(primary_key=True)
    manager_staff = models.ForeignKey(Staff, unique=True,related_name='storesmanagerstaff')
    address = models.ForeignKey(Address)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'store'

# Customer, Film, Payment, Rental, Inventory



