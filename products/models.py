from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Size(models.Model):
    choice=(('S','Small'),('M','Medium'),('L','Large'),('XL','XLarge'),('XXL','XXLarge'))
    size=models.CharField(max_length=5,choices=choice)

    def __str__(self):
        return self.size
    
# class Size(models.Model):
#     choice=(('S','Small'),('M','Medium'),('L','Large'),('XL','XLarge'),('XXL','XXLarge'))
#     size=models.CharField(max_length=5,choices=choice)

#     def __str__(self):
#         return self.size    

    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_image=models.ImageField(upload_to='product_images')
    size=models.ManyToManyField(Size)
    price=models.IntegerField()
    description=models.CharField(max_length=100)
    quantity=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name
    
def sizes(obj):
    return ", ".join([size.size for size in obj.size.all()])
sizes.short_description = 'Sizes'


class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.quantity} X {self.product.product_name}'
    

class Order(models.Model):
    user=models.ForeignKey(CustomUser,blank=True,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=10)
    address=models.TextField()
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    email=models.EmailField(null=True)
    is_paid=models.BooleanField(default=False)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.user}'
    
class BuyerWallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name
class AdminWallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name
    
class SellerWallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name
    



    