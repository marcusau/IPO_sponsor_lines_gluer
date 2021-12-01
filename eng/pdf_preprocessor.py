import string,os,pathlib,sys
from typing import List, Dict
sys.path.append(r"C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\ML")
sys.path.append(r"C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\ML\lines_gluer\pdf_preprocessor.py")
sys.path.append(r"C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\ML\lines_gluer")


# This code was automatically generated at 2021-05-06 19:35:09.215877

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from numpy import array

_clf = LogisticRegression()
_clf.coef_ = array([[-5.49328318e-01,  3.31691554e-01,  5.61206393e-01,
        -2.10562918e+00,  9.39846332e-01,  4.54219508e+00,
         4.75013627e+00,  2.42899292e+00,  2.50281904e+00,
         4.57974042e-01, -1.11329657e+00, -1.04228652e+00,
        -4.26656930e-01, -7.55477130e-01,  1.12382368e+00,
         0.00000000e+00, -2.82542392e+00,  4.09092527e-01,
         3.19152576e+00,  5.87239211e-01, -1.74790289e+00,
         3.14470333e+00, -9.23437031e-01, -7.50292347e-01,
        -6.80081619e-01, -3.78571650e+00, -2.12053595e+00,
        -1.28607802e+00, -3.08175702e+00, -3.77791457e-01,
         8.53851039e-01,  5.38990538e-01,  2.43117151e+00,
         4.65729166e-01,  3.05766939e+00, -1.18058244e-01,
        -1.89506812e+00,  0.00000000e+00, -7.78001658e-02,
        -9.73559399e-02,  3.97192981e-01, -2.33719151e+00,
        -1.66385453e+00,  9.70050205e-01,  2.93450967e+00,
         2.53500341e+00,  6.50565560e-01, -1.11780222e+00,
         1.17003943e-01, -8.27339843e-01, -4.53033465e-01,
        -3.29882552e+00, -1.35139577e+00, -7.01273761e-01,
        -8.23405340e-01,  5.50000712e-01,  1.71077944e-01,
        -1.27410533e-02, -6.44132499e-04,  4.32502398e-01,
        -1.05834131e+00,  1.06461787e+00, -4.92518993e-01,
        -1.10999669e-01,  2.69504662e+00, -3.90862362e-01,
        -6.91676040e-02,  3.05669664e+00, -9.69316329e-02,
        -6.45886788e-01, -5.22538282e-01, -8.94483077e-04,
        -1.44842935e+00, -7.41701219e-03]])
_clf.classes_ = array([False,  True])
_clf.intercept_ = [2.41229307]

_v = DictVectorizer()
_v.feature_names_ = ['first_chars=#', 'first_chars=#0', 'first_chars=&', 'first_chars=(', 'first_chars=(0', 'first_chars=(A', 'first_chars=(a', 'first_chars=)', 'first_chars=) ', 'first_chars=))', 'first_chars=*', 'first_chars=* ', 'first_chars=+\t', 'first_chars=+ ', 'first_chars=,', 'first_chars=, ', 'first_chars=- ', 'first_chars=.', 'first_chars=. ', 'first_chars=."', 'first_chars=0', 'first_chars=0 ', 'first_chars=0,', 'first_chars=0-', 'first_chars=0.', 'first_chars=0/', 'first_chars=00', 'first_chars=0A', 'first_chars=0a', 'first_chars=0–', 'first_chars=:', 'first_chars=: ', 'first_chars=<A', 'first_chars=A', 'first_chars=A ', 'first_chars=A&', "first_chars=A'", 'first_chars=A)', 'first_chars=A-', 'first_chars=A.', 'first_chars=A0', 'first_chars=AA', 'first_chars=Aa', 'first_chars=a', 'first_chars=a ', 'first_chars=a.', 'first_chars=a/', 'first_chars=aA', 'first_chars=aa', 'first_chars=˙', 'first_chars=– ', 'first_chars=− ', 'first_chars=� ', 'first_chars=��', 'isalpha', 'isdigit', 'islower', 'mean_len', 'prev_len', 'punct= ', 'punct="', 'punct=#', 'punct=&', "punct='", 'punct=(', 'punct=)', 'punct=*', 'punct=,', 'punct=-', 'punct=.', 'punct=:', 'punct=;', 'punct=>', 'this_len']
_v.vocabulary_ = {'first_chars=#': 0, 'first_chars=#0': 1, 'first_chars=&': 2, 'first_chars=(': 3, 'first_chars=(0': 4, 'first_chars=(A': 5, 'first_chars=(a': 6, 'first_chars=)': 7, 'first_chars=) ': 8, 'first_chars=))': 9, 'first_chars=*': 10, 'first_chars=* ': 11, 'first_chars=+\t': 12, 'first_chars=+ ': 13, 'first_chars=,': 14, 'first_chars=, ': 15, 'first_chars=- ': 16, 'first_chars=.': 17, 'first_chars=. ': 18, 'first_chars=."': 19, 'first_chars=0': 20, 'first_chars=0 ': 21, 'first_chars=0,': 22, 'first_chars=0-': 23, 'first_chars=0.': 24, 'first_chars=0/': 25, 'first_chars=00': 26, 'first_chars=0A': 27, 'first_chars=0a': 28, 'first_chars=0–': 29, 'first_chars=:': 30, 'first_chars=: ': 31, 'first_chars=<A': 32, 'first_chars=A': 33, 'first_chars=A ': 34, 'first_chars=A&': 35, "first_chars=A'": 36, 'first_chars=A)': 37, 'first_chars=A-': 38, 'first_chars=A.': 39, 'first_chars=A0': 40, 'first_chars=AA': 41, 'first_chars=Aa': 42, 'first_chars=a': 43, 'first_chars=a ': 44, 'first_chars=a.': 45, 'first_chars=a/': 46, 'first_chars=aA': 47, 'first_chars=aa': 48, 'first_chars=˙': 49, 'first_chars=– ': 50, 'first_chars=− ': 51, 'first_chars=� ': 52, 'first_chars=��': 53, 'isalpha': 54, 'isdigit': 55, 'islower': 56, 'mean_len': 57, 'prev_len': 58, 'punct= ': 59, 'punct="': 60, 'punct=#': 61, 'punct=&': 62, "punct='": 63, 'punct=(': 64, 'punct=)': 65, 'punct=*': 66, 'punct=,': 67, 'punct=-': 68, 'punct=.': 69, 'punct=:': 70, 'punct=;': 71, 'punct=>': 72, 'this_len': 73}


def preprocess_pdf(text: str) -> str:
    return _preprocess_pdf(text, _clf, _v)

# end of automatically generated code


def _mean_in_window(lines, i) -> float:
    start = max(i - 5, 0)
    finish = min(i + 5, len(lines) - 1)
    sm, count = 0, 0
    for n in range(start, finish):
        sm += len(lines[n]) - 1  # minus one-char prefix
        count += 1
    return sm / max(count, 1)


def _last_char(line: str) -> str:
    return ' ' if len(line) < 1 else line[-1]


def _last_char_features(l_char: str) -> Dict[str, object]:
    res = {
        'isalpha': l_char.isalpha(),
        'isdigit': l_char.isdigit(),
        'islower': l_char.islower(),
        'punct': l_char if l_char in string.punctuation else ' ',
    }
    return res


def _first_chars(line: str) -> str:
    if len(line) < 1:
        chars = ' '
    elif len(line) < 2:
        chars = line[0]
    else:
        chars = line[:2]
    res = []
    for c in chars:
        if c.isdigit():
            res.append('0')
        elif c.isalpha():
            res.append('a' if c.islower() else 'A')
        else:
            res.append(c)
    return ''.join(res)


def _line_to_features(line: str, i: int, lines: List[str], annotated: bool) -> Dict[str, object]:
    features = {}
    this_len = len(line)
    mean_len = _mean_in_window(lines, i)
    if i > 0:
        prev_len = len(lines[i - 1]) - (1 if annotated else 0)
        l_char = _last_char(lines[i - 1])
    else:
        prev_len = 0
        l_char = ' '
    features.update(
        {
            'this_len': this_len,
            'mean_len': mean_len,
            'prev_len': prev_len,
            'first_chars': _first_chars(line),
        })
    features.update(_last_char_features(l_char))
    return features


def _featurize_text_with_annotation(text: str) -> (List[object], List[bool]):
    lines = text.strip().splitlines()
    x, y = [], []
    for i, line in enumerate(lines):
        y.append(line[0] == '+')  # True, if line should be glued with previous
        line = line[1:]
        x.append(_line_to_features(line, i, lines, True))
    return x, y


_HYPHEN_CHARS = {
    '\u002D',  # HYPHEN-MINUS
    '\u00AD',  # SOFT HYPHEN
    '\u2010',  # HYPHEN
    '\u2011',  # NON-BREAKING HYPHEN
}


def _preprocess_pdf(text: str, clf, v) -> str:
    lines = [s.strip() for s in text.strip().splitlines()]
    x = []
    for i, line in enumerate(lines):
        x.append(_line_to_features(line, i, lines, False))
    if not x:
        return ''

    x_features = v.transform(x)
    y_pred = clf.predict(x_features)

    corrected_acc = []
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0 or not y_pred[i]:
            corrected_acc.append(line)
        else:
            prev_line = corrected_acc[-1]
            if prev_line != '' and prev_line[-1] in _HYPHEN_CHARS:
                corrected_acc[-1] = prev_line[:-1]
            else:
                corrected_acc[-1] += ' '
            corrected_acc[-1] += line

    corrected = '\n'.join(corrected_acc)
    return corrected