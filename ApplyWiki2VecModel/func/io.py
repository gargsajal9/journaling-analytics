'''
Created on Jun 5, 2015

@author: Changsung Moon (csmoon2@ncsu.edu)

copied from http://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
'''

from docx import Document

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


'''
    Extract text from pdf
'''
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    
    return text



'''
    Extract text from docx
'''
def convert_docx_to_txt(path):
    document = Document(path)
    
    text = '\n'.join([paragraph.text.encode('utf-8') for paragraph in document.paragraphs])
    
    return text



def convert_file_to_txt(path, tags):
    f = open(path, 'r')
    text = ""
    
    for line in f:
        if tags[0] in line:
            content = line.split(tags[0])[1]
            text = text + content
        elif tags[1] in line:
            content = line.split(tags[1])[1]
            text = text + content
        elif tags[2] in line:
            content = line.split(tags[2])[1]
            text = text + content
        
    return text