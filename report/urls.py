from django.urls import path, include

from . import views




urlpatterns = [
   
    path('', views.reports, name='icnsreport'),
    path('intervention/', views.reports, name='icnsreport'),
    path('intervention/new', views.icnreport_add, name='icnreport_new'),
    path('intervention/<int:id>/edit/', views.icnreport_edit, name='icnreport_edit'),


    path('icn/add', views.icnreport_add, name='icnreport_add'),
    path('intervention/<int:pk>/', views.icnreport_detail, name='icnreport_detail'),
    path('intervention/<int:pk>/approval/', views.icnreport_submit_approval, name='icnreport_submit_approval'),
    path('activity/<int:pk>/approval/', views.activityreport_submit_approval, name='activityreport_submit_approval'),
    path('download/<int:id>/', views.download, name='download'),
    path('downloada/<int:id>/', views.downloada, name='downloada'),
    path('delete_icn/<int:pk>/', views.icnreport_delete, name='icnreport_delete'),
    
    path('iregion/', views.iregion, name='iregion'),
    path('iregion/izones/', views.izones, name='izones'),
    path('iregion/<int:id>/', views.iregion, name='iregion'),
    path('iregion/izones/', views.izones, name='izones'),
    path('iregion/izones/iworedas/', views.iworedas, name='iworedas'),
    path('idelete_iarea/<int:pk>/', views.idelete_area, name='idelete_area'),
    path('adelete_aarea/<int:pk>/', views.adelete_area, name='adelete_aarea'),
    path('iregion/iedit_iarea/<int:pk>/', views.iarea_edit_form, name='iarea_edit_form'),
    path('download_env_att/<int:id>/', views.download_env_att, name='download_env_att'),
    path('icnreport_submit_form_partial/<int:id>/', views.icnreport_submit_form_partial, name='icnreport_submit_form_partial'),
    path('activityreport_submit_form_partial/<int:id>/', views.activityreport_submit_form_partial, name='activityreport_submit_form_partial'),
    path('activity/', views.activitiesreport, name='activitiesreport'),
    path('activity/<int:pk>/', views.activityreport_detail, name='activityreport_detail'),
    path('activity/add', views.activityreport_add, name='activityreport_new'),
    path('activity/<int:id>/edit/', views.activityreport_edit, name='activityreport_edit'),
    path('aregion/<int:id>/', views.aregion, name='aregion'),
    path('aregion/aedit_aarea/<int:pk>/', views.aarea_edit_form, name='aarea_edit_form'),
    
]

htmxpatterns = [


 
 path('icnreport_submit_detail/<int:id>/', views.icnreport_submit_detail, name='icnreport_submit_detail'),
 path('icnreport_submit_list/<int:id>/', views.icnreport_submit_list, name='icnreport_submit_list'),


 path('icnreport_submit_form/<int:id>/', views.icnreport_submit_form, name='icnreport_submit_form'),
 path('activityreport_submit_form/<int:id>/', views.activityreport_submit_form, name='activityreport_submit_form'),
 path('icnreport_submit_document/<int:id>/', views.icnreport_submit_document, name='icnreport_submit_document'),
 path('activityreport_submit_document/<int:id>/', views.activityreport_submit_document, name='activityreport_submit_document'),
 path('icnreport_approvalp/<int:id>/', views.icnreport_approvalp, name='icnreport_approvalp'),
 path('icnreport_approvalf/<int:id>/', views.icnreport_approvalf, name='icnreport_approvalf'),
 path('icnreport_approvalt/<int:id>/', views.icnreport_approvalt, name='icnreport_approvalt'),
 path('activityreport_approvalt/<int:id>/', views.activityreport_approvalt, name='activityreport_approvalt'),
 path('activityreport_approvalp/<int:id>/', views.activityreport_approvalp, name='activityreport_approvalp'),
 path('activityreport_approvalf/<int:id>/', views.activityreport_approvalf, name='activityreport_approvalf'),
 path('icnreport_filter/', views.search_results_view, name='icnreport_filter'),
 path('activityreport_filter/', views.search_results_view2, name='activityreport_filter'),
 
 path('document_list/<int:id>/', views.document_list, name='document_list'),
 path('activityreport_document_list/<int:id>/', views.activityreport_document_list, name='activityreport_document_list'),
 path('iarea_list/<int:id>/', views.iarea_list, name='iarea_list'),
 path('aarea_list/<int:id>/', views.aarea_list, name='aarea_list'),
 path('current_submit_approval_list/<int:id>/', views.current_submit_approval_list, name='current_submit_approval_list'),
 path('latest_submit_approval_list/<int:id>/', views.latest_submit_approval_list, name='latest_submit_approval_list'),
 path('latest_submit_approval_list_activity/<int:id>/', views.latest_submit_approval_list_activity, name='latest_submit_approval_list_activity'),
 path('current_activityreport_submit_approval_list/<int:id>/', views.current_activityreport_submit_approval_list, name='current_activityreport_submit_approval_list'),
 path('submit_approval_list/<int:id>/', views.submit_approval_list, name='submit_approval_list'),
 path('activityreport_submit_approval_list/<int:id>/', views.activityreport_submit_approval_list, name='activityreport_submit_approval_list'),
 path('add_impact/<int:id>/', views.add_impact, name='add_impact'),
 path('add_activityreport_impact/<int:id>/', views.add_activityreport_impact, name='add_activityreport_impact'),
 path('impact_list/<int:id>/', views.impact_list, name='impact_list'),
 path('activityreport_impact_list/<int:id>/', views.activityreport_impact_list, name='activityreport_impact_list'),
 path('edit_impact/<int:pk>/', views.edit_impact, name='edit_impact'),
 path('edit_activityreport_impact/<int:pk>/', views.edit_activityreport_impact, name='edit_activityreport_impact'),
 path('impact/<int:pk>/remove', views.remove_impact, name='remove_impact'),
 path('activityreport_impact/<int:pk>/remove', views.remove_activityreport_impact, name='remove_activityreport_impact'),
]

urlpatterns += htmxpatterns