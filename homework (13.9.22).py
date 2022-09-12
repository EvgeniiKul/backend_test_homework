from dataclasses import dataclass
from typing import Dict, List, Tuple, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

    def get_message(self) -> str:
        """Отправить информационное сообщение о данных тренировки"""

        type: str = f'Тип тренировки: {self.training_type}; '
        duration: str = f'Длительность: {self.duration} ч.; '
        dist: str = f'Дистанция: {self.distance} км; '
        speed: str = f'Ср. скорость: {self.speed} км/ч; '
        calories: str = f'Потрачено ккал: {self.calories}.'
        message: str = type + duration + dist + speed + calories
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    LEN_STROKE: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    convert_to_min: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k_ccal_1_run: int = 18
        k_ccal_2_run: int = 20
        spent_ccal_run: float = ((k_ccal_1_run * self.get_mean_speed() - k_ccal_2_run)
                                 * self.weight / self.M_IN_KM
                                 * self.duration * self.convert_to_min)
        return spent_ccal_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    convert_to_min: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k_ccal_1_walk: float = 0.035
        k_ccal_2_walk: float = 0.029
        spent_ccal_walk: float = ((k_ccal_1_walk * self.weight
                                   + (self.get_mean_speed() ** 2 // self.height)
                                   * k_ccal_2_walk * self.weight)
                                  * self.duration * self.convert_to_min)
        return spent_ccal_walk


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k_ccal_1_swim: float = 1.1
        k_ccal_2_swim: int = 2
        return ((self.get_mean_speed() + k_ccal_1_swim)
                * k_ccal_2_swim * self.weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STROKE / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]]
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
