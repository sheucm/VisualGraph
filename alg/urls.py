from django.conf.urls import url
from alg import views

urlpatterns = [
    url(r'^randomSample/$', views.randomSample),  
    
]
