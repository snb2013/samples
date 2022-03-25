import json

from django.contrib.sessions.backends import file
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Команда приводит исходный файл к виду фикстуры'
    data = []

    def handle(self, *args, **options):
        name_file = options['file'][0]
        # получаем имя файла
        try:
            f = open(name_file)
            ff = f.read()
            ff = ff.replace("\n", "")
            ff = ff.replace("    ", "")
            ff = ff.replace("  ", "")
            parent = 1
            level = 0
            start = 0
            end = 0
            nom = 1
            for index in range(len(ff)):
                if ff[index] == "[":
                    if ff[index + 1] == "\"":
                        start = index
                if ff[index] == "]" or ff[index] == "[":
                    end = index
                if ff[index - 1] == "[":
                    level += 1
                if ff[index - 1] == "]":
                    level -= 1

                if start != 0 and end != 0 and start != end:
                    # нашли элемент для записи в БД, нужно его сохранить
                    line = ff[start + 1:end]
                    # определяем поля и сохраняем в список
                    parent = self.search_parent(level)
                    if line[-1] == ",":
                        line = line[:-1]
                    line = "[" + line + "]"
                    list_line = json.loads(line)
                    choice_text = list_line[0]
                    answer_text = list_line[1]
                    self.add_json(nom, parent, choice_text, answer_text, level)
                    nom += 1
                    start = 0
                    end = 0
            for line in self.data:
                # удаляем ненужный ключ
                del line['level']
            with open(name_file, "w") as fl:
                json.dump(self.data, fl)
        except FileNotFoundError:
            print("Файл не существует!")
        if len(options['file']) == 0:
            raise CommandError('Пустая строка')

    def search_parent(self, level):
        if level != 1:
            last = self.data[-1]
            # получаем последний элемент
            old_level = last['level']
            if level > old_level:
                return last['pk']
            elif level < old_level:
                start = 0
                for line in self.data:
                    field = line['fields']
                    if field['parent'] is None:
                        # ищем последний элемент верхнего уровня, все что до него нас уже не интересует
                        start = line['pk']
                for line in self.data:
                    if line['level'] == level and line['pk'] > start:
                        field = line['fields']
                        return field['parent']
            else:
                field = last['fields']
                return field['parent']

    def add_json(self, nom, parent, choice_text, answer_text, level):
        entry = {
            "model": "bot.Dialog",
            "pk": nom,
            "level": level,
            "fields": {
                "parent": parent,
                "choice_text": choice_text,
                "answer_text": answer_text
                }
            }
        self.data.append(entry)

    def add_arguments(self, parser):
        parser.add_argument(
            '-file',
            '-f',
            nargs=1,
            type=str,
            help='Укажите имя файла, включая полный путь до него'
        )
