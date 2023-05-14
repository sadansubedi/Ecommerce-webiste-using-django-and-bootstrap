from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

STATE_CHOICE = (
    ('Province No. 1','Koshi Province'),
    ('Province No. 2','Madhes Province'),
    ('Province No. 3','Bagmati Province'),
    ('Province No. 4','Gandaki Province'),
    ('Province No. 5','Lumbini Province'),
    ('Province No. 6','Karnali Province'),
    ('Province No. 7','Sudurpashchim Province'),
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField(max_length=200)
    state = models.CharField(choices=STATE_CHOICE,max_length=200)

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)#max_length must be equal or more than CATEGORY_CHOICES ok
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)#PositiveIntegerField start from 0 but by default=1 makes starting from 1 ok 

    def __str__(self):
        return str(self.id)
    
    @property #to show thw individual price of item in placeorder from where we can get cost of each item,used in line no 15 of checkout.html {{items.total_cost}}
    def total_cost(self):
        return self.quantity*self.product.discounted_price

STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='Pending')#default='Pending' first it is pending state ok  
    
    @property #to show thw individual price of item in placeorder from where we can get cost of each item,used in line no 15 of checkout.html {{items.total_cost}}
    def total_cost(self):
        return self.quantity*self.product.discounted_price
