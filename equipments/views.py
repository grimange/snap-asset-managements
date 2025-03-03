from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.http import JsonResponse
from equipments.models import EquipmentType, EquipmentBrand, EquipmentBrandModel


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
        elif select in ['Equipment Type', 'Brand'] and action == 'add':
            name = str(request.POST.get('name', None)).lower()
            if select == 'Equipment Type' and EquipmentType.objects.filter(name=name).exists():
                EquipmentType.objects.create(name=name)
                return JsonResponse({'success': 'Equipment Type Added'})
            elif select == 'Brand' and EquipmentBrand.objects.filter(name=name).exists():
                EquipmentBrand.objects.create(name=name)
                return JsonResponse({'success': 'Brand Added'})
        elif action == 'get' and select == 'Model':
            type_id = request.POST.get('typeId', None)
            brand_id = request.POST.get('brandId', None)

            models = EquipmentBrandModel.objects.filter(type=type_id, brand=brand_id).values('id','name', 'description')
            return JsonResponse(list(models), safe=False)
        return JsonResponse({'error': 'Invalid Request'})
