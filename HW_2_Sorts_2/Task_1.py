"""
k -я имперская порядковая статистика
ограничение по времени на тест1.2 секунд
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Батальон клонов вышел на построение. Все имперцы стали в один ряд и пересчитались: первый, второй, третий, …, n-й.
Каждый из них держит в руках бумажку с результатом своего тестирования IQ. Как известно, результатом тестирования
IQ является число от 1 до 109.

Периодически к батальону подходит граф Дуко, размахивает мечом и делает запрос: «Если всех клонов с i-го по j-го
упорядочить по результату теста, то какое значение будет у клона, стоящем на k-м месте?» — и быстро требует ответ,
грозя всю партию пустить в расход. Большая просьба — решите эту задачу и помогите клонам выжить.
"""
import random

from typing import List


def partition(arr: List[int], idx_left_bound: int, idx_right_bound: int) -> int:
    separating_element = arr[random.randint(idx_left_bound, idx_right_bound)]
    idx_left_bound -= 1
    idx_right_bound += 1
    while True:
        idx_left_bound += 1
        while arr[idx_left_bound] < separating_element:
            idx_left_bound += 1

        idx_right_bound -= 1
        while arr[idx_right_bound] > separating_element:
            idx_right_bound -= 1

        if idx_left_bound < idx_right_bound:
            arr[idx_left_bound], arr[idx_right_bound] = arr[idx_right_bound], arr[idx_left_bound]
        else:
            return idx_right_bound


def find(arr: List[int], idx_left_bound: int, idx_right_bound: int, k: int) -> int:
    def _find(arr_: List[int], idx_lb: int, idx_rb: int, k_: int):
        if idx_lb < idx_rb:
            idx_section = partition(arr_, idx_lb, idx_rb)
            if k_ <= idx_section:
                return _find(arr_, idx_lb, idx_section, k_)
            else:
                return _find(arr_, idx_section + 1, idx_rb, k_)

    _find(arr, idx_left_bound, idx_right_bound, idx_left_bound + k)
    return arr[idx_left_bound + k]


number_of_clones = int(input())
clones = list(map(int, input().split()))
number_request = int(input())
requests = []
for _ in range(number_request):
    requests.append(list(map(lambda x: int(x) - 1, input().split())))

for request in requests:
    print(find(clones.copy(), *request))
