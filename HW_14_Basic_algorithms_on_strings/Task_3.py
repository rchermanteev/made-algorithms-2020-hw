import sys

CHARACTER_OUTSIDE_ALPHABET = "#"


def search_substring_in_string(substr: str, string: str):
    mod_string = substr + CHARACTER_OUTSIDE_ALPHABET + string
    len_substr = len(substr)
    prefix_list = [0] * len(mod_string)
    answer = []
    for i in range(1, len(mod_string)):
        k = prefix_list[i - 1]
        while k > 0 and mod_string[i] != mod_string[k]:
            k = prefix_list[k - 1]

        if mod_string[i] == mod_string[k]:
            k += 1

        prefix_list[i] = k
        if k == len_substr:
            answer.append(i - len_substr * 2)

    return answer


def main():
    substring = sys.stdin.readline().rstrip()
    base_string = sys.stdin.readline().rstrip()
    starts_substr = search_substring_in_string(substring, base_string)
    print(len(starts_substr))
    print(" ".join(map(lambda x: str(x + 1), starts_substr)))


if __name__ == "__main__":
    main()
