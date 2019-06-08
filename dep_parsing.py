#import spacy
#from spacy import displacy

#nlp=spacy.load('en')

#docx=nlp("yesterday a smart and beutiful boy go to the club")
#docx=nlp("The car is red and the building is tall and new")
#for word in docx:
    #print(word.text, word.dep_, word.head.text, word.head.pos_,
          #[child for child in word.children])

#displacy.serve(docx,style='dep')


import spacy
from spacy.symbols import amod,conj,acomp,advmod
from spacy import displacy

def dep_parsing(Objects,input_text):
    nlp = spacy.load('en')

    doc = nlp(input_text)

    noun_adj_pairs = {}
    temp=[]
    for x in Objects:
        for word in doc:
            if word.lemma_ == x:
                temp.append(x)
                for features in word.head.children:
                    if features.dep == acomp:
                        temp.append(str(features))
                        for conjFeatures in features.children:
                            if conjFeatures.dep == conj:
                                temp.append(str(conjFeatures))
                for features in word.children:
                    if features.dep == amod:
                        temp.append(str(features))
                        for conjFeatures in features.children:
                            if conjFeatures.dep == conj:
                                temp.append(str(conjFeatures))
                #noun_adj_pairs.append(temp)
                noun_adj_pairs[x]=temp
                temp=[]


    print("Features are ",noun_adj_pairs)
    # displacy.serve(docx,style
