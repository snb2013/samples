import json
import logging
import os
import requests
import time
from threading import RLock, Thread
from pathlib import Path
from queue import Queue

THREAD_COUNT = 4
REQUEST_FILE = 'requests.txt'
AUTOSAVE_FILE = 'autosave.txt'
ID_REQUEST_FILE = 'id.txt'
CLIENTS = {
    "foo": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/1/"],
    "bar": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/2/"],
    "baz": ["https://yachtclubparus.ru/test/2/", "https://yachtclubparus.ru/test/1/"]
}


def send_request(payload, listurl, number):
    logging.info(f"Отправляем запрос {payload} на адрес: {listurl}")
    response = requests.post(listurl, data=payload)
    # сохраняем строку во временный файл
    if response.status_code != 200:
        # если вернулся не код 200 начинаем удваивать интервал времени и повторять запросы
        time_size = 1
        while response.status_code != 200:
            time.sleep(time_size)
            time_size *= 2
            logging.info(
                f"Увеличиваем время отправки запроса {payload} на адрес {listurl} до: {time_size} секунд")
            response = requests.post(listurl, data=payload)
    logging.info(
        f"Запрос {payload} на адрес: {listurl} успешно выполнен. Строка {number} обработана")


class SendRequest(Thread):
    def __init__(self, queue, lock):
        """Инициализация потока"""
        Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.next_request = False
        # если запрос с таким ID уже был эта переменная принимает значение Истина

    def run(self):
        """Запуск потока"""
        while True:
            # Получаем строку из очереди
            line = self.queue.get()
            # вызываем функцию отправки запросов по конфигу
            self.job_request(line)
            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def check_and_write_id(self, id_request):
        with self.lock:
            if os.path.exists(ID_REQUEST_FILE):
                ids = [w for w in Path(ID_REQUEST_FILE).read_text(encoding="utf-8").replace("\n", " ").split()]
            else:
                ids = []

            if id_request not in ids:
                file2 = open(ID_REQUEST_FILE, "a")
                file2.write(str(id_request) + '\n')
                file2.close()
            else:
                logging.info(f"Ошибка: запрос с id {id_request} уже был направлен")
                self.next_request = True

    def autosave_request(self, list_url, payload, number):
        with self.lock:
            with open(AUTOSAVE_FILE, "a") as f:
                d = {
                    "url": list_url,
                    "payload": payload,
                    "number": number
                }
                h = json.dumps(d)
                f.write("%s\n" % h)

    def remove_request(self, list_url, payload, number):
        with self.lock:
            with open(AUTOSAVE_FILE, 'r') as fp:
                for n, line1 in enumerate(fp, 1):
                    jline1 = json.loads(line1.rstrip('\n'))
                    if jline1['url'] == list_url and jline1['payload'] == payload and jline1['number'] == number:
                        number_str = n - 1
                        break
            with open(AUTOSAVE_FILE, "r") as file:
                lines2 = file.readlines()
            del lines2[number_str]
            with open(AUTOSAVE_FILE, "w") as file:
                file.writelines(lines2)

    def job_request(self, jline):
        if 'client_id' in jline:
            # если client_id есть, значит это запрос из файла с запросами,
            # если нет - значит идет досылка из файла avtosave
            list_url = CLIENTS.get(jline['client_id'])
            # получаем список адресов из конфига для отправки запросов
            if jline['client_id'] and jline['payload'] and jline['client_id'] in CLIENTS.keys():
                # проверяем на выполнение нужных условий
                if jline.get('id'):
                    # формируем список уникальных id или выдаем сообщение об ошибке
                    self.check_and_write_id(jline['id'])
                if not self.next_request:
                    # если запрос на такой ID был, пропускаем его
                    for i in range(len(list_url)):
                        payload = jline['payload']
                        url = list_url[i]
                        number = jline['number']
                        self.autosave_request(url, payload, number)
                        # начинаем перебирать адреса из конфига и отправлять на них последовательно запросы
                        send_request(payload, url, number)
                        self.remove_request(url, payload, number)
                self.next_request = False
                # переключаем флаг, чтобы следующий запрос мог уйти
            else:
                logging.info(f"Обработка запроса: Client_ID: {jline['client_id']}, "
                             f"payload: {jline['payload']} - ошибка")
        else:
            payload = jline['payload']
            url = jline['url']
            number = jline['number']
            # logging.info(f"Отправка запроса из avtosave.txt payload: {payload} на адрес {url}")
            send_request(payload, url, number)


def http_post():
    # смотрим есть ли сохраненные неотправленные запросы, если да, то отправляем в один поток, не заморчаиваемся
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    save_str = 0
    # переменная, в которой будет храниться максимальный номер обработанной строки

    queue = Queue()
    lock = RLock()
    for j in range(THREAD_COUNT):
        t = SendRequest(queue, lock)
        t.daemon = True
        t.start()

    try:
        with open(AUTOSAVE_FILE) as fp:
            for n, line in enumerate(fp, 1):
                jline = json.loads(line.rstrip('\n'))
                save_str = max(save_str, jline['number'])
                queue.put(jline)
        os.remove(AUTOSAVE_FILE)
    except FileNotFoundError:
        pass

    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = os.path.join(dir_path, REQUEST_FILE)
    with open(lines, 'r') as fp:
        for n, line in enumerate(fp, 1):
            if n > save_str:
                line_number_row = json.loads(line.rstrip('\n'))
                line_number_row['number'] = n
                queue.put(line_number_row)
    queue.join()


http_post()
