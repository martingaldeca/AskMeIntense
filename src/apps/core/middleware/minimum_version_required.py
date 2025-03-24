import logging

import waffle
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from packaging import version
from packaging.version import InvalidVersion
from rest_framework import status

logger = logging.getLogger(__name__)


class MinimumVersionRequired:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        try:
            if waffle.switch_is_active("minimum_version_required_active") and not (
                "api/" not in request.path
                or "api/verify" in request.path
                or "api/data_event" in request.path
                or "api/schema" in request.path
                or "interested_user" in request.path
            ):
                app_version = request.headers.get("Appversion", "0.0.0")
                if version.parse(app_version) < version.parse(
                    settings.MINIMUM_REQUIRED_APP_VERSION_ANDROID
                ):
                    return JsonResponse(
                        data={"upgrade": settings.MINIMUM_REQUIRED_APP_VERSION_ANDROID},
                        status=status.HTTP_426_UPGRADE_REQUIRED,
                    )
                return self.get_response(request)
            else:
                return self.get_response(request)
        except InvalidVersion as exception:
            logger.error(exception)
            return JsonResponse(
                data={"error": str(exception)},
                status=status.HTTP_400_BAD_REQUEST,
            )
