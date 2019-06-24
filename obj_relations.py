import spacy
from spacy import displacy
import re

nlp = spacy.load('en')

def Objs_relations(input_text):

    tokinized_sentences = re.split('(\.)', input_text)      ########################### to do -> edit split

    relations = []

    for sentence in tokinized_sentences:
        #print("sentence is : ",sentence)
        parsed_sentence=nlp(sentence)
        for word in parsed_sentence:
            current_prep = pnoun = pobj = " "
            if word.pos_ == "ADP":

                current_prep = str(word)

                #################################### find pnoun #########################################
                current_word = word
                while current_word.head.pos_ == "ADP" or (
                        current_word.head.pos_ == "NOUN" and current_word.head.dep_ == "pobj"):
                    if (current_word.head.pos_ == "NOUN" and current_word.head.dep_ == "pobj"):
                        current_prep = str(current_word.head)

                    current_word = current_word.head
                    #print("Enter", word, str(current_word))

                if current_word.head.pos_ == "VERB":
                    #print("VERB", str(current_word.head))
                    children_verb = current_word.head.children

                    if current_word.head.dep_ == "acl":
                        pnoun = str(current_word.head.head)
                        #print("pnoun ",pnoun)
                    else:
                        for child in children_verb:
                            if child.dep_ == "nsubj" or child.dep_ == "nsubjpass":
                                pnoun = str(child)

                else:
                    #print("not Verb")
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
                            #print("push", word)
                            pobj = str(child)
                            rel = (current_prep, pnoun, pobj)
                            relations.append(rel)

                ###########################################################################################
        #displacy.serve(parsed_sentence, style='dep')

    return relations



