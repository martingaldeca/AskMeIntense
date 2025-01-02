from django.db import models


class CustomQuestionReactionManager(models.Manager):
    @property
    def liked(self):
        from questions.models import QuestionReaction

        return self.filter(reaction=QuestionReaction.ReactionChoices.LIKE)

    @property
    def disliked(self):
        from questions.models import QuestionReaction

        return self.filter(reaction=QuestionReaction.ReactionChoices.DISLIKE)

    @property
    def favorite(self):
        from questions.models import QuestionReaction

        return self.filter(reaction=QuestionReaction.ReactionChoices.FAVORITE)
