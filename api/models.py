from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import tree
# Create your models here.
class UserProfile(AbstractUser):
    image = models.ImageField(null=True,blank=True)
    is_driver = models.BooleanField(default=False)
    mobile_no = models.CharField(max_length=100,null=True,blank=True)
class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

   


class Cars(BaseModel):
    name = models.CharField(max_length=100,null=True,blank=True)
    car_driver = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name="car_driver")
    model = models.CharField(max_length=100,null=True,blank=True)
    booked = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name



class Booking(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,related_name='user')
    car = models.ForeignKey(Cars, on_delete=models.DO_NOTHING,related_name='car')
    is_paid = models.BooleanField(default=False)
    address  = models.CharField(max_length=300, null=True,blank=True)


    @property
    def mobile_no(self):
        return self.user.mobile_no

    
    def __str__(self):
        return self.user.first_name

class Reviews(BaseModel):
    car = models.ForeignKey(Cars,on_delete=models.CASCADE,related_name="car_review")
    comment = models.TextField(null=True,blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_review')

    def __str__(self):
        return self.comment 
