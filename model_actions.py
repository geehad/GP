import spacy
from spacy import displacy
from nltk.stem import WordNetLemmatizer
import re



nlp = spacy.load('en')

#parsed_origin_senstence= nlp("The boy with brown hair played football")
#parsed_origin_senstence= nlp("The boy with brown hair was playing football")
#parsed_origin_senstence= nlp("John drinks a juice")
#parsed_origin_senstence= nlp("John and mary drink some juice")
#parsed_origin_senstence= nlp("John and mary and alice drink some juice")
#parsed_origin_senstence= nlp("John , mary , alice and bob drink some juice")
#parsed_origin_senstence= nlp("John and mary drink some juice in a coffee")
#parsed_origin_senstence= nlp("John cooked alice a delicious meal")


####################################parsed_origin_senstence= nlp("John and mary drink in a coffee some juice")   --> drink is NOUN ??????

def extract_models_actions(input_text):

    lemmatizer = WordNetLemmatizer()
    tokinized_sentences = re.split('(\.)', input_text)  ########################### to do -> edit split
    # verb , subject , [obj1 , obj2]
    models_actions = []

    for sentence in tokinized_sentences:
        #print("sentence is : ", sentence)
        parsed_sentence = nlp(sentence)
        for word in parsed_sentence:
            verb = subj = obj = ""
            if word.pos_ == "VERB":
                verb = lemmatizer.lemmatize(str(word), 'v')

                ###################### find objects ##################
                count_no_objects = 0
                objects = []
                for child in word.children:
                    if child.dep_ == "dobj":
                        objects.append(str(child))
                        count_no_objects += 1
                    if (count_no_objects == 2):
                        break
                # print (objects)
                ######################################################

                ##################### find sujects ###################
                for child in word.children:
                    ######### first subject ###############
                    if child.dep_ == "nsubj":
                        subj = str(child)
                        action = (verb, subj, objects)
                        models_actions.append(action)
                        ######################################
                        ######### conj subjects ##############
                        current_subj = child
                        found_conj = True
                        while (found_conj):
                            found_conj = False
                            for child_of_subj in current_subj.children:
                                if child_of_subj.dep_ == "conj":
                                    subj = str(child_of_subj)
                                    action = (verb, subj, objects)
                                    models_actions.append(action)
                                    current_subj = child_of_subj
                                    found_conj = True
                    #####################################

        #displacy.serve(parsed_sentence, style='dep')

    return models_actions



#print(extract_models_actions("John drunk a juice in a coffee. John and alice eat some food in a resturant. John played football."))


