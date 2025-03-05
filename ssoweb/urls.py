from django.urls import path
from .views import *



app_name = 'ssoweb'


urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('user-register/', RegisterUserView.as_view(), name='register_user'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('create-individual-case/', CreateIndividualCaseView.as_view(), name='create_case'),
    path('create-legal-case/', CreateLegalCaseView.as_view(), name='create_case'),

]