import spacy
import neuralcoref
from spacy import displacy
from nltk.stem import WordNetLemmatizer
import re



nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


#parsed_origin_senstence= nlp("The boy with brown hair played football")
#parsed_origin_senstence= nlp("The boy with brown hair was playing football")
#parsed_origin_senstence= nlp("John drinks a juice")
#parsed_origin_senstence= nlp("John and mary drink some juice")
#parsed_origin_senstence= nlp("John and mary and alice drink some juice")
#parsed_origin_senstence= nlp("John , mary , alice and bob drink some juice")
#parsed_origin_senstence= nlp("John and mary drink some juice in a coffee")
#parsed_origin_senstence= nlp("John cooked alice a delicious meal")


####################################parsed_origin_senstence= nlp("John and mary drink in a coffee some juice")   --> drink is NOUN ??????

def count_PRON(input_text):
    count_pron = 0
    tokinized_sentences = input_text.split('.')
    for sentence in tokinized_sentences:
        parsed_sentence = nlp(sentence)
        for word in parsed_sentence:
            if word.pos_ == "PRON":
                count_pron += 1

    return  count_pron


def extract_models_actions(input_text):

    lemmatizer = WordNetLemmatizer()
    #tokinized_sentences = re.split('(.)', input_text)  ########################### to do -> edit split
    #tokinized_sentences = input_text.split('.')         ########################### to do -> edit split
    tokinized_sentences = []
    doc = nlp(input_text)
    #print(tokinized_sentences)
    for sent in doc.sents:
        tokinized_sentences.append(str(sent.text))

    print("tokinized_sentences : ",tokinized_sentences)
    # verb , subject , [obj1 , obj2]
    models_actions = []

    sentence_index = -1

    for sent in doc.sents:
        print("sent : ",sent)
        sentence_index += 1

        #print("sentence is : ", sentence)
        #parsed_sentence = nlp(sent)

        tokens_in_currentSentence = []

        for word in sent:
            tokens_in_currentSentence.append(str(word))

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
                        ###### check if it is a PRON , then get its coreference , otherwise put it as it is ######
                        ### get the num of pronouns preceding it from the start
                        if child.pos_ == "PRON":
                            token_index = child.i-sent.start
                            print("token value : ", child.text)
                            print("token_index : ",token_index)
                            text_preceding = ""
                            for i in range(0, sentence_index):
                                text_preceding += tokinized_sentences[i]

                            last_sentence = ""
                            for i in range(0, token_index):
                                last_sentence += tokens_in_currentSentence[i] + " "
                                if i == token_index - 1:
                                    last_sentence += "."

                            text_preceding += last_sentence

                            print("text_preceding : ", text_preceding)
                            no_preceding_pron = count_PRON(text_preceding)
                            print("no_preceding_pron : ",no_preceding_pron)
                            pron_num = no_preceding_pron + 1
                            coref = doc._.coref_clusters[pron_num-1].mentions[-1]._.coref_cluster.main
                            print("coref : ",coref)

                            subj = str(coref)
                            action = (verb, subj, objects)
                            models_actions.append(action)

                        else:
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



print(extract_models_actions("My sister has a dog and she loves it. My mother has a cat and she loves it. My brother has a cat and he loves it."))


