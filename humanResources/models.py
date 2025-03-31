import os
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

class HrRequestCategoryManager(models.Manager):
    def get_select_categories(self):
        categories =  self.filter(is_active=True)
        data = []
        if categories:
            for category in categories:
                subs = category.hrrequestsubcategory_set.filter(is_active=True)
                cat = {'id': category.id,'name': category.name}
                cat_sub = []
                for sub in subs:
                    cat_sub.append({'id': sub.id, 'name': sub.name, 'clickable': sub.clickable == True})
                data.append({'category': cat, 'subs': cat_sub})
        return data

class HRRequestCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = HrRequestCategoryManager()

class HRRequestSubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(HRRequestCategory, null=True, on_delete=models.CASCADE)
    clickable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class HRRequestNewManager(models.Manager):
    def get_all_by_list(self):
        newList = self.all()

class HRRequestNew(models.Model):
    sub_category = models.ForeignKey(HRRequestSubCategory, on_delete=models.CASCADE)
    notes = models.TextField()
    handled_by = models.ForeignKey(get_user_model(), related_name='handler', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='new')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = HRRequestNewManager()

class HrRequestFilesManager(models.Manager):
    @staticmethod
    def __getSubCategory(sub_category_id):
        return HRRequestSubCategory.objects.get(id=sub_category_id)

    def save_new_request(self, sub_category_id, notes, user, files):
        sub_category = self.__getSubCategory(sub_category_id)
        newRequest = HRRequestNew.objects.create(sub_category=sub_category, notes=notes, created_by=user)
        if files:
            uploaded_folder = f"static/assets/uploaded_files/{user.username}/{sub_category.name}/"

            if not os.path.exists(uploaded_folder):
                os.makedirs(uploaded_folder)

            today = datetime.today().strftime("%Y%m%d%H%M%S")
            uploaded_files = files.getlist("files")
            for file in uploaded_files:
                fileName = f"{today}-{file.name}"
                file_path = os.path.join(uploaded_folder, fileName)
                self.create(newRequest=newRequest, name=fileName, size=file.size, content_type=file.content_type,
                            file_path=file_path, created_by=user)
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
        hrRequestList = HRRequestNew.objects.filter(created_by=user)
        data = []
        if hrRequestList:
            for hrRequest in hrRequestList:
                data.append({'id': hrRequest.id, 'notes': hrRequest.notes})
        return data

class HrRequestFiles(models.Model):
    new_request = models.ForeignKey(HRRequestNew, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    content_type = models.CharField(max_length=100)
    file_path = models.TextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = HrRequestFilesManager()
