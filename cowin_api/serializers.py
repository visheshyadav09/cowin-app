from django.db.models import fields
from rest_framework import serializers
from .models import State, District

class StateSerializers(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['state_id', 'state_name']

class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['district_id', 'district_name']