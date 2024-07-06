from django.urls import path, include

from . import views



urlpatterns = [
   
   
    path('', views.portfolios, name='portfolio'),
    path('portfolio/', views.portfolios, name='portfolios'),

    path('portfolios/', views.portfolios, name='portfolios'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('program/edit/<int:id>/', views.edit_portfolio, name='edit_portfolio'),
  

    path('pregion/<int:id>/', views.pregion, name='pregion'),
    path('pregion/pzones/', views.pzones, name='pzones'),
    path('pregion/pzones/pworedas/', views.pworedas, name='pworedas'),
    path('portfolios_list/', views.portfolios_list, name='portfolios_list'),
    path('portfolio/add/', views.add_porfolio, name='add_portfolio'),
    path('edit/<int:id>/', views.edit_portfolio, name='edit_portfolio'),
    path('delete/<int:pk>/', views.delete_portfolio, name='delete_portfolio'),
    path('portfolio_filter/', views.portfolio_filter, name='portfolio_filter'),
    path('categories/', views.categories, name='categories'),
   
    path('portfolio_profile/<int:pk>/', views.portfolio_profile, name='portfolio_profile'),
    path('portfolio_conceptnotes/<int:id>/', views.portfolio_conceptnotes, name='portfolio_conceptnotes'),
    path('fieldoffice/<int:id>/', views.fieldoffices, name='fieldoffices'),
    path('fieldoffice_edit/<int:pk>/', views.fieldoffice_edit, name='fieldoffice_edit'),
     
    path('fieldoffice_delete/<int:pk>/', views.remove_fieldoffice, name='remove_fieldoffice'),

    
    
 
]

