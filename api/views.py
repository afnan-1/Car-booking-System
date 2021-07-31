from rest_framework import serializers
from api.serializers import BookingSerializer, CarSerializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import *
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

@api_view(['GET'])
def car_details(request,id):
    car = Cars.objects.get(id=id)
    serializer = CarSerializer(car,many=False)
    return Response(serializer.data)



@api_view(['GET',])
def list_cars(request):
    cars = Cars.objects.all()
    serializer = CarSerializer(cars,many=True)
    return Response(serializer.data)


@api_view(['GET',])
def list_cars_available(request):
    cars = Cars.objects.filter(booked=False)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def book_car(request,id):
    try:
        data = request.data
        car = Cars.objects.get(id=id)
        car.booked = True
        car.save()

        booking = Booking()
        booking.car = car
        booking.user = request.user
        booking.address = data['address']
        booking.save()
        return Response({'message':'Car Booked'},status=200)
    except:
        return Response({"message":"Car is Already Booked"},status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def booking_paid(request,id):
    booking = Booking.objects.get(id=id)
    if request.user.is_driver:
        booking.car.car_driver = request.user
        booking.is_paid = True
        booking.save()
        return Response({"message":"Booking is paid Succesfully"},status=200)
    else:
        return Response({"message":"You are not driver"},status=400)





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = UserProfile(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),
            mobile_no=data['mobile_no'],
            is_driver=data['is_driver']
        )
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_bookings(request):
    booking = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(booking,many=True)
    return Response(serializer.data)