"""
The task is to implement an elevator driver.
Elevator moves between floors (up & down). There are button for each floor in the
elevator cabin (no buttons to open/close the doors). On each floor there are
2 buttons UP & DOWN (1 button for the highest floor DOWN and 1 for the lowest UP).
The elevator should move according to the floors selected by users,
but no user should have priority and each user should be able to go to the desired
floor (i.e. if there is 25 floors in the building, users on each floor should have
the same priority; also there should be no possibility to stop the elevator from
moving to users that are not inside of the cabin e.g. by moving between 2nd & 3rd
floor endlessly).
Implementation notes:
- Start updating the template code in Elevator class (see comments) if you need
	additional methods - implement it after Elevator.__init__
- If elevator is not moving get_current_direction returns DIRECTION_NONE
- get_current_floor called from on_before_floor returns the floor number that was
	before the floor for which on_before_floor is called (i.e. if the elevator goes up
	after the 2nd floor, and on_before_floor is called for the 3rd floor,
	get_current_floor will return 2)
- move_up & move_down functions starts movement and are not discrete (i.e. if
	move_up is called you should explicitly provide stop conditions and stop the
	elevator - it doesn't move the elevator up by one floor).
- Docstrings and comments in your code are appreciated.
"""

import time

DIRECTION_DOWN, DIRECTION_NONE, DIRECTION_UP = -1, 0, 1


class HardwareElevator:
    """This is the hardware elevator (engine) which provides an interface
    for the main business logic programmed in Elevator.
    This class cannot and MUST NOT be changed.
    """

    def __init__(self):
        self.on_cabin_button_pressed = None
        self.on_floor_button_pressed = None
        self.current_floor = 1
        self.current_direction = DIRECTION_NONE
        self.on_doors_closed = None
        self.on_before_floor = None

    def move_up(self):
        self.current_direction = DIRECTION_UP

    def move_down(self):
        self.current_direction = DIRECTION_DOWN

    def stop_and_open_doors(self):
        self.current_direction = DIRECTION_NONE

    def set_doors_closed_callback(self, callback):
        """Set a function to be called when the doors automatically close.
        """
        self.on_doors_closed = callback

    def set_before_floor_callback(self, callback):
        """Set a function to be called when the elevator is about to arrive
        to a floor.
        NOTE: self.get_current_floor() will return at this moment not the
        floor the elevator is about to arrive to.
        """
        self.on_before_floor = callback

    def set_floor_button_callback(self, callback):
        """Set a function to be called when someone presses a button on a floor.
        The callback is passed the floor number and the desired direction.
        """
        self.on_floor_button_pressed = callback

    def set_cabin_button_callback(self, callback):
        """Set a function to be called when someone presses a button inside the
        cabin.
        The callback is passed the desired floor number.
        """
        self.on_cabin_button_pressed = callback

    def get_current_floor(self):
        return self.current_floor

    def get_current_direction(self):
        """Return the direction in which the elevator is currently moving.
        When the elevator is stopped on a floor, the direction is None.
        """
        return self.current_direction


class Elevator:
    def __init__(self):
        self.elevator = HardwareElevator()
        self.elevator.set_doors_closed_callback(self.on_doors_closed)
        self.elevator.set_before_floor_callback(self.on_before_floor)
        self.elevator.set_floor_button_callback(self.on_floor_button_pressed)
        self.elevator.set_cabin_button_callback(self.on_cabin_button_pressed)
        self.floor_button_press = [[], []]
        self.cabin_button_press = []
        self.on_active = None
        self.need_direction = 0

    def on_doors_closed(self):
        # your code here
        if self.elevator.get_current_direction() == 0 and (self.floor_button_press[0] or self.cabin_button_press):
            # лифт стоит, но есть нажатые кнопки

            if self.on_active == "floor":
                if self.elevator.get_current_floor() > self.floor_button_press[0][0]:
                    # лифт стоит выше этажа откуда вызывают
                    self.need_direction = -1
                elif self.elevator.get_current_floor() < self.floor_button_press[0][0]:
                    # лифт стоит ниже этажа откуда вызывают
                    self.need_direction = 1
                else:
                    self.elevator.stop_and_open_doors()

            elif self.on_active == "cabin":
                if self.elevator.get_current_floor() > self.cabin_button_press[0]:
                    # лифт стоит выше этажа откуда вызывают
                    self.need_direction = -1
                elif self.elevator.get_current_floor() < self.cabin_button_press[0]:
                    # лифт стоит ниже этажа откуда вызывают
                    self.need_direction = 1
                else:
                    self.elevator.stop_and_open_doors()
            else:
                if self.cabin_button_press:
                    # Если остались нажатые кнопки в кабине лифта. Сначала проверяем их, потому что приоритет за кабиной
                    self.on_active = "cabin"
                    if self.elevator.get_current_floor() > self.cabin_button_press[0]:
                        # лифт стоит выше этажа откуда вызывают
                        self.need_direction = -1
                    elif self.elevator.get_current_floor() < self.cabin_button_press[0]:
                        # лифт стоит ниже этажа откуда вызывают
                        self.need_direction = 1
                    else:
                        self.elevator.stop_and_open_doors()
                elif self.floor_button_press[0]:
                    self.on_active = "floor"
                    if self.elevator.get_current_floor() > self.floor_button_press[0][0]:
                        # лифт стоит выше этажа откуда вызывают
                        self.need_direction = -1
                    elif self.elevator.get_current_floor() < self.floor_button_press[0][0]:
                        # лифт стоит ниже этажа откуда вызывают
                        self.need_direction = 1
                    else:
                        self.elevator.stop_and_open_doors()

    def on_before_floor(self):
        # your code here

        if len(self.cabin_button_press) > 1 and self.elevator.get_current_floor() in self.cabin_button_press:
            # если нажато несколько кнопок в кабине, можно высадить тех, кто раньше выходит
            self.elevator.stop_and_open_doors()
            print("Высадили пассажира на", self.elevator.get_current_floor(), "этаже")
            index = self.cabin_button_press.index(self.elevator.current_floor)
            # ищем тот этаж, на котором высадили и удаляем из списка
            del self.cabin_button_press[index]

        if self.cabin_button_press and self.on_active == "cabin" and \
                self.cabin_button_press[0] == self.elevator.get_current_floor():
            self.elevator.stop_and_open_doors()
            print('Вы приехали на', self.elevator.get_current_floor(), 'этаж')
            del self.cabin_button_press[0]
            self.need_direction = 0
            if not self.cabin_button_press:
                # проверяем есть ли еще нажатые кнопки в лифте, пока всех пассажиров не развезем
                # лифт не остановится и не передаст управление кнопкам на этаже
                self.on_active = None

        if self.floor_button_press[0] and self.on_active == "floor" \
                and self.floor_button_press[0][0] == self.elevator.get_current_floor():
            # приехал вызываемый нами лифт
            self.elevator.stop_and_open_doors()
            print('К Вам приехал лифт на', self.elevator.get_current_floor(), 'этаж')
            del self.floor_button_press[0][0]
            del self.floor_button_press[1][0]
            self.need_direction = 0
            # удаляем 2 элемента списка (этаж и направление), потому что задача выполнена.
            self.on_active = None

        if self.elevator.get_current_direction() == 1 or self.need_direction == 1:
            self.need_direction = 1
            self.elevator.move_up()
            self.elevator.current_floor = self.elevator.current_floor + 1
        if self.elevator.get_current_direction() == -1 or self.need_direction == -1:
            self.need_direction = -1
            self.elevator.move_down()
            self.elevator.current_floor = self.elevator.current_floor - 1

    def on_floor_button_pressed(self, floor, direction):
        # your code here
        self.floor_button_press[0].append(floor)
        self.floor_button_press[1].append(direction)
        if self.on_active != "cabin":
            self.on_active = "floor"

    def on_cabin_button_pressed(self, floor):
        # your code here
        self.cabin_button_press.append(floor)
        if self.on_active != "floor":
            self.on_active = "cabin"


def elevator_job():
    el = Elevator()
    hw = el.elevator

    time_for_job = 50
    # условная переменная для ограничения времени работы лифта, чтобы не было бесконечного цикла
    time_size = 1
    # продолжительность в секундах условной переменной
    time_on_cabin_button_pressed = [3, 5, 10]
    # через сколько секунд после начала работы лифта нажмут кнопку в лифте
    floor_cabin = [5, 4, 8]
    # какая кнопка будет нажата в кабине лифта
    time_on_floor_button_pressed = [5, 8, 9]
    # через сколько секунд после начала работы нажмут кнопку на этаже
    floor_and_direction = [[3, 8, 7], [-1, 1, 1]]
    # какая кнопка и какое направление будет нажато на этаже
    cab = 0
    # счетчик, учитывающий порядковый номера этажей, на которых нажата кнопка вызова лифта
    fl = 0

    print("Лифт начал работу")

    for i in range(1, time_for_job):
        time.sleep(time_size)
        # задерживаем на единицу времени

        if i in time_on_floor_button_pressed:
            # пришло время нажать кнопку на этаже
            hw.on_floor_button_pressed(floor_and_direction[0][fl], floor_and_direction[1][fl])
            fl += 1

        if i in time_on_cabin_button_pressed:
            # пришло время нажать кнопку в кабине лифта
            hw.on_cabin_button_pressed(floor_cabin[cab])
            cab += 1

        hw.on_before_floor()
        hw.on_doors_closed()

    print("Лифт закончил работу")


elevator_job()
