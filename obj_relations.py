import spacy
from spacy import displacy


nlp = spacy.load('en')

#doc = nlp("The cup is on the table and under the lamp and in the room")
#doc = nlp("The cup is on the table and under the lamp and in the room and a chair behind a table")
#doc = nlp("There is a cup on the table and a book in the room and a chair behind a table")
#doc = nlp("The present inside the big box is red")
#doc = nlp("The cup which is blue is on the table")
#doc = nlp("The cup Ahmed put is on the table")
doc = nlp("The boy was at his home")
#doc = nlp("The cup which is blue is on the table and under the lamp")

relations = []

for word in doc:
    current_prep=pnoun=pobj = " "
    if word.pos_ == "ADP":

        current_prep = str(word)

        #################################### find pnoun #########################################
        current_word = word
        while current_word.head.pos_ == "ADP":
            current_word = current_word.head
            print("Enter",str(current_word))
        if current_word.head.pos_ == "VERB":
            print("VERB",str(current_word.head))
            children_verb = current_word.head.children
            for child in children_verb:
                if child.dep_ == "nsubj":
                    pnoun = str(child)
        else:
            print("not Verb")
            pnoun = str(current_word.head)

        #########################################################################################

        #################################  find pobj ############################################
        for child in word.children:
            if child.dep_ == "pobj":
                pobj = str(child)
                rel = (current_prep, pnoun, pobj)
                relations.append(rel)

        ###########################################################################################


print(relations)

#displacy.serve(doc,style='dep')

