# Introduction of IPO sponsor lines gluer module


PDF cleaner
This project aimed to preprocess PDF-extracted or other texts with paragraph termination symbols, used as line endings and hard-hyphenations.
fork this repository: https://github.com/serge-sotnyk/pdf-lines-gluer



# use of this module

Simple get https://github.com/serge-sotnyk/pdf-lines-gluer/blob/master/pdf_preprocessor.py and copy it to your project. After this, you can use functionality calling function preprocess_pdf():


don't use language dependent features so that you can try this classifier on any text written on Indo-European languages. Nevertheless, you can face troubles for your texts. If it occurs, you can train your new own classifier.



Add mode train data. Add text with mistakes into folder corpus and annotate it like file corpus/1005058.txt. Every file should contain the first symbol with mark, should we glue current line with the previous one or not ('*' - leave as is, '+' - should be glued). 
