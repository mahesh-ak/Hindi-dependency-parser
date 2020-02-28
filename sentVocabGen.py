import os
import json
import re


# Command to extract:
# python WikiExtractor.py ../data/hiwiki-20200220-pages-articles.xml.bz2 --json -de gallery,timeline,noinclude --filter_disambig_pages

def GenSentVocab():
    folders = os.listdir('text')
    vocab = {}
    out_file = open('sentences.txt','a')
    for fldr in folders:
        fldr_pth = os.path.join('text',fldr)
        files = os.listdir(fldr_pth)
        for fl in files:
            fl_pth = os.path.join(fldr_pth,fl)
            with open(fl_pth,'r') as f:
                lines = f.readlines()
                for line in lines:
                    article = json.loads(line)
                    text = article['text'].replace('॥',' ॥\n')
                    text = article['text'].replace('।',' ।\n')
                    text = article['text'].replace('.',' .\n')
                    for s in ['\"',"\'",'?','.',',','(',')','[',']','{','}','-','|',';',':','/','\\','=','’','—','‘','`','!','@','$','~','&','^','%','“','”','+','*','।']:
                        text = text.replace(s,' '+s+' ')
                    ref_tag = re.compile(r'<ref( name= \" .*? \" )*>.*</ref>')
                    text = re.sub(ref_tag,'',text)
                    ref_tag = re.compile(r'<.*?>')
                    text = re.sub(ref_tag,'',text)
                    text = re.sub(' +',' ',text)
                    text = re.sub(r"\n+",'\n',text)
                    text = re.sub(r"[A-Z|a-z]",'',text)
                    text = re.sub(r"[0-9]+",' \1 ',text)
                    sentences = re.split(r"\n",text)
                    for sent in sentences:
                        sentence = sent.strip()
                        if sentence == '':
                            continue
                        out_file.write(sentence+'\n')
                        tokens = sentence.split()
                        for tkn in tokens:
                            if tkn not in vocab:
                                vocab[tkn] = 1
                            else:
                                vocab[tkn] += 1
    out_file.close()
    with open('vocabulary.txt','a') as voc:
        for w in vocab:
            voc.write(w+'\n')
        voc.write('<UNK>'+'\n')
            



if __name__=='__main__':
    GenSentVocab()