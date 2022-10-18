

def list_to_string(our_list):
    result = ""
    for line in our_list:
        for i in line:
            result += i
        result += "\n"
    return result[:-1]


def long_division(dividend, divider):
    lines = [list(str(dividend) + "|" + str(divider))]
    quotient = dividend // divider
    space_counter = 0
    quotient_index = 0
    number = ""
    for i in str(dividend):
        number += i
        if int(number) < divider:
            if quotient_index != 0:
                quotient_index += 1
            continue
        else:
            incomplete_div = divider * int(str(quotient)[quotient_index])
            if incomplete_div == 0:
                quotient_index += 1
                continue
            if quotient_index != 0:
                if number[0] == "0":
                    number = number[1:]
                    space_counter += 1
                lines.append(list(" " * space_counter + number))
            difference = int(number) - incomplete_div
            space_counter += len(number) - len(str(incomplete_div))
            lines.append(list(" " * space_counter + str(incomplete_div)))
            space_counter += len(str(incomplete_div)) - len(str(difference))
            quotient_index += 1
            number = str(difference)
    # РћР±СЂР°Р±РѕС‚РєР° СЃРёС‚СѓР°С†РёРё СЃ РЅСѓР»РµРј РІ РґРµР»РёРјРѕРј
    if int(number) == 0:
        lines.append(list(" " * space_counter + str(int(number))))
    else:
        change_zeros = " " * (len(number) - len(str(int(number))))
        lines.append(list(" " * space_counter +
                          change_zeros + str(int(number))))
    lines[1] += list((len(str(dividend)) -
                      len(lines[1])) * " " + "|" + str(quotient))
    return list_to_string(lines)


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()