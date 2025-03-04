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
        elif select == 'Brand' and action == 'add':
            name = str(request.POST.get('name', None)).lower()
            if select == 'Brand' and not EquipmentBrand.objects.filter(name=name).exists():
                EquipmentBrand.objects.create(name=name)
                return JsonResponse({'success': 'Brand Added'})
            else:
                return JsonResponse({'error': 'Brand Already Exists'}, status=400)
        elif action == 'get' and select == 'Model':
            type_id = request.POST.get('typeId', None)
            brand_id = request.POST.get('brandId', None)

            models = EquipmentBrandModel.objects.filter(type=type_id, brand=brand_id).values('id','name', 'description')
            return JsonResponse(list(models), safe=False)
        elif action == 'add' and select == 'Model':
            type_id = request.POST.get('typeId', None)
            brand_id = request.POST.get('brandId', None)
            name = str(request.POST.get('name', None)).lower()
            description = str(request.POST.get('description', None))

            if EquipmentBrandModel.objects.filter(name=name, brand_id=brand_id, type_id=type_id).exists():
                return JsonResponse({'error': 'Model Already Exists'}, status=400)
            else:
                EquipmentBrandModel.objects.create(type_id=type_id, brand_id=brand_id, name=name, description=description)
                return JsonResponse({'success': 'Model Added'})
        return JsonResponse({'error':
                                 {'message': 'Invalid Request', 'action': action, 'select': select}
                             }, status=400)
