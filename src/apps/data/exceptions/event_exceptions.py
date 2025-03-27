class NotValidEventException(Exception):

    def __init__(self, event_type):
        self.event_type = event_type
        self.message = f"Event type '{self.event_type.status}' is not valid"

        super().__init__(self.message)
