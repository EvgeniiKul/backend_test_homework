from typing import List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    text = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.1f} ч.; '
        'Дистанция: {distance:.1f} км; '
        'Ср. скорость: {speed:.1f} км/ч; '
        'Потрачено ккал: {calories:.1f}.'
    )

    def get_message(self) -> str:
        return self.text.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    convert_to_min: int = 60

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
    COEF_CCAL_1_RUN: float = 18
    COEF_CCAL_2_RUN: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEF_CCAL_1_RUN * self.get_mean_speed()
                 - self.COEF_CCAL_2_RUN)
                * self.weight / self.M_IN_KM
                * self.duration * self.convert_to_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_CCAL_1_WALK: float = 0.035
    COEF_CCAL_2_WALK: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEF_CCAL_1_WALK * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.COEF_CCAL_1_WALK * self.weight)
                * self.duration * self.convert_to_min)


class Swimming(Training):
    """Тренировка: плавание."""

    COEF_CCAL_1_SWIM: float = 1.1
    COEF_CCAL_2_SWIM: int = 2
    LEN_STROKE: float = 1.38

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

        return ((self.get_mean_speed() + self.COEF_CCAL_1_SWIM)
                * self.COEF_CCAL_2_SWIM * self.weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STROKE / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: List[Tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
