from django.contrib.auth import views as auth_view
from django.urls import path
from .apis.views import *
from .views import *

urlpatterns = [
    path("ussd/", ussd, name='ussd'),
    path('about/', about, name='about'),
    path('contact/', contact, name="contact"),
    path('profile/', profile, name='profile'),
    path('api/keys/', APIKeysView.as_view()),
    path('api/prediction/', PredictionAPIView.as_view()),
    path('api/keys/validate/', ValidateAPIKeysView.as_view()),
    path('api/key/generate/', generate_api_key, name='generate_api_key'),
    path('api/sensor/data/<int:sensor_number>/', SensorDataAPIView.as_view()),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name="logout"),
]