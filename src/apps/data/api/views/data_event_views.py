from data.api.serializers import DataEventSerializer
from data.tasks import send_event
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    tags=["data"],
)
class DataEventView(APIView):
    serializer_class = DataEventSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_event.delay(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
