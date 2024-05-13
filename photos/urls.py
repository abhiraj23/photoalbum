from django.urls import path
from. import views 


urlpatterns = [
    
    path('register/', views.user_signup, name="signup"),
    path('', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    

    path('gallery/',views.gallery, name="gallery"),
    path('photo/<str:pk>/',views.viewPhoto, name="photo"),
    path('add/',views.addPhoto, name="add")
    
]

