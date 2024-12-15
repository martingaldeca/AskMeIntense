class NotValidQuestionStatusForApproveOrDeny(Exception):

    def __init__(self, question):
        self.question = question
        self.message = (
            f"Question status '{self.question.status}' is not valid, "
            f"status must be '{self.question.StatusChoices.STATUS_PENDING_REVIEW}'"
        )

        super().__init__(self.message)
