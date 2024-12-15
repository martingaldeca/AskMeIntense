from core.api.serializers import MeSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated


@extend_schema(
    tags=["token"],
)
class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@extend_schema(
    tags=["users"],
)
class MeDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
