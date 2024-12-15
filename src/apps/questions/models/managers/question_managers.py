from django.db import models


class CustomQuestionManager(models.Manager):
    @property
    def approved(self):
        from questions.models import Question

        return self.filter(status=Question.StatusChoices.STATUS_APPROVED)

    @property
    def denied(self):
        from questions.models import Question

        return self.filter(status=Question.StatusChoices.STATUS_DENIED)

    @property
    def pending_review(self):
        from questions.models import Question

        return self.filter(status=Question.StatusChoices.STATUS_PENDING_REVIEW)
