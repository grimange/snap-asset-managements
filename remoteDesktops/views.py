import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from remoteDesktops.models import Desktop

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
    """Receives data from PowerShell"""
    try :
        data = request.data
        data['geo_location']['ip_address'] = get_client_ip(request)
        Desktop.objects.record(request.data)
    except Exception as error:
        return Response({"error": str(error)}, status=400)
    return Response({"message": "Data received successfully"}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            # Save file or process it
            return Response({"message": "File uploaded successfully", "filename": file.name})
        return Response({"error": "No file uploaded"}, status=400)

