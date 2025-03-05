import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_data(request):
    """Receives data from PowerShell"""
    try :
        data = request.data
        print(data['motherboard'])
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

