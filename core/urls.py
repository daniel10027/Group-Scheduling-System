from django.urls import path
from . import views

urlpatterns = [
    path('upload_salles/', views.upload_salles, name='salles'),
    path('upload_filieres/', views.upload_filieres, name='filieres'),
    path('results/', views.display_results, name='results'),
    path('', views.home, name="home"),
    path('reset/', views.reset, name="reset"),
    path('generate_groups/', views.generate_groups, name="generate_groups")
     
     
]
