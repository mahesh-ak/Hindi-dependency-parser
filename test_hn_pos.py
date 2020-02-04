from conllu import parse
from io import open
from conllu import parse_incr
# from sklearn.externals import joblib
# import cloudpickle
import dill



# with open('my_tagger.dill', 'rb') as f:
#     tagger = dill.load(f)

# print('Model Loaded')
# hmm_tagger.tag(sent)


def test_fn(test_sent):

    with open('my_tagger.dill', 'rb') as f:
        tagger = dill.load(f)
    out = tagger.tag(test_sent)
    tagged_out = [tags for _,tags in out]
    # print('Output :\n',tagged_out)
    return tagged_out



data_file = open("hi_hdtb-ud-test.conllu", "r", encoding="utf-8")
test_sentences=[]
for tokenlist in parse_incr(data_file):
    test_sentences.append(tokenlist)
# test_data_hn=[[(token['form'],token['upostag']) for token in sentence ]for sentence in test_sentences ]

test1=[token['form'] for token in test_sentences[10]]
print('input:\n',test1)
print(test_fn(test1))