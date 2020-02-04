from conllu import parse
from io import open
from conllu import parse_incr
# from sklearn.externals import joblib
# import cloudpickle
import dill

data_file = open("hi_hdtb-ud-train.conllu", "r", encoding="utf-8")
sentences=[]
for tokenlist in parse_incr(data_file):
    sentences.append(tokenlist)

data_file = open("hi_hdtb-ud-dev.conllu", "r", encoding="utf-8")

for tokenlist in parse_incr(data_file):
    sentences.append(tokenlist)

data_file = open("hi_hdtb-ud-test.conllu", "r", encoding="utf-8")
test_sentences=[]
for tokenlist in parse_incr(data_file):
    test_sentences.append(tokenlist)

train_sentences = sentences#[:1500]
test_sentences = test_sentences
train_data_hn=[[(token['form'],token['upostag']) for token in sentence ]for sentence in train_sentences ]
test_data_hn=[[(token['form'],token['upostag']) for token in sentence ]for sentence in test_sentences ]


import nltk
from nltk.tag import hmm
trainer = hmm.HiddenMarkovModelTrainer()
tagger = trainer.train_supervised(train_data_hn)

with open('my_tagger.dill', 'wb') as f:
    dill.dump(tagger, f)
print('MODEL SAVED')
# tagger3 = joblib.load('filename.pkl')

# print( tagger)

test1=[token['form'] for token in test_sentences[10]]
print('input :\n',test1)
out = tagger.tag(test1)
act = [(token['form'],token['upostag']) for token in test_sentences[10] ]



def acc(test_sentences=test_sentences):
    num = 0
    denom = 0
    for sen in test_sentences:
        test1=[token['form'] for token in sen]
        out = tagger.tag(test1)
        act = [(token['form'],token['upostag']) for token in sen ]
        num+=sum(x == y for x, y in zip(out, act))
        denom+=len(out)
    print("acc=",num/denom)

acc()
# s=sum(x == y for x, y in zip(out, act))/sum(x != y for x, y in zip(out, act))

print("An Example \n")
print("True:\n",act)
print("\nPredicted:\n",out)

'''
test1=[token['form'] for token in test_sentences[10]]
print('input :\n',test1)
out = tagger.tag(test1)

'''