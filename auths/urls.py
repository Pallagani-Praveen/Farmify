from django.urls import path
from . import views as v

urlpatterns = [
    path('',v.authindex,name="auth_index"),
    path('signup',v.auths_signup,name="signup"),
    path('login',v.auths_login,name="login"),
    path('logout',v.auths_logout,name="logout"),
]
