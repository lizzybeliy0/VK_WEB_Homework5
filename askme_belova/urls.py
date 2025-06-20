"""
URL configuration for askme_belova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexPage, name='index'),
    path('hot/', views.hotPage, name='hot'),
    path('question/<int:question_id>/', views.questionPage, name='question'),
    
    path('tag/<str:tag_name>/', views.tagPage, name='tag'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signUpPage, name='signup'),
    path('ask/', views.askPage, name='ask'),
    path('logout/', views.logoutPage, name='logout'),
    path('settings', views.settingsPage, name='settings'),

    path('question/right', views.setRightAnswer, name="right_answer"),
    path('make_like', views.createLike, name="like"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
