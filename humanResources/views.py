from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from humanResources.models import HRRequestCategory, HrRequestFiles


# Create your views here.
class HrRequestMain(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'humanResources.view_hrrequestnew'

class HrRequestNewView(HrRequestMain):
    template_name = 'hr/index.html'

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)

        # print(request.user.get_all_permissions())
        if action == 'load_category':
            return JsonResponse(HRRequestCategory.objects.get_select_categories(), safe=False)
        if action == 'new_HrRequest':
            sub_category_id = request.POST.get('sub_category_id', None)
            notes = request.POST.get('notes', None)
            if request.FILES:
                files = request.FILES.getlist("files")
                results = HrRequestFiles.objects.save_new_request(sub_category_id=sub_category_id, notes=notes,
                                                                  user=request.user, files=files)
            return JsonResponse(results, safe=False)
        return JsonResponse({'error': {'message': 'Invalid Request', 'action': action} }, status=400)

