import time
from operator import itemgetter
from collections import namedtuple

def char_to_int(c):
    '''
    :param c string: A ~ Z 중에 알파벳 하나
    :return: A를 0으로 하는 알파벳의 포지션 리턴. B는 1이 될 것이다.
    :rtype: int
    '''
    return (ord(c) - ord('A'))


def count_bits(n):
    '''
    :param n : 정수
    :return: 정수를 bit로 표현 시 1의 개수를 리턴한다.
    :rtype: int
    '''
    return bin(n).count('1')


def num_of_matches(b1, b2):
    '''
    :param b1 b2 : 정수
    :return: b1, b2를 이진수로 표현 시, 1이 겹치는 개수를 리턴한다. 즉, intersection을 하여, 개수를
    센다고 보면 된다.
    :rtype: int
    '''
    inter = b1 & b2
    return count_bits(inter)


People = namedtuple('People', ('letters', 'bits', 'idx'))


def is_break(first_letters, second_letters, max_matches):
    '''
    max_matches를 기준으로 해가 될 가능성이 없는 케이스가 나오면
    추가 검색을 중지하도록 break 여부를 돌려준다.

    만약 first_letters의 값이 A B C D E 이고,
    max_matches가 2인 경우, second_letters의 첫 문자가 D(10-max_matches 위치에 있다)보다 큰 문자(E, F, G ...)일 경우,
    최대 matches 값은 기껏해야 1 (E가 겹치는 경우)이므로 이 다음 row는 비교할 필요가 없다.

    만약 비교 대상자의 첫 문자가 D와 같다면, 이제는 second_letters의 두번째 문자와 E와 비교해야 한다.

    두번째 문자가 E보다 크다면, matches 값은 1이 되므로 이 다음 row의 letters는 해가될 가능성이 없다.
    '''
    idx = 0
    while idx <= 9 and 10-max_matches+idx <= 9:
        if second_letters[idx] > first_letters[10-max_matches+idx]:
            return True
        elif second_letters[idx] == first_letters[10-max_matches+idx]:
            idx += 1
        else:
            return False
    return False


def match(people):
    # people은 정렬된 상태임을 기억하자.
    n = len(people)

    # n 값이 0이거나 1일 때는 해가 없다
    if n == 0 or n == 1:
        return []

    max_matches = 1
    first_total_match_position = 0
    result = []

    # 현재 row와 다음 row만 비교해 빠르게 max_matches 유사 값을 가져온다.
    # 10개 완전 매칭의 존재 여부는 100% 정확도로 확인할 수 있다.
    # O(n)에 실행되므로 매우 빠르다.
    for i in range(n-1):
        first = people[i][1]
        second = people[i+1][1]

        matches = num_of_matches(first, second)

        if matches > max_matches:
            max_matches = matches

            if max_matches == 10:
                # 10개의 매칭이 발견된 첫번째 포지션을 저장
                first_total_match_position = i
                break


    if max_matches == 10:
        # 최대 매칭 값이 10개면 연속된 row에 매칭 값이 위치한다!
        # 첫 10개의 매칭값이 발견한 된 position부터 시작한다.
        for i in range(first_total_match_position, n):
            first = people[i]
            first_bits = first.bits
            first_idx = first.idx
            for j in range(i+1, n):
                # i의 다음 열부터 비교를 하고, 한번이라도 같은 값이 아니면 for 구문을 벗어난다.
                second = people[j]
                second_bits = second.bits
                second_idx = second.idx
                if first_bits == second_bits:
                    result.append([first_idx, second_idx])
                    continue
                else:
                    break
    else:
        # 최대 매칭 값이 10개가 아닌 경우는 전체 검색을 한다. 
        # 정렬된 성질을 활용하여 휴리스틱으로 해의 검색 범위를 최대한 제한한다.(is_break 함수)
        for i in range(n):
            first = people[i]
            first_letters = first.letters
            first_bits = first.bits
            first_idx = first.idx

            for j in range(i+1, n):
                second = people[j]
                second_letters = second.letters
                if is_break(first_letters, second_letters, max_matches):
                    break

                second_bits = second.bits

                matches = num_of_matches(first_bits, second_bits)
                if matches > max_matches:
                    max_matches = matches
                    result = []
                    result.append([first_idx, second.idx])
                elif matches == max_matches:
                    result.append([first_idx, second.idx])

    return result


if __name__ == "__main__":
    start = time.time()
    n = int(input())
    people = []

    for i in range(n):
        row = input().split()
        value = 0
        for c in row:
            value |= 1 << char_to_int(c)

        # People namedtuple
        # 첫번째 요소: 정렬된 취미 목록 
        # 두번째 요소: 알파벳의 존재 유무를 비트로 저장.
        # 셋번째 요소: index 값. rows 정렬을 하기 때문에 원래 위치를 저장할 필요가 있다.
        people.append(People(sorted(row), value, i+1))

    # 알파벳으로 표시된 정렬된 row를 전체 정렬한다.
    people.sort(key=itemgetter(0))

    result = match(people)
    print("time diff: ", time.time() - start)

    # 결과 값을 정렬한다. 필요 없는 작업이나 해를 확인하기 쉽도록 적용해 두었다.
    for pair in result:
        pair.sort()
    result.sort()


    print("the number of results: %d" % len(result))
    for pair in result:
        print(pair[0], "-", pair[1])
