from django.db import models


class QuestionList(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=255)
    list = models.ForeignKey(QuestionList, on_delete=models.CASCADE,
                             related_name='questions')
    parent_answer = models.ForeignKey('Answer', on_delete=models.CASCADE,
                                      related_name='questions', null=True,
                                      blank=True)

    class Meta:
        ordering = ('text',)

    def __str__(self):
        return '%s on %s' % (self.text, self.parent_answer.text) \
            if self.parent_answer else self.text


class Answer(models.Model):
    text = models.CharField(max_length=255)
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                        related_name='answers')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('parent_question', 'order')

    def __str__(self):
        return '%s on %s' % (self.text, self.parent_question.text)
