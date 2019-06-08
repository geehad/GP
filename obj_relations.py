import spacy
from spacy import displacy


nlp = spacy.load('en')
doc = nlp("The cup which is blue is on the table")
#doc = nlp("The cup Ahmed put is on the table")
########################doc = nlp("The cup which is blue is on the table and under the lamp")
########################doc = nlp("The present inside the big box is mine")

relations = []

for word in doc:
    prep=pnoun=pobj = " "
    if word.pos_ == "ADP":
        prep = str(word)
        children = word.children
        for child in children:
            if child.dep_ == "pobj":
                pobj = str(child)

        word_head = word.head
        children_verb = word_head.children
        for child in children_verb:
            if child.dep_ == "nsubj":
                pnoun = str(child)


    if prep != " ":
        rel = (prep,pnoun,pobj)
        relations.append(rel)

print(relations)

displacy.serve(doc,style='dep')

