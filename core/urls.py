
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_nested import routers 


router = routers.DefaultRouter()
router.register('signup',views.UserRegstrationViewSet,basename='register')
router.register('login',views.UserLoginViewSet,basename='login')
router.register('users',views.CurrentUserViewSet,basename='users')
router.register('users/change/password',views.UserChangePasswordViewSet,basename='changepassword')

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', views.HelloView.as_view(), name='hello'),
    # path('register/', views.RegisterUserView.as_view(), name='register'),
]
