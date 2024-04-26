from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Gas(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.BigIntegerField()
    msg=models.CharField(max_length=100)

class Product(models.Model):
    CAT=((1,'BPGAS'),(2,'HPGAS'),(3,'INDIANGAS'))
    name=models.CharField(max_length=20,verbose_name='Product Name')
    price=models.FloatField()
    pdetails=models.CharField(max_length=50)
    cat=models.IntegerField(verbose_name='Category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='Avaliable')
    pimage=models.ImageField(upload_to='image')
    def __str__(self):
        return self.name
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)  
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)


    
