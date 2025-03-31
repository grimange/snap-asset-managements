from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboards/index.html'
    template_hr = 'hr/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_hr)
