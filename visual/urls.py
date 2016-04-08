from django.conf.urls import url
from visual import views

urlpatterns = [
    url(r'^get_real_dengue_by_date/$', views.get_real_dengue_by_date),  
    url(r'^weight_of_SSB/$', views.weight_of_SSB),
]