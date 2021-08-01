


from django.urls import path
from .views import *
urlpatterns = [
    path('list-cars/',list_cars),
    path('available-cars/',list_cars_available),
    path('book-car/<int:id>/',book_car),
    path('order-paid/<int:id>/',booking_paid),
    path('login/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', registerUser, name='register'),
    path('my-bookings/',get_my_bookings),
    path('car-detail/<int:id>/',car_details),
    path('car/reviews/add/<int:pk>/',createProductReview)
]
