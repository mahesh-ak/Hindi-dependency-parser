from conllu import parse_incr, parse
from nltk.parse import DependencyGraph, DependencyEvaluator
from nltk.parse.transitionparser import TransitionParser
import pickle
import pygraphviz as pgv
from test_hn_pos import test_fn

def Process(sentence):
    words = sentence.replace('|','।').split()
    tags = test_fn(words)
    text = []
    for word, tag in zip(words,tags):
        text.append(' '.join([word,tag,'1','NMOD']))
    dg = DependencyGraph('\n'.join(text))
    parser = TransitionParser('arc-eager')
    with open('parser.pkl','rb') as in_file:
        parser = pickle.load(in_file)
    predictions = parser.parse([dg],'arc_eager.model')
    out = DependencyGraph(predictions[0].to_conll(4))
    out_dot = out.to_dot()
    G = pgv.AGraph(out_dot)
    G.layout(prog='dot') # use dot
    G.draw('static/process.png')

    


    

## creates dependency graph list according to nltk library specification
def DepGraphList(sentenceList):
    dgList = []
    for sentence in sentenceList:
        text = []
        for token in sentence:
            text.append(' '.join([token['form'],token['upostag'],str(token['head']),token['deprel'].upper()]))
        dg = DependencyGraph('\n'.join(text))
        dgList.append(dg)
    return dgList

def main():
    data_file = open('data/UD_Hindi-HDTB/hi_hdtb-ud-dev.conllu','r',encoding='utf-8')
    sentence_iter = parse_incr(data_file)
    sentences = []
    for s in sentence_iter:
        sentences.append(s)
    training_set = DepGraphList(sentences[len(sentences)//4:])
    test_set = DepGraphList(sentences[0:len(sentences)//4])
   
    parser = TransitionParser('arc-eager')
    ## Training
    ##parser.train(training_set,'arc_eager.model')
    ##with open('parser.pkl','wb') as out:
    ##    pickle.dump(parser,out)
    ## Evaluation
    # with open('parser.pkl','rb') as in_file:
    #     parser = pickle.load(in_file)
    # predictions = parser.parse(test_set,'arc_eager.model')
    # de = DependencyEvaluator(predictions,test_set)
    # print(de.eval())
    Process('राम अच्छा पुरुष है |')
    return

if __name__=='__main__':
    main()