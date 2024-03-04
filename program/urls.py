from django.urls import path, include

from . import views



urlpatterns = [
   
    path('', views.program, name='programs'),
    path('program/', views.program, name='programs'),
    path('new/', views.create_view, name='add_program'),
    path('program/<int:pk>/', views.program_detail, name='program_detail'),
    path('program/edit/<int:id>/', views.edit_view, name='edit_program'),
    
]

htmxpatterns = [
    path('region/<int:id>/', views.region, name='region'),
    
    path('edit_user_roles/<int:uid>/', views.edit_user_role, name='edit_user_role'),
    #path('create_area/<int:id>', views.create_area, name='create_area'),
    path('edit/', views.edit_view, name='edit_program'),
    
    path('region/zones/', views.zones, name='zones'),
    path('region/zones/woredas/', views.woredas, name='woredas'),
    path('delete_area/<int:pk>/', views.delete_area, name='delete_area'),
    
    path('edit_program_profile/<int:id>/', views.edit_program_profile, name='edit_program_profile'),
    
    path('program_profile/<int:id>/', views.program_profile, name='program_profile'),
   

    path('delete_program/<int:pk>/', views.delete_program, name='delete_program'),
    
    
    
  
   
    
   
    path('delete_area/<int:pk>/', views.delete_area, name='delete_area'),

    path('area/<str:pk>/edit/', views.area_edit_form, name='area_edit_form'),
   
 
    
    path('program_filter/', views.search_results_view, name='program_filter'),
    path('indicators/<int:id>/', views.indicator_list, name='indicator_list'),
    path('indicator_add/<int:id>/', views.add_indicator, name='add_indicator'),
    path('indicator/<int:pk>/remove', views.remove_indicator, name='remove_indicator'),
    path('indicator/<int:pk>/edit', views.edit_indicator, name='edit_indicator'),
    path('users/<int:id>/', views.user_list, name='user_list'),
    path('user_add/<int:id>/', views.add_user, name='add_user'),
    path('area_list/<int:id>/', views.area_list, name='area_list'),
    path('region/edit_area/<int:pk>/', views.area_edit_form, name='area_edit_form'),
    path('update_user_roles/<int:id>/', views.update_user_roles, name='update_user_roles'),
    path('remove_user_role/<int:pk>/', views.remove_user_role, name='remove_user_role'),
    path('newportfolio/', views.newportfolio, name='newportfolio'),
   

   
]
 


urlpatterns += htmxpatterns