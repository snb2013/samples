import json
import logging
import os
import requests
import time
from threading import RLock, Thread
from pathlib import Path
from queue import Queue

THREAD_COUNT = 4


class SendRequest(Thread):

    def __init__(self, queue, lock):
        """Инициализация потока"""
        Thread.__init__(self)
        self.queue = queue
        self.lock = lock

    def run(self):
        """Запуск потока"""
        while True:
            # Получаем строку из очереди
            line = self.queue.get()
            # вызываем функцию отправки запросов по конфигу
            self.send_request(line)
            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def check_and_write_id(self, id):
        with self.lock:
            ids = [w for w in Path("id.txt").read_text(encoding="utf-8").replace("\n", " ").split()]
            if id not in ids:
                file2 = open("id.txt", "a")
                file2.write(str(id) + '\n')
                file2.close()
            else:
                logging.info(f"Ошибка: запрос с id {id} уже был направлен")

    def send_request(self, line):

        config_clients = {
            "foo": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/1/"],
            "bar": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/2/"],
            "baz": ["https://yachtclubparus.ru/test/2/", "https://yachtclubparus.ru/test/1/"]
        }
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")

        jline = json.loads(line.rstrip('\n'))
        list_url = config_clients.get(jline['client_id'])
        # получаем список адресов из конфига для отправки запросов
        if jline['client_id'] and jline['payload'] and jline['client_id'] in config_clients.keys():
            # проверяем на выполнение нужных условий
            if jline.get('id'):
                # формируем список уникальных id или выдаем сообщение об ошибке
                self.check_and_write_id(jline['id'])
            for i in range(len(list_url)):
                # начинаем перебирать адреса из конфига и отправлять на них последовательно запросы
                logging.info(f"Отправляем запрос {jline['payload']} на адрес: {list_url[i]}")
                response = requests.post(list_url[i], data=jline['payload'])
                if response.status_code != 200:
                    # если вернулся не код 200 начинаем удваивать интервал времени и повторять запросы
                    time_size = 1
                    while response.status_code != 200:
                        time.sleep(time_size)
                        time_size *= 2
                        logging.info(
                            f"Увеличиваем время отправки запроса {jline['payload']} на адрес {list_url[i]} до: {time_size} секунд")
                        response = requests.post(list_url[i], data=jline['payload'])
                    logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен")
                else:
                    logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен")
        else:
            logging.info(f"Обработка запроса: Client_ID: {jline['client_id']}, playload: {jline['payload']} - ошибка")


def http_post():
    # Зачем создавать пустые файлы?
    # open('id.txt', 'w').close()
    # open('sample.log', 'w').close()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = os.path.join(dir_path, "requests.txt")
    queue = Queue()
    lock = RLock()
    for j in range(THREAD_COUNT):
        t = SendRequest(queue, lock)
        t.daemon = True
        t.start()
    with open(lines, 'r') as fp:
        for n, line in enumerate(fp, 1):
            queue.put(line)
    queue.join()


http_post()
