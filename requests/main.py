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
        self.next_request = False

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
                self.next_request = True
    
    def autosave_request(self, list_url, payload):
        with self.lock:
            with open("autosave.txt", "a") as f:
                d = {
                    "url": list_url,
                    "payload": payload
                }
                l = json.dumps(d)
                f.write("%s\n" % l)

    def remove_request(self, list_url, payload):
        with self.lock:
            with open("autosave.txt", 'r') as fp:
                for n, line1 in enumerate(fp, 1):
                    jline1 = json.loads(line1.rstrip('\n'))
                    if jline1['url'] == list_url and jline1['payload'] == payload:
                        number_str = n - 1
                        break
            with open("autosave.txt", "r") as file:
                lines2 = file.readlines()
            del lines2[number_str]
            with open("autosave.txt", "w") as file:
                file.writelines(lines2)

    def send_request(self, line):

        config_clients = {
            "foo": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/1/"],
            "bar": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/2/"],
            "baz": ["https://yachtclubparus.ru/test/2/", "https://yachtclubparus.ru/test/1/"]
        }
        logging.basicConfig(filename='requests.log', level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")

        jline = json.loads(line.rstrip('\n'))
        list_url = config_clients.get(jline['client_id'])
        # получаем список адресов из конфига для отправки запросов
        if jline['client_id'] and jline['payload'] and jline['client_id'] in config_clients.keys():
            # проверяем на выполнение нужных условий
            if jline.get('id'):
                # формируем список уникальных id или выдаем сообщение об ошибке
                self.check_and_write_id(jline['id'])
            if not self.next_request:
                # если запрос на такой ID был, пропускаем его
                for i in range(len(list_url)):
                    # начинаем перебирать адреса из конфига и отправлять на них последовательно запросы
                    logging.info(f"Отправляем запрос {jline['payload']} на адрес: {list_url[i]}")
                    response = requests.post(list_url[i], data=jline['payload'])
                    self.autosave_request(list_url[i], jline['payload'])
                    # сохраняем строку во временный файл
                    if response.status_code != 200:
                        # если вернулся не код 200 начинаем удваивать интервал времени и повторять запросы
                        time_size = 1
                        while response.status_code != 200:
                            time.sleep(time_size)
                            time_size *= 2
                            logging.info(
                                f"Увеличиваем время отправки запроса {jline['payload']} на адрес {list_url[i]} до: {time_size} секунд")
                            response = requests.post(list_url[i], data=jline['payload'])
                    #     logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен.")
                    # else:
                    #     logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен.")
                    self.remove_request(list_url[i], jline['payload'])
                    logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен.")
            self.next_request = False
            # переключаем флаг, чтобы следующий запрос мог уйти
        else:
            logging.info(f"Обработка запроса: Client_ID: {jline['client_id']}, playload: {jline['payload']} - ошибка")

    def send_request_autosave(self, line):

        logging.basicConfig(filename='requests.log', level=logging.INFO,
                                format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")

        jline = json.loads(line.rstrip('\n'))
        logging.info(f"Отправляем запрос {jline['payload']} на адрес: {jline['url']}")
        response = requests.post(jline['url'], data=jline['payload'])
        if response.status_code != 200:
            # если вернулся не код 200 начинаем удваивать интервал времени и повторять запросы
            time_size = 1
            while response.status_code != 200:
                time.sleep(time_size)
                time_size *= 2
                logging.info(f"Увеличиваем время отправки запроса {jline['payload']} на адрес {jline['url']} до: {time_size} секунд")
                response = requests.post(jline['url'], data=jline['payload'])
            self.remove_request(jline['url'], jline['payload'])
            logging.info(f"Запрос {jline['payload']} на адрес: {jline['url']} успешно выполнен.")


def http_post():
    # смотрим есть ли сохраненные неотправленные запросы, если да, то отправляем в один поток, не заморчаиваемся
    if os.stat("autosave.txt").st_size:
        with open("autosave.txt", 'r') as fp:
            for n, line in enumerate(fp, 1):
                logging.basicConfig(filename='requests.log', level=logging.INFO,
                                        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
                jline = json.loads(line.rstrip('\n'))
                logging.info(f"Отправляем запрос {jline['payload']} на адрес: {jline['url']}")
                response = requests.post(jline['url'], data=jline['payload'])
                if response.status_code != 200:
                    time_size = 1
                    while response.status_code != 200:
                        time.sleep(time_size)
                        time_size *= 2
                        logging.info(f"Увеличиваем время отправки запроса {jline['payload']} на адрес {jline['url']} до: {time_size} секунд")
                        response = requests.post(jline['url'], data=jline['payload'])
                logging.info(f"Запрос {jline['payload']} на адрес: {jline['url']} успешно выполнен.")
        # очищаем файл
        f = open('autosave.txt', 'w')
        f.close()

    queue = Queue()
    lock = RLock()
    for j in range(THREAD_COUNT):
        t = SendRequest(queue, lock)
        t.daemon = True
        t.start()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = os.path.join(dir_path, "requests.txt")

    with open(lines, 'r') as fp:
        for n, line in enumerate(fp, 1):
            queue.put(line)
    queue.join()


http_post()
