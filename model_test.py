import os,pathlib,sys,csv,itertools
import json, re
from typing import Union,Dict,List,Tuple,Optional
from collections import OrderedDict

import cleantext

import xml.etree.ElementTree as ET
from rapidfuzz import process, fuzz

#from sklearn.model_selection import train_test_split

import fitz
from eng import pdf_preprocessor as eng_preprocess_pdf
from chi import pdf_preprocessor as chi_preprocess_pdf

###---------------------------------------------------------------------------------------------------------------------------------------------
title_text_path=r'C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\keywords\keywords.txt'

word4search={}

with open(title_text_path,'r',encoding='utf-8') as f:
    for line in f.readlines() :
        t_, lang, t_words=line.strip().split('\t')
        if t_ not in word4search:
            word4search[t_]={'chi':[], 'eng':[]}
        word4search[t_][lang].append(t_words)


#########-----------------------------------------------------------------------------------------------------------------

def search_toc(toc_pages,tag:str='parties',lang:str='eng'):
    fuzz_toc = {t: process.extractOne(t, choices=word4search[tag][lang], scorer=fuzz.WRatio)[1] for t in    toc_pages}
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



def locate_pages(pdf_file_path,tag:str='parties',lang:str='chi'):

    doc = fitz.open(pdf_file_path)
    fitz_toc = doc.getToC(simple = False)
    if len(fitz_toc) == 0:
        print("No Table of Contents available")
        return None,None
    else:
        toc_pages=fetch_toc_pages(fitz_toc)
        pi_pages,tag_toc =search_toc(toc_pages, tag= tag, lang=lang)
        if not pi_pages:
            print(f'cannot find the pages of "directors and parties involved for stocks:{pdf_file_path}')
            return None,None
        else:
            return pi_pages, tag_toc

##-------------------------------------------------

def clean_pretext(tt,tag_toc,lang:str='eng'):
    tt = cleantext.normalize_whitespace(tt.strip())
    tt = cleantext.replace_emails(tt)
    tt = cleantext.replace_emails(tt)
    tt = re.sub(tag_toc, '', tt, flags=re.I)
    tt = re.sub('\— \d+ \—|– \d+ \–|\− \d+ \−', '', tt)
    tt = re.sub('�', '-', tt)

    if lang.lower()=='chi':
        tt = re.sub('\n', '', tt)
        match = re.findall(' ', tt)

        if len(match) >= round(len(tt) * 0.4):
            tt = re.sub(' ', '', tt)

    return tt

###---------------------------------------------------------------------------------------------
###
flags = fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE  # | fitz.TEXT_PRESERVE_SPANS


def fetch_pretext(pdf_path,tag:str='parties',lang:str='chi'):
    doc = fitz.open(pdf_path)
    pi_pages,tag_toc =locate_pages(pdf_path,tag=tag,lang=lang)


    pi_texts = []
    for pi_page in pi_pages:
        if lang.lower()=='eng':
            pi_page_xhtml = doc[pi_page].get_textpage(flags).extractXHTML()
            for tt in ET.fromstring(pi_page_xhtml).itertext():
                pi_text = clean_pretext(tt,tag_toc,lang=lang)
                pi_texts.append(pi_text)
        else:
            #print('fetch chinese text')
            pi_page_xhtml = doc[pi_page].get_textpage(flags).extractBLOCKS()
            for block in pi_page_xhtml:
                tt = block[4].strip()
                pi_text = clean_pretext(tt, tag_toc,lang=lang)
                pi_texts.append(pi_text.strip())

    pi_texts = ' \n'.join(pi_texts)
    pi_texts = re.sub(' \s\s|\t|\s\s\s', "", pi_texts)


    if lang.lower()=='eng':
        process_texts=eng_preprocess_pdf(pi_texts)
    else:
        print('process Chinese text')
        process_texts=chi_preprocess_pdf(pi_texts)

    return process_texts

if __name__=='__main__':
    lang='chi'
    stockcode=3938
    pdf_path=r'C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\pdf\{}\{}.pdf'.format(lang,stockcode)
    train=[pdf_path]
    #
    # # stockcode=1413
    # lang = 'chi'
    # pdf_folder_path = pathlib.Path(r'C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\pdf\{}'.format(lang))
    # raw_data_folder = pathlib.Path(  r'C:\Users\marcus\PycharmProjects\ipo_pdf_scrapping\ML\NER\data\raw\{}'.format(lang))
    # text_path = raw_data_folder / f'total.txt'
    #
    # pdf_files = [f for f in pdf_folder_path.iterdir()]
    # test, train = train_test_split(pdf_files, test_size=0.5, shuffle=True, random_state=3333)

    for f in train:
        stockcode = int(f.stem)

        #   if stockcode in [368]:
       # pdf_path = pdf_folder_path / f'{stockcode}.pdf'
        try:
            print(f"processing stockcode :{stockcode}")
            pre_texts=fetch_pretext(pdf_path=pdf_path,tag='parties',lang=lang)
            for pre_text in pre_texts.split('\n'):
                if lang.lower()=='chi':
                    match = re.findall(' ', pre_text)
                    if len(match) >= round(len(pre_text) * 0.4):
                        pre_text = re.sub(' ', '', pre_text)
                print(pre_text)
            #     with open(text_path.as_posix(),'a',encoding='utf-8') as f:
            #        f.write(pre_text+'\n')
            # print('\n')
        except Exception as e:
            print(f"error: {e}, stockcode :{stockcode}")