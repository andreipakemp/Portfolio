from django.urls import path, include
from Base import views
from Base.views import ViewUserCreate, ViewLoginCustom
from django.views.generic.base import TemplateView

urlpatterns = [
    path(
        '', 
        views.index,
        name='index'
        ),
    path(
        'other',
        views.otherPage, 
        name='other'
        ),
    path(
        'about',
        views.aboutPage,
        name='about'
        ),
    path(
        'projects',
        views.projectsPage,
        name='projects'
        ),
    path(
        'register/', 
        ViewUserCreate.as_view(), 
        name='register'
        ),
    path(
        'register/success/', 
        TemplateView.as_view(template_name="registration/success.html"), 
        name='register-success'
    ),
    path(
        'login/', 
        ViewLoginCustom.as_view(), 
        name='login'
        ),
    path(
        '', 
        include('django.contrib.auth.urls')
        ),
]