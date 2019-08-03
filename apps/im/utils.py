ones = ["", "One ", "Two ", "Three ", "Four ", "Five ", "Six ", "Seven ", "Eight ", "Nine ", "Ten ", "Eleven ",
        "Twelve ", "Thirteen ", "Fourteen ", "Fifteen ", "Sixteen ", "Seventeen ", "eighteen ", "Nineteen "]

twenties = ["", "", "Twenty ", "Thirty ", "Forty ", "Fifty ", "Sixty ", "Seventy ", "Eighty ", "Ninety "]

thousands = ["", "thousand ", "million ", "billion ", "trillion ", "quadrillion ", "quintillion ", "sextillion ",
             "septillion ", "octillion ", "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ",
             "quattuordecillion ", "quindecillion", "sexdecillion ", "septendecillion ", "octodecillion ",
             "novemdecillion ", "vigintillion "]


def num999(n):
    c = n % 10  # singles digit
    b = ((n % 100) - c) / 10  # tens digit
    a = ((n % 1000) - (b * 10) - c) / 100  # hundreds digit
    t = ""
    h = ""
    if a != 0 and b == 0 and c == 0:
        t = ones[a] + "hundred "
    elif a != 0:
        t = ones[a] + "hundred and "
    if b <= 1:
        h = ones[n % 100]
    elif b > 1:
        h = twenties[int(b)] + ones[int(c)]
    st = t + h
    return st


def num2word(num):
    if num == 0: return 'zero'

    i = 3
    n = str(num)
    word = ""
    k = 0
    while (i == 3):
        nw = n[-i:]
        n = n[:-i]
        if int(nw) == 0:
            word = num999(int(nw)) + thousands[int(nw)] + word
        else:
            word = num999(int(nw)) + thousands[k] + word
        if n == '':
            i = i + 1
        k += 1
    return word[:-1]


def get_remark(mark, pass_mark):
    if mark == 'a' or mark == 'A':
        return 'Absent'
    elif int(mark) < int(pass_mark):
        return 'Fail/NQ'
    else:
        return ''


def is_fail(mark, pass_mark):
    if mark == 'a' or mark == 'A':
        return True
    elif int(mark) < int(pass_mark):
        return True
    return False


