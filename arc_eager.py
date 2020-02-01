from conllu import parse_incr
from nltk.parse import DependencyGraph, DependencyEvaluator
from nltk.parse.transitionparser import TransitionParser
import pickle

def Process(sentence):
    words = sentence.replace('।','').split() + ['।']
    text = []
    for word in words:
        text.append(' '.join([word,'NOUN','0','NMOD']))
    dg = DependencyGraph('\n'.join(text))
    with open('parser.pkl','rb') as in_file:
        parser = pickle.load(in_file)
    predictions = parser.parse([dg],'arc_eager.model')
    out_dg = predictions[0].to_conllu()
    out = parse_incr(out_dg)
    to = {'words':[],'arcs':[]}

    for token in out:
        to['words'].append({"text": token['form'], "tag": token['upostag']})
        to['arcs'].append({"start": token['head'], "end": token['id'], "label": token['deprel'], "dir": "left"})
    
    return [to]


    

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
    with open('parser.pkl','rb') as in_file:
        parser = pickle.load(in_file)
    predictions = parser.parse(test_set,'arc_eager.model')
    de = DependencyEvaluator(predictions,test_set)
    print(de.eval())
    return

if __name__=='__main__':
    main()