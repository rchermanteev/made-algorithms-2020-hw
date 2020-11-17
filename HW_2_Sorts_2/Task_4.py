"""
D. Гриша после дискотеки
ограничение по времени на тест2 секунды
ограничение по памяти на тест512 мегабайт
вводстандартный ввод
выводстандартный вывод
На следующий день после дискотеки Гриша решил устроить детям «взрыв мозга». Он взял много карточек и написал на каждой
из них одну латинскую букву в нижнем регистре. А после этого придумал свою строку и задал детям задание: составить как
можно больше подстрок своей строки, используя карточки. Гришина строка состоит только из букв латинского алфавита в
нижнем регистре. Вам нужно определить сколько её подстрок можно составить, используя только данные карточки.

Запишем буквы, написанные на карточках, подряд друг за другом. Тогда если Гришина строка — это «aaab», а карточки — это
«aba», то можно составить три подстроки «a», подстроку «b», две подстроки «aa» и подстроки «ab» и «aab». А подстроки
«aaa» и «aaab» нельзя, так как есть всего две карточки с буквой «a».
"""

from typing import List, Iterable


def get_counting_list(arr: Iterable[str], min_: int, max_: int) -> List[int]:
    len_cl = max_ - min_ + 1
    counting_list = [0] * len_cl
    for el in arr:
        counting_list[ord(el) - min_] += 1

    return counting_list


def is_substring(cnt_substr: List[int], cnt_voc: List[int]) -> bool:
    for i in range(len(cnt_voc)):
        if cnt_substr[i] > cnt_voc[i]:
            return False
    return True


# O(n^2)
# def counting_substring(str_, voc):
#     count_substr = 0
#     min_el, max_el = ord('a'), ord('z')
#     cnt_voc = get_counting_list(voc, min_el, max_el)
#     for step in range(1, len(voc) + 1):
#         for i in range(len(str_) - step + 1):
#             cnt_substring = get_counting_list(string[i: i + step], min_el, max_el)
#             if is_substring(cnt_substring, cnt_voc):
#                 count_substr += 1
#
#     return count_substr

def counting_substring(str_: str, voc: str) -> int:
    _MIN_EL, _MAX_EL = ord('a'), ord('z')
    count_substr = 0
    cnt_voc = get_counting_list(voc, _MIN_EL, _MAX_EL)
    cnt_substring = get_counting_list(str_[0], _MIN_EL, _MAX_EL)
    i, j = 0, 0
    len_str = len(str_)
    while j < len_str:
        sub_str = str_[i: j + 1]
        if is_substring(cnt_substring, cnt_voc):
            j += 1
            count_substr += len(sub_str)
            if j < len_str:
                cnt_substring[ord(str_[j]) - _MIN_EL] += 1
        elif i == j:
            j += 1
            if j < len_str:
                cnt_substring[ord(str_[j]) - _MIN_EL] += 1
        else:
            cnt_substring[ord(str_[i]) - _MIN_EL] -= 1
            i += 1

    return count_substr


len_data, len_vocabulary = map(int, input().split())
string = input()
vocabulary = input()

print(counting_substring(string, vocabulary))
