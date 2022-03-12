import json, time, logging, requests
import os
import threading
from threading import Lock, Thread
from pathlib import Path
from queue import Queue


class SendRequest(threading.Thread):

    def __init__(self, queue):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = threading.Lock()

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
        # функция проверяет наличие ID в списке и если его там нет записывает его в список
        # self.lock.acquire()
        # try:
        #     # 1 вариант
        #     ids = []
        #     ids = [w for w in Path("id.txt").read_text(encoding="utf-8").replace("\n", " ").split()]
        #     # 2 вариант
        #     # write_id = True
        #     # with open("id.txt", "r") as file1:
        #     # # итерация по строкам
        #     #     for line1 in file1:
        #     #         if line1.rstrip('\n') == id:
        #     #             write_id = False
        #     if not id in ids:
        #         file2 = open("id.txt", "a")
        #         file2.write(id + '\n')
        #         file2.close()
        #     else:
        #         logging.info(f"Ошибка: запрос с id {id} уже был направлен")
        # finally:
        #     self.lock.release()
        with self.lock:
            ids = []
            ids = [w for w in Path("id.txt").read_text(encoding="utf-8").replace("\n", " ").split()]
            if not id in ids:
                file2 = open("id.txt", "a")
                file2.write(id + '\n')
                file2.close()
            else:
                logging.info(f"Ошибка: запрос с id {id} уже был направлен")

    def send_request(self, line):

        config_clients = {
            "foo": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/1/"],
            "bar": ["https://yachtclubparus.ru/test/", "https://yachtclubparus.ru/test/2/"],
            "baz": ["https://yachtclubparus.ru/test/2/", "https://yachtclubparus.ru/test/1/"]
        }
        logging.basicConfig(filename="sample.log", level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")

        jline = json.loads(line.rstrip('\n'))
        list_url = config_clients.get(jline['client_id'])
        # получаем список адресов из конфига для отправки запросов
        if jline['client_id'] and jline['payload'] and jline['client_id'] in config_clients.keys():
            # проверяем на выполнение нужных условий
            if jline['id']:
                # формируем список уникальных id или выдаем сообщение об ошибке
                self.check_and_write_id(jline['id'])
            for i in range(len(list_url)):
                # начинаем перебирать адреса из конфига и отправлять на них последовательно запросы
                logging.info(f"Отправляем запрос {jline['payload']} на адрес: {list_url[i]}")
                response = requests.post(list_url[i], data=jline['payload'])
                print(response.status_code)
                if response.status_code != 200:
                    # если вернулся не код 200 начинаем удваивать интервал времени и повторять запросы
                    time_size = 1
                    while response.status_code != 200:
                        time.sleep(time_size)
                        time_size = time_size * 2
                        logging.info(
                            f"Увеличиваем время отправки запроса {jline['payload']} на адрес {list_url[i]} до: {time_size} секунд")
                        response = requests.post(list_url[i], data=jline['payload'])
                    logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен")
                else:
                    logging.info(f"Запрос {jline['payload']} на адрес: {list_url[i]} успешно выполнен")
        else:
            logging.info(f"Обработка запроса: Client_ID: {jline['client_id']}, playload: {jline['payload']} - ошибка")


def http_post():
    open('id.txt', 'w').close()
    open('sample.log', 'w').close()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = os.path.join(dir_path, "sample.txt")
    queue = Queue()
    for j in range(4):
        t = SendRequest(queue)
        t.daemon = True
        t.start()
    with open(lines, 'r') as fp:
        for n, line in enumerate(fp, 1):
            queue.put(line)
    queue.join()


http_post()
