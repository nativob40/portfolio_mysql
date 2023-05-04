from rest_framework.generics import ListAPIView
from app_dashboard.models import Departments
from app_api.serializers import DepartamentosSerializer

class DepartamentosListAPIView(ListAPIView):
    queryset = Departments.objects.all().order_by('dept_no')
    serializer_class = DepartamentosSerializer

    def post(self,request,*args, **kwargs):
        return self.list(request,**args, **kwargs)
