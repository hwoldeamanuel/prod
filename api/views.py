from rest_framework import generics

from app_admin.models import Country, Region, Zone, Woreda
from .serializers import  CountrySerializer, RegionSerializer, ZoneSerializer, WoredaSerializer


class RegionList(generics.ListCreateAPIView):
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = Region.objects.all()
        country = self.request.query_params.get('country')
        if country is not None:
            queryset = queryset.filter(country=country)
        return queryset


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ZoneList(generics.ListCreateAPIView):
    serializer_class = ZoneSerializer

    def get_queryset(self):
        queryset = Zone.objects.all()
        region = self.request.query_params.get('region')
        if region is not None:
            queryset = queryset.filter(region=region)
        return queryset


class ZoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class WoredaList(generics.ListCreateAPIView):
    serializer_class = WoredaSerializer

    def get_queryset(self):
        queryset = Woreda.objects.all()
        zone = self.request.query_params.get('zone')
        if zone is not None:
            queryset = queryset.filter(zone=zone)
        return queryset


class WoredaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Woreda.objects.all()
    serializer_class = WoredaSerializer