from .base import (
    BackendDataEvent,
    DataEvent,
    FrontendDataEvent,
    RsyncUserPropertiesEvent,
)
from .front_events import StartGameClickEvent

# Document events
events = {
    DataEvent.event_type: DataEvent,
    RsyncUserPropertiesEvent.event_type: RsyncUserPropertiesEvent,
    # Front events
    StartGameClickEvent.event_type: StartGameClickEvent,
}
