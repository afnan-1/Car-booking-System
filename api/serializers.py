from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=('id','first_name','email','username','image','is_driver','mobile_no')



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    car_driver = serializers.SerializerMethodField(read_only=True)
    car_review = ReviewSerializer(many=True)
    car_driver_image = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Cars
        fields = "__all__"

    def get_car_driver(self,obj):
        return obj.car_driver.first_name

    def get_car_driver_image(self,obj):
        try:
            if obj.car_driver.image.url:
                return obj.car_driver.image.url
        except:
            return "No pic found"
        


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    car = CarSerializer(many=False)
    # car = serializers.SerializerMethodField(read_only=True)
    # car_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"

    def get_user(self,obj):
        return obj.user.first_name


