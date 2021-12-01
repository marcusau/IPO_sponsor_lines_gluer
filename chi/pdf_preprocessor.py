import string
from typing import List, Dict



# This code was automatically generated at 2021-06-09 10:51:25.120875


from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from numpy import array

_clf = LogisticRegression()
_clf.coef_ = array([[ 2.49516082e+00,  3.21495231e-01,  1.06619677e+00,
        -2.23489117e-01, -3.14600017e-01,  1.04481480e+00,
        -1.80910585e-04, -2.91727946e+00,  3.48916920e-01,
         2.09966902e-01, -5.79743358e-01, -5.99318109e-01,
         2.24567302e+00, -7.69514586e-01, -8.12459765e-01,
         0.00000000e+00,  2.93213099e+00,  1.81748614e+00,
         4.72036523e-01,  0.00000000e+00,  1.89195056e-01,
         3.21699315e+00, -2.62887718e+00,  8.61267860e-01,
         6.12063779e-02,  2.16040924e+00, -1.42766944e+00,
        -5.63207533e-01,  9.67354498e-01,  0.00000000e+00,
        -4.02457723e-01, -6.96100740e-01, -4.76744678e+00,
        -1.81927163e-01, -7.48464025e-02,  8.61804895e-01,
         4.90513690e-02,  3.62943841e-01, -6.68732492e-02,
        -7.71975640e-02,  9.94495048e-01, -1.55764794e-01,
         7.97851199e-01,  0.00000000e+00,  2.97414972e+00,
        -8.38043836e-01,  1.98743225e+00, -2.30893359e+00,
        -8.26496632e-02]])
_clf.classes_ = array([False,  True])
_clf.intercept_ = [3.451186]

_v = DictVectorizer()
_v.feature_names_ = ['first_chars=#0', 'first_chars=( ', 'first_chars=(0', 'first_chars=(A', 'first_chars=(「', 'first_chars=* ', 'first_chars=*A', 'first_chars=-0', 'first_chars=0 ', 'first_chars=0-', 'first_chars=0.', 'first_chars=00', 'first_chars=0A', 'first_chars=0a', 'first_chars=A ', 'first_chars=A&', 'first_chars=A(', 'first_chars=A)', 'first_chars=A,', 'first_chars=A-', 'first_chars=A.', 'first_chars=A0', 'first_chars=AA', 'first_chars=Aa', 'first_chars=A‧', 'first_chars=A。', 'first_chars=A《', 'first_chars=A「', 'first_chars=A」', 'first_chars=a\xad', 'first_chars=a½', 'first_chars=a¾', 'first_chars=—0', 'first_chars=《A', 'first_chars=「A', 'isalpha', 'isdigit', 'islower', 'mean_len', 'prev_len', 'punct= ', 'punct=#', 'punct=)', 'punct=*', 'punct=,', 'punct=-', 'punct=.', 'punct=:', 'this_len']
_v.vocabulary_ = {'first_chars=#0': 0, 'first_chars=( ': 1, 'first_chars=(0': 2, 'first_chars=(A': 3, 'first_chars=(「': 4, 'first_chars=* ': 5, 'first_chars=*A': 6, 'first_chars=-0': 7, 'first_chars=0 ': 8, 'first_chars=0-': 9, 'first_chars=0.': 10, 'first_chars=00': 11, 'first_chars=0A': 12, 'first_chars=0a': 13, 'first_chars=A ': 14, 'first_chars=A&': 15, 'first_chars=A(': 16, 'first_chars=A)': 17, 'first_chars=A,': 18, 'first_chars=A-': 19, 'first_chars=A.': 20, 'first_chars=A0': 21, 'first_chars=AA': 22, 'first_chars=Aa': 23, 'first_chars=A‧': 24, 'first_chars=A。': 25, 'first_chars=A《': 26, 'first_chars=A「': 27, 'first_chars=A」': 28, 'first_chars=a\xad': 29, 'first_chars=a½': 30, 'first_chars=a¾': 31, 'first_chars=—0': 32, 'first_chars=《A': 33, 'first_chars=「A': 34, 'isalpha': 35, 'isdigit': 36, 'islower': 37, 'mean_len': 38, 'prev_len': 39, 'punct= ': 40, 'punct=#': 41, 'punct=)': 42, 'punct=*': 43, 'punct=,': 44, 'punct=-': 45, 'punct=.': 46, 'punct=:': 47, 'this_len': 48}


def preprocess_pdf(text: str) -> str:
    return _preprocess_pdf(text, _clf, _v)

# end of automatically generated code


def _mean_in_window(lines, i) -> float:
    start = max(i - 10, 0)
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