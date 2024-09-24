from django.urls import path
from .views import CountryList, CountryDetail, RegionDetail, RegionList, ZoneList, ZoneDetail, WoredaList, WoredaDetail

urlpatterns = [
    path('region/', RegionList.as_view()),
    path('region/<int:pk>/', RegionDetail.as_view()),
    path('country/', CountryList.as_view()),
    path('country/<int:pk>/', CountryDetail.as_view()),
    path('zone/', ZoneList.as_view()),
    path('zone/<int:pk>/', ZoneDetail.as_view()),
    path('woreda/', WoredaList.as_view()),
    path('woreda/<int:pk>/', WoredaDetail.as_view()),
]