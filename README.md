# Hindi-dependency-parser
A project in course CS698O: Topics in Natural Language Processing offered in Winter 2020 at IIT Kanpur by Instructor Prof. Ashutosh Modi, IIT Kanpur.

## Developers:
* Abhishek Jaiswal
* A.V.S.D.S.Mahesh
* Tushar Shandilya

## Dependencies (Implemented and tested on these):
* Python 3.7
* flask 1.1.1
* flask-wtf 0.14.2
* flask-markdown 0.3
* nltk 3.4.5
* pygraphviz 1.3
* conllu 2.2.2
* scikit-learn 0.22.1
* dill 0.3.1.1

## Instructions:

Run the following from this directory to fetch the required data
```bash
> mkdir data
> cd data
> git clone https://github.com/UniversalDependencies/UD_Hindi-HDTB.git
> cd ..
```

Run the following to host the app at localhost:5000
```bash
> python app.py
```

