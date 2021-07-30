from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=('id','first_name','email','username','image','is_driver','mobile_no')

class CarSerializer(serializers.ModelSerializer):
    car_driver = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cars
        fields = "__all__"

    def get_car_driver(self,obj):
        return obj.car_driver.first_name


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


