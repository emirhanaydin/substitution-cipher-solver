import csv

file_names = {
    "encoded": "encoded.txt",
    "decoded": "decoded.txt",
    "alphabet": "alphabet.txt",
    "key": "key.csv",
    "alphabet_letter_frequency": "alphabet_letter_frequency.csv",
    "encoded_letter_frequency": "encoded_letter_frequency.csv",
    "patterns": "patterns.csv",
    "letter_guess": "letter_guess.csv",
}


def read_file(filename):
    result = ""
    with open(filename, "r", encoding="utf-8") as file:
        while line := file.readline():
            result += str.rstrip(line)

    return result


def read_lines(filename):
    result = []
    with open(filename, "r", encoding="utf-8") as file:
        while line := file.readline():
            result.append(str.rstrip(line))

    return result


def read_csv(filename, skip_header=True):
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        if skip_header:
            next(reader)

        result = dict(reader)

    return result


def create_char_index_dict(text):
    return dict(zip(text, range(len(text))))


def create_index_char_dict(text):
    return dict(zip(range(len(text)), text))


def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)


def write_csv(filename, fields, data):
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows(data)


def create_letter_frequency_dict(text, as_ratio=True):
    d = {}
    for c in text:
        v = d.get(c)
        if v is None:
            d[c] = 1
        else:
            d[c] = v + 1

    if as_ratio:
        m = len(text)
        for k, v in d.items():
            d[k] = 100 * v / m

    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))


def find_repeating_patterns(text):
    minlen = 2
    mincnt = 2
    s = text
    d = {}
    for sublen in range(minlen, int(len(s) / mincnt)):
        for i in range(0, len(s) - sublen):
            sub = s[i:i + sublen]
            cnt = s.count(sub)
            if cnt >= mincnt and sub not in d:
                d[sub] = cnt

    return d


def char_freq(text):
    d = {}
    for c in text:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1

    return d


def freq_to_ratio(freq_dict, m):
    return {k: f"{100 * v / m}" for k, v in freq_dict.items()}


def decode(key, encoded):
    res = ""
    for e in encoded:
        d = key.get(e)
        if d is None:
            res += "-"
        else:
            res += d

    return res


def display_menu(options):
    for k, v in options.items():
        print(f"{k}. {v}")

    try:
        option = int(input())
    except ValueError:
        option = -1

    if option in options:
        return option


def main():
    encoded = read_file(file_names["encoded"])
    alphabet_frequency = read_csv(file_names["alphabet_letter_frequency"])
    key = read_csv(file_names["key"])

    decoded = ""

    options = {
        0: "exit",
        1: "import key file",
        2: "decode encoded file",
        3: "print decoded text",
        4: "write decoded text to file",
        5: "decode input text",
        6: "write repeating patterns to file",
        7: "write letter frequency table to file",
        8: "write letter guess by frequency table to file",
        9: "import letter guess file as key",
    }
    option = -1
    is_key_changed = False

    while option != 0:
        option = display_menu(options)
        if option == 1:
            key = read_csv(file_names["key"])
            print(f'{file_names["key"]} has been read.')
            is_key_changed = True
        if option == 2:
            decoded = decode(key, encoded)
            print(f'{file_names["encoded"]} has been decoded.')
        if option in (3, 4):
            if decoded == "":
                decoded = decode(key, encoded)
        if option == 3:
            print(decoded)
        if option == 4:
            write_file(file_names["decoded"], decoded)
            print(f'decoded text has been written to {file_names["decoded"]}.')
        if option == 5:
            print("encoded input:")
            inp = input()
            print("decoded output:")
            print(decode(key, inp))
        if option == 6:
            p = find_repeating_patterns(encoded)
            write_csv(file_names["patterns"], ["pattern", "repeat count"], p.items())
            print(f'repeating patterns have been written to {file_names["patterns"]}.')
        if option == 7:
            p = create_letter_frequency_dict(encoded)
            write_csv(file_names["encoded_letter_frequency"], ["letter", "ratio"], p.items())
            print(f'frequency table of the encoded text has been written to {file_names["encoded_letter_frequency"]}.')
        if option == 8:
            p = create_letter_frequency_dict(encoded)
            d = dict(zip(alphabet_frequency, p))
            write_csv(file_names["letter_guess"], ["alphabet letter", "encoded guess"], d.items())
            print(f'a guessed key has been written to {file_names["letter_guess"]}.')
        if option == 9:
            p = read_csv(file_names["letter_guess"])
            key = p
            print(f'guessed key {file_names["letter_guess"]} file has been read.')
            is_key_changed = True

        if is_key_changed:
            decoded = decode(key, encoded)
            is_key_changed = False


if __name__ == '__main__':
    main()
