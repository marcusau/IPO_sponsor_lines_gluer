import fitz
from typing import Union,Dict,List,Tuple,Optional
import os,sys,pathlib,csv,itertools
import json,random
import cleantext
from collections import OrderedDict
import xml.etree.ElementTree as ET
import re,time
from tqdm import tqdm
from rapidfuzz import process, fuzz
from sklearn.model_selection import train_test_split


title_text_path=r'C:\Users\marcus\PycharmProjects\IPO_sponsor_lines_gluer\keywords.txt'

word4search={}
with open(title_text_path,'r',encoding='utf-8') as f:
    for line in f.readlines() :
        t_, lang, t_words=line.strip().split('\t')
        if t_ not in word4search:
            word4search[t_]={'chi':[], 'eng':[]}
        word4search[t_][lang].append(t_words)

#########-----------------------------------------------------------------------------------------------------------------

def search_toc(toc_pages,tag:str='parties',lang:str='eng'):
    fuzz_toc = {t: process.extractOne(t, choices=word4search['parties'][lang], scorer=fuzz.WRatio)[1] for t in    toc_pages}
    tag_toc = max(fuzz_toc, key=fuzz_toc.get)
    tag_pages=toc_pages[tag_toc]
    tag_pages=list(filter(lambda x:x>=0,tag_pages))
    return tag_pages,tag_toc

#########-----------------------------------------------------------------------------------------------------------------

def fetch_toc_pages(fitz_toc):
    raw_toc = OrderedDict()
    for i, item in enumerate(fitz_toc):

        lvl, title, pno, ddict = item

        row_text = str(title, )

        row_text = ' '.join([w.capitalize() for w in row_text.split(' ')])
        row_text = cleantext.replace_emails(row_text)
        row_text = cleantext.replace_urls(row_text)
        row_text = cleantext.normalize_whitespace(row_text)

        toc_pagenum = int(pno)
        raw_toc[i] = {'content': row_text, 'start': toc_pagenum, }

    toc = {}
    for k, v in raw_toc.items():
        if k < max(raw_toc.keys()):
            start = v['start'] - 1
            end = int(raw_toc[k + 1].get('start')) - 1
            toc[v['content']] = list(range(start, end + 1))  # {'start': start, 'end': end}
    return toc

#########-----------------------------------------------------------------------------------------------------------------

def clean_pretext(tt):
    tt = cleantext.normalize_whitespace(tt.strip())
    tt = cleantext.replace_urls(tt.strip(), '')
    tt = cleantext.replace_emails(tt.strip(), '')
    tt = cleantext.fix_bad_unicode(tt)
    tt = re.sub(tag_toc, '', tt, flags=re.I)
    tt = re.sub('�', '', tt, flags=re.I)
    tt = re.sub('\n|\t', ' ', tt, flags=re.I)
    tt = re.sub('\– \d{1,3} \–|\-  \d{1,3} \-', '', tt, flags=re.I)

    match = re.findall(' ', tt)
    if len(match) >= round(len(tt) * 0.3):
        tt = re.sub(' ', '', tt)

    if len(tt) >= 2:
       return  tt.strip()
    else:
        return None

#########-----------------------------------------------------------------------------------------------------------------

flags = fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE| fitz.TEXT_INHIBIT_SPACES

lang='chi'
pdf_folder_path=pathlib.Path(r'C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\pdf\{}'.format(lang))
raw_data_folder=pathlib.Path(r'C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\ML\lines_gluer\data\raw\{}'.format(lang))
text_path = raw_data_folder / f'total.txt'

pdf_files=[f for f in pdf_folder_path.iterdir()]
test,train=train_test_split(pdf_files,test_size=0.99,shuffle=True,random_state=3333)

# for f in  pdf_folder_path.iterdir():
#     print(pdf_file)
for f in train:
    stockcode= int(f.stem)

 #   if stockcode in [368]:
    pdf_path=pdf_folder_path/f'{stockcode}.pdf'

    doc = fitz.open(pdf_path)
    fitz_toc = doc.getToC(simple = False)

    if len(fitz_toc) == 0:
            print(f"stockcode: {stockcode},No Table of Contents available")
    else:
            toc_pages=fetch_toc_pages(fitz_toc)
            pi_pages,tag_toc =search_toc(toc_pages, tag= 'parties', lang=lang)
            print(stockcode,tag_toc,pi_pages,)
            if not pi_pages:
                print(f'cannot find the pages of "directors and parties involved for stocks:{stockcode}')
            else:
                pi_texts=[]
                for  pi_page in pi_pages:
                    if lang.lower()=='eng':
                        pi_page_xhtml = doc[pi_page].get_textpage().extractXML()
                        for tt in ET.fromstring(pi_page_xhtml).itertext():
                            clean_pretext(tt)
                    else:
                        pi_page_xhtml = doc[pi_page].get_textpage(flags).extractBLOCKS()
                        for block in pi_page_xhtml:
                            tt = block[4].strip()
                            tt= clean_pretext(tt)
                            if tt:
                                with open(text_path.as_posix(), 'a', encoding='utf-8') as f:
                                    f.write(str(stockcode) + '\t' + tt + '\n')
                                   # print(f'stockcode:{stockcode}: ',tt.strip(),)


                       # print('\n')
                  #      pi_texts= '\n'.join(pi_texts)
                      #  pi_texts=re.sub(' \s\s|\t|\s\s\s', "", pi_texts)

               #
               #  with open(text_path.as_posix(), 'a', encoding='utf-8') as f:
               #          for sen in pi_texts.split('\n'):
               #              f.write(str(stockcode)+'\t'+sen+'\n')