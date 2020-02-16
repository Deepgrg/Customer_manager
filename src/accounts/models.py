from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length = 150 ,null = True )
    phone = models.IntegerField(null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length = 150 ,null = True )

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY =(
        ('Indoor' , 'Indoor'),
        ('Outdoor' , 'Outdoor'),
    )
    name =  models.CharField(max_length=150 , null=True)
    price = models.FloatField(null = True)
    category = models.CharField(max_length=150 , null=True , choices=CATEGORY)
    description = models.TextField(max_length=150 , null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags= models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out of Delivery','Out of Delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey(Customer ,on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    status = models.CharField(max_length=150 , null=True ,choices = STATUS )
    
    def __str__(self):
        return self.product.name