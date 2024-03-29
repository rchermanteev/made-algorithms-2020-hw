"""
Задача A. Королевская сортировка
Имя входного файла: стандартный ввод
Имя выходного файла: стандартный вывод
Ограничение по времени: 1 секунда
Ограничение по памяти: 256 мегабайт
У нерушимого города-государства Иннолэнд богатая история. Множество королей правило на
этой земле в течение многих веков. Город гордится своими предводителями, поэтому его жители
хотят выбить имя каждого из королей на особой плите в самом центре города (дабы заполнить хоть
чем-то пустующий и безлюдный город).
У каждого короля Иннолэнда помимо имени имеется порядковый номер. Этот номер записан в
римской системе счисления рядом с именем каждого короля великого города-государства. Например, Louis XIII был тринадцатым королем Иннолэнда, имеющим имя Louis (ох уж эти иннолэндовцы и их имена...).
Однако не все так просто устроено в этом городе. Жители Иннолэнда любят соблюдать порядок
во всем, поэтому должен соблюдаться и порядок имен на плите. Важно, чтобы имена на плите были
упорядочены в лексикографическом порядке. Однако некоторые короли могли иметь одно и то же
имя, поэтому короли с одинаковым именем они должны быть отсортированы в соответствии с их
порядковыми номерами. Например, славный король Louis IX должен быть указан на плите после
доблестного короля Louis VIII.
Жители Иннолэнда пока ещё плохо ладят с упорядочиванием имен и уж тем более с компьютерами, поэтому они обратились за помощью к Вам — Вы-то уже давно хорошо знакомы с этими
вещами. Они передали список имен всех королей, а Вы должны вернуть им тот же список, но имена в нем должны идти уже в нужном порядке: в желаемом списке раньше записаны те короли, у
которых имя лексикографически меньше, а среди королей с одинаковым именем раньше идут те, у
которых меньше порядковый номер.
Формат входных данных
В первой строке записано число n (1 ⩽ n ⩽ 50) — количество королей.
В следующих n строках записаны имена и порядковые номера королей. В каждой строке сначала
записано имя короля, состоящее из не более чем 20 латинских букв (первая буква имени прописная,
все последующие строчные), а затем через пробел записан его порядковый номер в виде римского
числа от 1 до 50.
Формат выходных данных
В n строках должны быть записаны имена и порядковые числа королей, упорядоченные необходимым образом.
"""


from typing import List

ROME_TO_ARABIC = {"L": 50, "X": 10, "V": 5, "I": 1}


def transform_rome_to_arabic(rome_number: str) -> int:
    temp_number = ROME_TO_ARABIC[rome_number[0]]
    arabic_number = 0
    for i in range(1, len(rome_number)):
        if not temp_number:
            temp_number = ROME_TO_ARABIC[rome_number[i]]

        if rome_number[i] == rome_number[i - 1]:
            temp_number += ROME_TO_ARABIC[rome_number[i]]
        elif ROME_TO_ARABIC[rome_number[i]] > temp_number:
            arabic_number += ROME_TO_ARABIC[rome_number[i]] - temp_number
            temp_number = 0
        elif ROME_TO_ARABIC[rome_number[i]] < temp_number:
            arabic_number += temp_number
            temp_number = ROME_TO_ARABIC[rome_number[i]]

    arabic_number += temp_number

    return arabic_number


def sort_kings(kings_: List[List[str]]) -> List[List[str]]:
    sorted_by_num = sorted(kings_, key=lambda x: transform_rome_to_arabic(x[1]))
    return sorted(sorted_by_num, key=lambda x: x[0])


number_kings = int(input())
kings = []
for _ in range(number_kings):
    kings.append(input().split())

print("\n".join(" ".join(king) for king in sort_kings(kings)))
