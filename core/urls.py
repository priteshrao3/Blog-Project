from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contect/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('addpost/', views.add_post, name='addpost'),
    path('update/<int:id>/', views.update_post, name='update'),
    path('delete/<int:id>/', views.delete_post, name='delete'),
]
