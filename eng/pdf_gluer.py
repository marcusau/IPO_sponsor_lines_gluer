from os import listdir
import pathlib
from os.path import isfile, join
from typing import List, Dict
import random
import datetime
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from eng import pdf_lines_gluer

#####--------------------------------------------------------------------------------------------------

process_data_folder=r'C:\Users\marcus\PycharmProjects\IPO_sponsor_lines_gluer\data\process\eng'

pdf_lines_gluer_script=r'C:\Users\marcus\PycharmProjects\IPO_sponsor_lines_gluer\eng\pdf_lines_gluer.py'
pdf_preprocessor_script=r'C:\Users\marcus\PycharmProjects\IPO_sponsor_lines_gluer\eng\pdf_preprocessor.py'

seed=1974
test_size=0.2
max_iter=300000

#####--------------------------------------------------------------------------------------------------
random.seed(seed)


def load_texts(f_names:str):
    #f_names = [join('corpus', f) for f in listdir('corpus') if isfile(join('corpus', f))]
    f_names = [f for f in pathlib.Path(f_names).iterdir() ]

    for fn in f_names:
        with open(fn, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
            if not text[0] in {'+', '*'}:
                print(f"File '{fn}' is not annotated, skipped.")
                continue
            #print(f"File '{fn}' is annotated, add to collection.")
            yield text

raw_corpus = list(load_texts(process_data_folder))

xx, yy = [], []
for raw_text in raw_corpus:
    x, y = pdf_lines_gluer._featurize_text_with_annotation(raw_text)
    xx+=x
    yy+=y
print(f"Total samples: {len(yy)}")
print(f"Positive samples: {sum(y for y in yy if y)}")

###--------------------------------------------------------------------------------

combined = list(zip(xx, yy))
random.shuffle(combined)

xx[:], yy[:] = zip(*combined)

v = DictVectorizer(sparse=False)
v.fit(xx)
xx_features = v.transform(xx)
print(xx_features[:1])

x_train, x_test, y_train, y_test = train_test_split(xx_features, yy, test_size=test_size, random_state=seed)

clf = LogisticRegression(random_state=seed, solver='liblinear', max_iter=max_iter, class_weight='balanced' )
clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)

print(classification_report(y_true=y_test, y_pred=y_pred))

# ## Check minimal properties set to save vectorizer and classifier

print(repr(v))
print(v.feature_names_)
print(v.vocabulary_)

vv = DictVectorizer()
vv.feature_names_ = v.feature_names_
vv.vocabulary_ = v.vocabulary_

print(repr(clf.coef_))
print(repr(clf.classes_))
print(clf.intercept_)

#
# ##### Serialize as code


serialized_as_code = f"""

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from numpy import array

_clf = LogisticRegression()
_clf.coef_ = {repr(clf.coef_)}
_clf.classes_ = {repr(clf.classes_)}
_clf.intercept_ = {clf.intercept_}

_v = DictVectorizer()
_v.feature_names_ = {v.feature_names_}
_v.vocabulary_ = {v.vocabulary_}


def preprocess_pdf(text: str) -> str:
    return _preprocess_pdf(text, _clf, _v)

"""

serialized_as_code = f"\n# This code was automatically generated at {datetime.datetime.now()}\n"+ serialized_as_code+ "# end of automatically generated code"

print(serialized_as_code)

with open(pdf_lines_gluer_script, 'r', encoding='utf-8') as file:
    template = file.read()

generated_code = template.replace('# inject code here #', serialized_as_code)

with open(pdf_preprocessor_script, 'wt', encoding='utf-8') as file:
    file.write(generated_code)