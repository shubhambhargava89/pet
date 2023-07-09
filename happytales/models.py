# from _typeshed import Self
from django.db import models  # Create your models here.
from django.contrib.auth.models import User,AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MinLengthValidator,MaxLengthValidator

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka	', 'Karnataka	'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.IntegerField()
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('do','Dog'),
    ('ca', 'Cat'),
    ('df','Dog_Food'),
    ('cf','Cat_Food'),
    )


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Deliverd', 'Deliverd'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Feedback(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)], unique=True)
    city = models.CharField(max_length=200)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

PET_TYPE = (
    ('Cat', 'Cat'),
    ('Dog', 'Dog'),
)

class Report(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)], unique=True)
    city = models.CharField(max_length=200)
    pincode = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    pet_type = models.CharField(choices=PET_TYPE, max_length=50)
    pet_breed = models.CharField(max_length=200)
    pet_location = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)


class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)], unique=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.user.username

class Pet(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    post_date = models.DateField()
    pet_name = models.CharField(max_length=10, null=True)
    pet_type = models.CharField(max_length=10, null=True)
    vaccinated = models.CharField(max_length=10, null=True)
    pet_breed = models.CharField(max_length=100)
    price = models.FloatField(max_length=20)
    location = models.CharField(max_length=100)
    age = models.FloatField(max_length=20)
    color = models.CharField(max_length=100)
    weight = models.FloatField(max_length=20)
    image = models.FileField()
    description = models.CharField(max_length=300)
    creationdate = models.DateField()

    def __str__(self):
        return self.pet_name

class Adopter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)], unique=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.user.username

class Buy(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    interest = models.CharField(max_length=10,null=True)
    applydate = models.DateField()

    def __str__(self):
        return self.pet.pet_name


class Ngo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)], unique=True)
    image = models.FileField(null=True)
    ngo_name = models.CharField(max_length=10, null=True)
    reg_id = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.user.username

class Fundrais(models.Model):
    fname = models.CharField(max_length=20, null=True)
    lname = models.CharField(max_length=20, null=True)
    mobile = models.IntegerField(validators=[MaxLengthValidator(11), MinLengthValidator(11)], unique=True)
    amount = models.IntegerField(null=True)
    fundraisingdate = models.DateField()

    def __str__(self):
        return self.fname


class HealthCheckup(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    notes = models.TextField()

    def __str__(self):
        return self.pet.pet_name
