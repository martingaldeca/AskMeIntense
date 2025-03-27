from data.events import FrontendDataEvent


class StartGameClickEvent(FrontendDataEvent):
    event_type = "start_game"
    description = "This event is triggered when any user clicks on start game button."
