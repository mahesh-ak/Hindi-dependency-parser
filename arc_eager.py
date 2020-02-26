from conllu import parse_incr, parse
from nltk.parse import DependencyGraph, DependencyEvaluator
from nltk.parse.transitionparser import TransitionParser
import pickle
import pygraphviz as pgv
from test_hn_pos import test_fn
import os

def Process(sentence):
    words = sentence.replace('|','।').split()
    tags = test_fn(words)
    text = []
    i = 0
    for word, tag in zip(words,tags):
        i += 1
        fill = '_'
        text.append('\t'.join([str(i),word,fill,fill,fill,fill,fill,fill,fill,fill]))
    dg = DependencyGraph('\n'.join(text))
    text = '\n'.join(text)
    text = text + '\n\n' + text
    with open('biaffine-parser-master/data/naive3.conllx','w') as f:
        f.write(text)
    os.chdir('biaffine-parser-master')
    os.system('python run.py predict --feat=bert --fdata=data/naive3.conllx --fpred=data/naive3.conllx')
    txt = ''
    os.chdir('..')
    with open('biaffine-parser-master/data/naive3.conllx','r') as f:
        txt = f.read().split('\n\n')[0]
    
    # parser = TransitionParser('arc-eager')
    # with open('models/parser.pkl','rb') as in_file:
    #     parser = pickle.load(in_file)
    # predictions = parser.parse([dg],'models/arc_eager.model')
    # txt = predictions[0].to_conll(4)
    err = False
    try:
        out = DependencyGraph(txt)
        out_dot = out.to_dot()
        G = pgv.AGraph(out_dot)
        G.layout(prog='dot') # use dot
        G.draw('static/process.png')
    except:
        err = True
        txt += '''Error generating graph.\n''' 
    return txt, err


    

## creates dependency graph list according to nltk library specification
def DepGraphList(sentenceList):
    dgList = []
    i = 0
    j = 0
    for sentence in sentenceList:
        text = []
        for token in sentence:
            text.append(' '.join([token['form'],token['upostag'],str(token['head']),token['deprel'].upper()]))
        try:
            dg = DependencyGraph('\n'.join(text))
        except:
            j += 1
            continue
        i += 1
        dgList.append(dg)
    print(i,j)
    return dgList

def main():
    data_file = open('data/UD_Bhojpuri-BHTB-master/bho_bhtb-ud-test.conllu','r',encoding='utf-8')
    sentence_iter = parse_incr(data_file)
    sentences = []
    for s in sentence_iter:
        sentences.append(s)
    training_set = DepGraphList(sentences[len(sentences)//4:])
    test_set = DepGraphList(sentences[0:len(sentences)//4])
   
    parser = TransitionParser('arc-eager')
    ## Training
    # parser.train(training_set,'models/arc_eager.model')
    # with open('models/parser2.pkl','wb') as out:
    #      pickle.dump(parser,out)
    # # ## Evaluation
    # with open('models/parser2.pkl','rb') as in_file:
    #     parser = pickle.load(in_file)
    # predictions = parser.parse(test_set,'models/arc_eager.model')
    # de = DependencyEvaluator(predictions,test_set)
    # print(de.eval())
    Process('राम अच्छा पुरुष है |')
    return

if __name__=='__main__':
    main()