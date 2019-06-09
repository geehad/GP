import spacy
from spacy import displacy


nlp = spacy.load('en')

#doc = nlp("The cup is on the table and under the lamp and in the room")
#doc = nlp("The cup is on the table and under the lamp and in the room and a chair behind a table")
#doc = nlp("There is a cup on the table and a book in the room and a chair behind a table")
#doc = nlp("The cup which is blue is on the table")
#doc = nlp("The cup Ahmed put is on the table")
#doc = nlp("The boy was at his home")
#doc = nlp("The cup which is blue is on the table and under the lamp")
#doc = nlp("The table is opposite the door")
#doc = nlp("The boy is right of the table")
#doc = nlp("The boy was setting on the chair")
#doc = nlp("The boy placed his book on the table")
#doc = nlp("There is a cat under the red table")
#doc = nlp("The present inside the big box is red")
#doc = nlp("The boy was to the left of the table")

#doc = nlp("The car is parked in front of the garden")
doc = nlp("There is a red chair to the right of the table")



relations = []

for word in doc:
    current_prep=pnoun=pobj = " "
    if word.pos_ == "ADP":

        current_prep = str(word)

        #################################### find pnoun #########################################
        current_word = word
        while current_word.head.pos_ == "ADP" or (current_word.head.pos_ == "NOUN" and current_word.head.dep_ == "pobj"):
                if (current_word.head.pos_ == "NOUN" and current_word.head.dep_ == "pobj"):
                    current_prep = str(current_word.head)

                current_word = current_word.head
                print("Enter", word,str(current_word))

        if current_word.head.pos_ == "VERB":
            print("VERB",str(current_word.head))
            children_verb = current_word.head.children
            for child in children_verb:
                if child.dep_ == "nsubj" or child.dep_ == "nsubjpass":
                    pnoun = str(child)
        else:
            print("not Verb")
            pnoun = str(current_word.head)

        #########################################################################################

        #################################  find pobj ############################################
        for child in word.children:
            if child.dep_ == "pobj":
                child_refer_to_prep = False
                for Child in child.children:
                    if Child.dep_ == "prep":
                        child_refer_to_prep = True
                        break
                if not child_refer_to_prep:
                    print("push" , word)
                    pobj = str(child)
                    rel = (current_prep, pnoun, pobj)
                    relations.append(rel)


        ###########################################################################################


print(relations)

displacy.serve(doc,style='dep')

