from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.http import JsonResponse
from equipments.models import EquipmentType, EquipmentBrand


class EquipmentMainView(PermissionRequiredMixin, View):
    permission_required = 'equipments.view_equipment'
    template_name = 'equipments/index.html'

class EquipmentView(EquipmentMainView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EquipmentAddView(EquipmentMainView):
    permission_required = 'equipments.add_equipment'
    def post(self, request, *args, **kwargs):
        select = request.POST.get('select', None)
        action = request.POST.get('action', None)

        if select == 'Equipment Type' and action == 'get':
            types = EquipmentType.objects.filter(is_active=True).values('id','name')
            return JsonResponse(list(types), safe=False)
        elif select == 'Brand' and action == 'get':
            brands = EquipmentBrand.objects.filter(is_active=True).values('id','name')
            return JsonResponse(list(brands), safe=False)
        elif select == 'Equipment Type' and action == 'add':
            name = request.POST.get('name', None)
            if name:
                EquipmentType.objects.create(name=name)
                return JsonResponse({'success': 'Equipment Type Added'})
        return JsonResponse({'error': 'Invalid Request'})
