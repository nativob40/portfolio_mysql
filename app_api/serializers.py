from rest_framework import serializers
from app_dashboard.models import Departments


class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'
