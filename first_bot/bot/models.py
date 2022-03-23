from django.db import models

# Create your models here.
from django.db import models


class Dialog(models.Model):
    parent_id = models.IntegerField(default=0)
    # связь между элементами
    choice_text = models.CharField(max_length=100)
    # выбор в меню
    answer_text = models.CharField(max_length=100)
    # ответ бота
