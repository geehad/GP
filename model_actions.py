import spacy
import neuralcoref
from spacy import displacy
from colour import Color
from nltk.stem import WordNetLemmatizer
import re
import models_char



nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)

object_coref_list =[]

#################### action_category ####################
verb_noObject = ['dance']                                   #cat_num =1
verb_prep = ['walk','walk','sit','sleep','play']            #cat_num=2
verb_oneObject= ['carry','eat','push']                      #cat_num=3
verb_twoObject= ['shoot']                                   #cat_num=4


#########################################################

def get_model_id (models_info,model_name,model_char):
    model_id = -1

    for i in range(0, len(models_info)):

        if model_name == models_info[i][1]:

            char_mentioned = []
            for j in range(0, len(model_char)):
                if model_char[j] != "none" and model_char[j] != -1:
                    char_mentioned.append(model_char[j])

            all_char_mentioned_found = 0

            if (all(x in models_info[i][2] for x in char_mentioned)):
                all_char_mentioned_found = 1

            if (all_char_mentioned_found):
                model_id = models_info[i][3]
                break

    return model_id

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

##################################################################################################
def get_objectCoref_map(input_text):  ################################################################ zai ma maktoob msh bageeb el lower wla 7aga 3shan law htt3dl

    doc=nlp(input_text)
    for i in range(0, len(doc._.coref_clusters)):
        clusters_coref = doc._.coref_clusters
        object_coref = doc._.coref_clusters[i].mentions[-1]._.coref_cluster.main

        for j in range(1, len(clusters_coref[i])):
            object_coref_list.append((object_coref, clusters_coref[i][j]))

##################################################################################################

def detect_object_type (model_name,obj_coref):
    model_type = ""
    ##### 1- check if human
    current_model = model_name.lower()
    if current_model in models_char.boy_synonymy:
        model_type = "boy"
    elif current_model in models_char.girl_synonymy:
        model_type = "girl"
    elif current_model in models_char.man_synonymy:
        model_type = "man"
    elif current_model in models_char.woman_synonymy:
        model_type = "woman"
    elif current_model in models_char.boy_girl_synonymy:  # law mfesh coref , eh el default ???
        found_coref = False
        for i in range(0, len(obj_coref)):
            if current_model == obj_coref[i][0]:

                found_coref = True

                ## if coref is He
                if obj_coref[i][1] == 'he':
                    model_type = "boy"
                elif obj_coref[i][1] == 'she':
                    model_type = "girl"

                obj_coref.remove(obj_coref[i])

        if (not found_coref):
            model_type = "boy"  # -----------------> default is boy

    elif current_model in models_char.man_woman_synonymy:  # law mfesh coref , eh el default ???
        found_coref = False
        for i in range(0, len(obj_coref)):
            if current_model == obj_coref[i][0]:

                found_coref = True

                ## if coref is He
                if obj_coref[i][1] == 'he':
                    model_type = "man"
                elif obj_coref[i][1] == 'she':
                    model_type = "woman"

                obj_coref.remove(obj_coref[i])

        if (not found_coref):
            model_type = "man"  # -----------------> default is man

    #### 2- not human

    else:
        if (str(model_name) in models_char.models_avail) or (str(model_name) == 'boy') or (str(model_name) == 'girl') or (
                str(model_name) == 'man') or (str(model_name) == 'woman'):
            model_type = str(model_name)
        else:
            model_type = 'none'

    return model_type, obj_coref


def detect_object_char (model_type, model_word):
    object_chars = []

    if (
            model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
        object_chars = [-1, "none", -1]  # not mentioned,  not mentioned , not mentioned
    else:
        object_chars = ["none", -1]  # not mentioned, not mentioned

    is_tall = False
    is_short = False
    is_old = False
    is_big = False
    is_small = False
    is_color = False

    ############## find first adj ##############

    found_newAdj = False

    #print("pobj_word", model_word)
    for child in model_word.children:
        #print("child", str(child))

        if child.dep_ == "amod":
            found_newAdj = True

            ####### append only the specific char #################
            ## 1- check if human
            if (
                    model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
                if str(child) in models_char.tall_synonymy:
                    is_tall = True
                    object_chars[2] = 2
                elif str(child) in models_char.short_synonymy:
                    is_short = True
                    object_chars[2] = 0

                elif str(child) in models_char.old_synonymy:
                    is_old = True
                    object_chars[0] = 1

            ## 2- not human
            else:
                if str(child) in models_char.big_synonymy:
                    is_big = True
                    object_chars[1] = 2
                elif str(child) in models_char.small_synonymy:
                    is_small = True
                    object_chars[1] = 0

                elif models_char.check_color(str(child)):
                    is_color = True
                    object_chars[0] = str(child)

            current_word = child

    ############ find conj adjs ###############

    while (found_newAdj):
        found_newAdj = False
        for child in current_word.children:
            if child.dep_ == "conj":
                found_newAdj = True
                current_word = child

                ## 1- check if human
                if (
                        model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
                    if str(child) in models_char.tall_synonymy:
                        is_tall = True
                        object_chars[2] = 2

                    elif str(child) in models_char.short_synonymy:
                        is_short = True
                        object_chars[2] = 0

                    elif str(child) in models_char.old_synonymy:
                        is_old = True
                        object_chars[0] = 1

                ## 2- not human
                else:
                    if str(child) in models_char.big_synonymy:
                        is_big = True
                        object_chars[1] = 2
                    elif str(child) in models_char.small_synonymy:
                        is_small = True
                        object_chars[1] = 0
                    elif models_char.check_color(str(child)):
                        is_color = True
                        object_chars[0] = str(child)

        if (((is_tall or is_short) and is_old) or (
                (is_big or is_small) and is_color)):  # edit --> add new features
            break

    return object_chars


def extract_models_actions(input_text,models_fullInfo):

    object_coref = models_char.get_coref(input_text)

    get_objectCoref_map(input_text)

    lemmatizer = WordNetLemmatizer()
    tokinized_sentences = []
    doc = nlp(input_text)

    for sent in doc.sents:
        tokinized_sentences.append(str(sent.text))


    models_actions = []

    sentence_index = -1

    for sent in doc.sents:
        #print("sent : ",sent)
        sentence_index += 1

        tokens_in_currentSentence = []

        for word in sent:
            tokens_in_currentSentence.append(str(word))

            verb = subj = obj = ""
            if word.pos_ == "VERB" and  ((lemmatizer.lemmatize(str(word), 'v') in verb_noObject ) or (lemmatizer.lemmatize(str(word), 'v') in verb_prep) or (lemmatizer.lemmatize(str(word), 'v') in verb_oneObject) or (lemmatizer.lemmatize(str(word), 'v') in verb_twoObject) ):
                verb = lemmatizer.lemmatize(str(word), 'v')

                obj_word = word
                subj_word = word

                subj_id = -1
                obj1_id = -1
                obj2_id = -1

                ###################### find objects ##################
                if (verb in verb_oneObject) or (verb in verb_twoObject):
                    for child in word.children:

                        if child.dep_ == "dobj":

                            if child.pos_ == "PRON":
                                token_index = child.i - sent.start
                                # print("token value : ", child.text)
                                # print("token_index : ",token_index)
                                text_preceding = ""
                                for i in range(0, sentence_index):
                                    text_preceding += tokinized_sentences[i]

                                last_sentence = ""
                                for i in range(0, token_index):
                                    last_sentence += tokens_in_currentSentence[i] + " "
                                    if i == token_index - 1:
                                        last_sentence += "."

                                text_preceding += last_sentence

                                # print("text_preceding : ", text_preceding)
                                no_preceding_pron = count_PRON(text_preceding)
                                # print("no_preceding_pron : ",no_preceding_pron)
                                pron_num = no_preceding_pron + 1
                                # coref = doc._.coref_clusters[pron_num-1].mentions[-1]._.coref_cluster.main
                                coref = object_coref_list[pron_num - 1][0]
                                # print("coref : ",coref)

                                #######################objects.append(str(coref))      ---------------------> detect type and char


                            else:

                                obj_word = child
                                ################################## detect object type ####################################
                                model_type, object_coref = detect_object_type(str(obj_word), object_coref)
                                if model_type == 'none':
                                    continue
                                ################################## detect obj_chars ###########################################
                                object_chars = []
                                object_chars = detect_object_char(model_type, obj_word)
                                print(str(obj_word), object_chars)
                                obj1_id = get_model_id(models_fullInfo, str(obj_word), object_chars)

                if (verb in verb_prep) or (verb in verb_twoObject):


                    for child in word.children:

                        if child.dep_ == "prep":
                            print("Enter prep :" , str(child))
                            current_word = child
                            for child_current_word in current_word.children:
                                if child_current_word.dep_ == "pobj":

                                    obj_word = child_current_word

                                    ################################## detect object type ####################################
                                    model_type, object_coref = detect_object_type(str(obj_word), object_coref)
                                    if model_type == 'none':
                                        continue
                                    ################################## detect obj_chars ###########################################
                                    object_chars = []
                                    object_chars = detect_object_char(model_type, obj_word)
                                    print(str(obj_word), object_chars)
                                    obj_id = get_model_id(models_fullInfo, str(obj_word), object_chars)

                                    if verb in verb_twoObject:
                                        print("enter prep verb_twoObject : ",verb)
                                        obj2_id=obj_id
                                    else:
                                        obj1_id = obj_id

                ############################################## find sujects ###############################################
                for child in word.children:
                    ######### first subject ###############
                    if child.dep_ == "nsubj":
                        ###### check if it is a PRON , then get its coreference , otherwise put it as it is ######
                        ### get the num of pronouns preceding it from the start
                        if child.pos_ == "PRON":
                            token_index = child.i-sent.start
                            #print("token value : ", child.text)
                            #print("token_index : ",token_index)
                            text_preceding = ""
                            for i in range(0, sentence_index):
                                text_preceding += tokinized_sentences[i]

                            last_sentence = ""
                            for i in range(0, token_index):
                                last_sentence += tokens_in_currentSentence[i] + " "
                                if i == token_index - 1:
                                    last_sentence += "."

                            text_preceding += last_sentence

                            #print("text_preceding : ", text_preceding)
                            no_preceding_pron = count_PRON(text_preceding)
                            #print("no_preceding_pron : ",no_preceding_pron)
                            pron_num = no_preceding_pron + 1
                            #coref = doc._.coref_clusters[pron_num-1].mentions[-1]._.coref_cluster.main
                            coref = object_coref_list[pron_num-1][0]
                            #print("coref : ",coref,"verb : ",verb)

                            subj = str(coref)
                            ##############################action = (verb, subj, objects)      ----------> to do handle
                            ##############################models_actions.append(action)

                        else:

                            subj_word = child
                            ################################## detect subj type ####################################
                            model_type, object_coref = detect_object_type(str(subj_word), object_coref)
                            if model_type == 'none':
                                continue
                            ################################# find subj chars #######################################
                            object_chars = []
                            object_chars = detect_object_char(model_type, subj_word)
                            print(str(subj_word), object_chars)
                            subj_id = get_model_id(models_fullInfo,str(subj_word), object_chars)

                            ################################# Add a new action to action list #######################

                            # action --> cat_num,verb_name,subj_id,obj1_id,obj2_id,action_pos
                            if verb in verb_noObject:
                                action = (1,verb, subj_id, obj1_id,obj2_id,word.i)
                            elif verb in verb_prep :
                                action = (2, verb, subj_id, obj1_id, obj2_id,word.i)
                            elif verb in verb_oneObject:
                                action = (3, verb, subj_id, obj1_id, obj2_id,word.i)
                            else:
                                action = (4, verb, subj_id, obj1_id, obj2_id,word.i)


                            models_actions.append(action)


    return models_actions


"""models_info = []

models_info.append(['box','box',['green',2],1])
models_info.append(['car','car',['black',1],2])
models_info.append(['computer','computer',['red',2],3])
models_info.append(['box','box',['green',1],4])
models_info.append(['man','man',[1,"",2],5])
models_info.append(['man','man',[1,"",0],6])
models_info.append(['chair','chair',['red',0],7])
models_info.append(['boy','boy',[0,"",2],8])
models_info.append(['gun','gun',['black',1],9])"""




#print(extract_models_actions("There is an old tall man. There is a huge green box. The tall man walks towards the green box.",models_info))
#print(extract_models_actions("The short man shoots the boy with a black gun.",models_info))
