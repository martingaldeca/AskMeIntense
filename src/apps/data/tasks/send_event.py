from core.models import User
from data.events import events

from backend.celery_backend.celery import app


@app.task(bind=True, max_retries=3)
def send_event(
    self,
    event_type: str,
    user_identifier: str = None,
    extra_info=None,
    user_properties=None,
    request_headers=None,
    app_version="0.0.0",
    location=None,
    device=None,
    update_user_profile=False,
):
    if (
        request_headers is not None
        and (store := request_headers.get("_store"))
        and (appversion := store.get("appversion"))
    ):
        app_version = appversion[1]
    if update_user_profile:
        user = User.objects.get(uuid=user_identifier)
        user_properties = {
            "email": user.user.email,
            "username": user.user.username,
            "first_name": user.user.first_name,
            "last_name": user.user.last_name,
        }

    events[event_type](
        user_identifier=user_identifier,
        extra_info=extra_info,
        user_properties=user_properties,
        app_version=app_version,
        location=location,
        device=device,
    ).send()


def rsync_user_properties():
    for user in User.objects.all():
        user_properties = {
            "email": user.user.email,
            "username": user.user.username,
            "first_name": user.user.first_name,
            "last_name": user.user.last_name,
        }
        events["rsync_user_properties_event"](
            user_identifier=user.uuid.hex,
            user_properties=user_properties,
        ).send()
