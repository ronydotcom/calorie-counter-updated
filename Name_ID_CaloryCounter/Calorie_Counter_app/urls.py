from django.urls import path
from Calorie_Counter_app.views import*

urlpatterns = [
    
    path('',register_page,name='register_page'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),
    path('profile/',profile_page,name='profile_page'),
    path('calorie-list/',calorie_list,name='calorie_list'),
    path('dashboard-page/',dashboard_page,name='dashboard_page'),
    path('calorie/', calorie_page, name='calorie_page'),
]