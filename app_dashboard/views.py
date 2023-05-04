from django.views.generic import TemplateView
import pandas as pd
from app_dashboard.models import Employees,DeptEmp,Salaries,Departments, DeptManager
from django.db.models import Sum,Avg,Count,F
from django.db.models.functions import ExtractYear
import pandas as pd
import numpy as np
import datetime
from django.http import HttpResponse
from django.template import loader


###############################################################################################################################
#                                                                                                                             #
#                                                       DASHBOARD                                                             #
#                                                                                                                             #
###############################################################################################################################

class Dash_uno(TemplateView):
    
    template_name = 'dashboard/dash_uno.html'


    def testing(request):

        mydata = sum(Employees.objects\
                            .filter(deptemp__dept_no__dept_name__in=['Development', 'Production', 'Finance', 'Sales', 'Human Resources'])\
                            .annotate(departamento=F('deptemp__dept_no__dept_name'), año=ExtractYear('hire_date'))\
                            .values('departamento', 'año')\
                            .annotate(Cant_Emp=Count('emp_no', distinct=True))\
                            .order_by('departamento', '-año')\
                            .values_list('Cant_Emp',flat=True))
        
        template = loader.get_template('dashboard/test.html')

        context = {
            'Empleados': mydata,
            'cards':{
                        'salary_last_month': mydata
                              },
        }
        return HttpResponse(template.render(context, request))
    
    ######## Cards #######


    ######## Graficos #######

    def contrataciones(self,depto):

        datos = Employees.objects.filter(deptemp__dept_no__dept_name__in=[depto])\
                         .annotate(departamento=F('deptemp__dept_no__dept_name'), año=ExtractYear('hire_date'))\
                         .values('departamento', 'año')\
                         .annotate(Cant_Emp=Count('emp_no', distinct=True))\
                         .order_by('departamento', '-año')\
                         .values_list('Cant_Emp')

        return np.array(datos).tolist
    
    ############### TABLAS #################

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        ##### Cards #####
        context['card_new_orders'] = DeptEmp.objects.filter(to_date__contains=9999).count # Employees actives
        context['card_new_customers'] = Employees.objects.filter(hire_date__contains = 2000).count # New Employees
        context['card_sales_last_month'] = Departments.objects.count
        context['card_costs_last_month'] = sum(Salaries.objects.values_list('salary',flat=True).filter(to_date__contains=datetime.date(2002, 8,1)))
        
        ##### Graficos #####

        ### Sales ###
        context['sales_over_time'] = sum(Employees.objects.values_list('deptmanager__dept_no__dept_name')\
                                                                      .exclude(deptmanager__dept_no=None)\
                                                                      .annotate(sueldos=Sum('salaries__salary'))\
                                                                      .values_list('sueldos',flat=True))
        
        context['sales_meses'] = np.array(Departments.objects.values_list('dept_name')).tolist

        context['sales_montos'] = np.array(Employees.objects.values_list('deptmanager__dept_no__dept_name')\
                                                            .exclude(deptmanager__dept_no=None)\
                                                            .annotate(sueldos=Sum('salaries__salary'))\
                                                            .values_list('sueldos',flat=True)
                                        ).tolist

        context['sales_avg'] = np.array(Employees.objects.values_list('deptmanager__dept_no__dept_name')\
                                                         .exclude(deptmanager__dept_no=None)\
                                                         .annotate(avg_valores=Avg('salaries__salary'))\
                                                         .values_list('avg_valores')\
                                        ).round(2).tolist

        ### Best Client ###

        # Salary by Departmens
        context['cliente_monto'] = sum(Employees.objects\
                                            .filter(deptemp__dept_no__dept_name__in=['Development', 'Production', 'Finance', 'Sales', 'Human Resources'])\
                                            .annotate(departamento=F('deptemp__dept_no__dept_name'), año=ExtractYear('hire_date'))\
                                            .values('departamento', 'año')\
                                            .annotate(Cant_Emp=Count('emp_no', distinct=True))\
                                            .order_by('departamento', '-año')\
                                            .values_list('Cant_Emp',flat=True))
        
        context['cliente_data_inicio'] = 1985#self.best_client()['ano'].min() #pointStart
        context['cliente_data_rango'] = str.format(f"Range: 1985 to 2000")#str.format(f"Range: {self.best_client()['ano'].min()} to {self.best_client()['ano'].max()}") #xAxis - rangeDescription

        # Datos
        departamento =  Departments.objects.values_list('dept_name',flat=True) #nombre de clientes sin duplicados

        context['cliente_uno_nombre'] = departamento[0]
        context['cliente_uno_datos'] = self.contrataciones(departamento[0])#self.best_client()['monto'][self.best_client()['customername']==departamento[0]].astype('float').to_list()

        context['cliente_dos_nombre'] = departamento[1]
        context['cliente_dos_datos'] =self.contrataciones(departamento[1])#self.best_client()['monto'][self.best_client()['customername']==departamento[1]].astype('float').to_list()

        context['cliente_tres_nombre'] = departamento[2]
        context['cliente_tres_datos'] = self.contrataciones(departamento[2])#self.best_client()['monto'][self.best_client()['customername']==departamento[2]].astype('float').to_list()

        context['cliente_cuatro_nombre'] = departamento[3]
        context['cliente_cuatro_datos'] = self.contrataciones(departamento[3])#self.best_client()['monto'][self.best_client()['customername']==departamento[3]].astype('float').to_list()

        context['cliente_cinco_nombre'] = departamento[4]
        context['cliente_cinco_datos'] = self.contrataciones(departamento[4])#self.best_client()['monto'][self.best_client()['customername']==departamento[4]].astype('float').to_list()

        ##### Tablas #####
        
        context['list_client'] = Employees.objects.values('emp_no', 'first_name', 'last_name','titles__title')\
                                                  .filter(titles__title__contains='Senior Engineer',titles__to_date__contains=9999)[:1000]

        context['list_person_sales'] = Employees.objects.values('first_name','last_name','titles__title','salaries__salary')\
                                                        .filter(deptemp__to_date__contains=datetime.date(9999, 1,1), titles__to_date__contains=datetime.date(9999, 1,1))\
                                                        .order_by('-salaries__salary')[:10] # El '-' indica que el orden es DESC
        return context


