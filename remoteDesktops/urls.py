from django.urls import path
from remoteDesktops.views import receive_data, FileUploadView, receive_chrome_data
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('receive-data/', receive_data, name='receive_data'),
    path('receive_chrome_data/', receive_chrome_data, name='receive_chrome_data'),
    path('upload-image/', FileUploadView.as_view(), name='upload-image'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
