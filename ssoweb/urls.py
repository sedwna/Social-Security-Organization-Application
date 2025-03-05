from django.urls import path
from . import views
from .views import *



app_name = 'ssoweb'


urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('create-case/', CreateCaseView.as_view(), name='create_case'),
    path('cases/', ListUserCasesView.as_view(), name='list_cases'),
    path('create-workshop/', CreateWorkshopView.as_view(), name='create_workshop'),
    path('list-user-workshops/', ListUserWorkshopsView.as_view(), name='list_user_workshops'),

]