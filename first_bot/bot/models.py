from django.db import models

# Create your models here.
from django.db import models


class Dialog(models.Model):
    parent = models.ForeignKey('Dialog', on_delete=models.CASCADE, null=True, blank=True)
    # связь между элементами
    choice_text = models.CharField(max_length=100)
    # выбор в меню
    answer_text = models.CharField(max_length=100)
    # ответ бота

    def __str__(self):
        return self.choice_text
