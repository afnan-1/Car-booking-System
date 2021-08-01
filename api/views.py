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
from django.db.models import Q

# Create your views here.

@api_view(['GET'])
def car_details(request,id):
    car = Cars.objects.get(id=id)
    serializer = CarSerializer(car,many=False)
    return Response(serializer.data)



@api_view(['GET',])
def list_cars(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    cars = Cars.objects.filter(
       Q(name__icontains=query)|Q(city__icontains=query), booked=False).order_by('-created_at')
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
        if car.booked:
            return Response({'message':'Car is Already Booked'},status=400)
        car.booked = True
        car.save()

        booking = Booking()
        booking.car = car
        booking.user = request.user
        booking.address = data['address']
        booking.mobile_no = data['mobile_no']
        booking.save()
        return Response({'message':'Car Booked'},status=200)
    except:
        return Response({"message":"Car is Already Booked"},status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def booking_paid(request,id):
    data = request.data
    booking = Booking.objects.get(id=id)
    if request.user.is_driver:
        booking.car.car_driver = request.user
        booking.is_paid = True
        booking.price = data['price']
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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    car = Cars.objects.get(id=pk)
    data = request.data
    print(data)
    # 1 - Review already exists
    alreadyExists = car.car_review.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=400)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=400)

    # 3 - Create review
    else:
        review = Reviews.objects.create(
            user=user,
            car=car,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = car.car_review.all()
        car.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        car.rating = total / len(reviews)
        car.save()

        return Response('Review Added')