from conllu import parse_incr
from nltk.parse import DependencyGraph, DependencyEvaluator
from nltk.parse.transitionparser import TransitionParser
import pickle

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
    parser.train(training_set,'arc_eager.model')
    with open('parser.pkl','wb') as out:
        pickle.dump(parser,out)
    ## Evaluation
    ##with open('parser.pkl','rb') as in:
    ##    parser = pickle.load(in)
    ##predictions = parser.parse(test_set,'arc_eager.model')
    ##de = DependencyEvaluator(predictions,test_set)
    ##print(de.eval())
    return

if __name__=='__main__':
    main()