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
verb_prep = ['walk','move','sit','sleep','play']            #cat_num=2
verb_oneObject= ['carry','eat','push']                      #cat_num=3
verb_twoObject= ['shoot']                                   #cat_num=4


#########################################################

count_char = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth']
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


def get_objectCoref_map(input_text):

    doc=nlp(input_text)
    for i in range(0, len(doc._.coref_clusters)):
        clusters_coref = doc._.coref_clusters
        object_coref = doc._.coref_clusters[i].mentions[-1]._.coref_cluster.main

        #print("before object_coref : ",object_coref)

        object_coref_lst = str(object_coref).split(" ")

        if str(object_coref_lst[0]).lower() == "the":
            #print("Enter coref ")
            object_coref_lst[0] = "a"
            object_coref = ' '.join(object_coref_lst)

        #print("after object_coref : ", object_coref)

        if (str(clusters_coref[i][1]).lower() in models_char.male_pronoun) or (str(clusters_coref[i][1]).lower() in models_char.female_pronoun) or (str(clusters_coref[i][1]).lower() in models_char.rigid_pronoun):
                #print("enteeeeeeeeeeeeeeeeeer")
                object_coref_list.append((str(object_coref).lower(), str(clusters_coref[i][1]).lower()))
                #print("object_coref_list : ",object_coref_list)



##################################################################################################
def get_refrencedObject(pronoun):

    for i in range(0,len(object_coref_list)):
        print("object_coref_list[i][1] : ",object_coref_list[i][1])
        if  object_coref_list[i][1] == pronoun:
            return object_coref_list[i][0]

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
        object_chars = [-1, "none", -1,"none"]  # not mentioned age ,  not mentioned hair color, not mentioned height , copy number (the first,the second .....)
    else:
        object_chars = ["none", -1,"none"]  # not mentioned color, not mentioned size , copy number (the first,the second .....)

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
                elif str(child) in count_char:
                    object_chars[3]=str(child)

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
                elif str(child) in count_char:
                    object_chars[2] = str(child)

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

    print("object_coref_list : ",object_coref_list)

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

                                obj_pronoun = str(child.text).lower()
                                print("obj_pronoun : ", obj_pronoun)

                                coref_obj = get_refrencedObject(obj_pronoun)
                                print("coref_obj : ", coref_obj, "verb : ", verb)

                                objInfo = models_char.extract_models_char(coref_obj)
                                print("objInfo : ", objInfo)

                                coref_obj_word = ""
                                coref_obj_chars = []

                                for i in range(0, len(objInfo)):
                                    if objInfo[i][1] == 'boy' or objInfo[i][1] == 'man':
                                        if obj_pronoun in models_char.male_pronoun:
                                            coref_obj_word = objInfo[i][1]
                                            coref_obj_chars = objInfo[i][2]
                                            break
                                    elif objInfo[i][1] == 'girl' or objInfo[i][1] == 'woman':
                                        if obj_pronoun in models_char.female_pronoun:
                                            coref_obj_word = objInfo[i][1]
                                            coref_obj_chars = objInfo[i][2]
                                            break
                                    elif obj_pronoun in models_char.rigid_pronoun:
                                        coref_obj_word = objInfo[i][1]
                                        coref_obj_chars = objInfo[i][2]
                                        break


                                #print("coref_obj_word : ", coref_obj_word)
                                #print("coref_obj_chars : ", coref_obj_chars)
                                obj1_id = get_model_id(models_fullInfo, coref_obj_word, coref_obj_chars)


                            else:

                                obj_word = child
                                ################################## detect object type ####################################
                                model_type, object_coref = detect_object_type(str(obj_word), object_coref)
                                if model_type == 'none':
                                    continue
                                ################################## detect obj_chars ###########################################
                                object_chars = []
                                object_chars = detect_object_char(model_type, obj_word)
                                #print(str(obj_word), object_chars)
                                obj1_id = get_model_id(models_fullInfo, str(obj_word), object_chars)

                if (verb in verb_prep) or (verb in verb_twoObject):    #----------------------> add coref


                    for child in word.children:

                        if child.dep_ == "prep":
                            #print("Enter prep :" , str(child))
                            current_word = child
                            for child_current_word in current_word.children:
                                if child_current_word.dep_ == "pobj":

                                    #print("Enter pobj for prep")
                                    if child_current_word.pos_ == "PRON":

                                        obj_pronoun = str(child_current_word.text).lower()
                                        print("obj_pronoun : ", obj_pronoun)

                                        coref_obj = get_refrencedObject(obj_pronoun)
                                        print("coref_obj : ", coref_obj, "verb : ", verb)

                                        objInfo = models_char.extract_models_char(coref_obj)
                                        print("objInfo : ", objInfo)

                                        coref_obj_word = ""
                                        coref_obj_chars = []

                                        for i in range(0, len(objInfo)):
                                            if objInfo[i][1] == 'boy' or objInfo[i][1] == 'man':
                                                if obj_pronoun in models_char.male_pronoun:
                                                    coref_obj_word = objInfo[i][1]
                                                    coref_obj_chars = objInfo[i][2]
                                                    break
                                            elif objInfo[i][1] == 'girl' or objInfo[i][1] == 'woman':
                                                if obj_pronoun in models_char.female_pronoun:
                                                    coref_obj_word = objInfo[i][1]
                                                    coref_obj_chars = objInfo[i][2]
                                                    break
                                            elif obj_pronoun in models_char.rigid_pronoun:
                                                coref_obj_word = objInfo[i][1]
                                                coref_obj_chars = objInfo[i][2]
                                                break

                                        #print("coref_obj_word : ", coref_obj_word)
                                        #print("coref_obj_chars : ", coref_obj_chars)
                                        obj_id = get_model_id(models_fullInfo, coref_obj_word, coref_obj_chars)

                                        if verb in verb_twoObject:
                                            #print("enter prep verb_twoObject : ",verb)
                                            obj2_id = obj_id
                                        else:
                                            #print("enter prep verb_prep : ", verb)
                                            obj1_id = obj_id
                                            #print("obj1_id : ", obj1_id)


                                    else :

                                        obj_word = child_current_word

                                        ################################## detect object type ####################################
                                        model_type, object_coref = detect_object_type(str(obj_word), object_coref)
                                        if model_type == 'none':
                                            continue
                                        ################################## detect obj_chars ###########################################
                                        object_chars = []
                                        object_chars = detect_object_char(model_type, obj_word)
                                        #print(str(obj_word), object_chars)
                                        obj_id = get_model_id(models_fullInfo, str(obj_word), object_chars)

                                        if verb in verb_twoObject:
                                            # print("enter prep verb_twoObject : ",verb)
                                            obj2_id = obj_id
                                        else:
                                            obj1_id = obj_id


                 #print("obj1_id : ",obj1_id)
                ############################################## find subjects ###############################################

                found_subj = False

                print ("Verb : ",str(word))
                for child in word.children:
                    ######### first subject ###############
                    if child.dep_ == "nsubj":

                        print("find subject")

                        found_subj = True

                        found_conjSubject = True
                        current_subject = child

                        while found_conjSubject :

                            ###### check if it is a PRON , then get its coreference , otherwise put it as it is ######
                            ### get the num of pronouns preceding it from the start
                            if current_subject.pos_ == "PRON":

                                subj_pronoun = str(current_subject.text).lower()
                                print("subj_pronoun : ", subj_pronoun)

                                coref_subj = get_refrencedObject(subj_pronoun)
                                print("coref_subj : ", coref_subj, "verb : ", verb)

                                subjInfo = models_char.extract_models_char(coref_subj)
                                print("subjInfo : ", subjInfo)

                                coref_subj_word = ""
                                coref_subj_chars = []

                                for i in range(0, len(subjInfo)):
                                    if subjInfo[i][1] == 'boy' or subjInfo[i][1] == 'man':
                                        if subj_pronoun in models_char.male_pronoun:
                                            coref_subj_word = subjInfo[i][1]
                                            coref_subj_chars = subjInfo[i][2]
                                            break
                                        elif subjInfo[i][1] == 'girl' or subjInfo[i][1] == 'woman':
                                            if subj_pronoun in models_char.female_pronoun:
                                                coref_subj_word = subjInfo[i][1]
                                                coref_subj_chars = subjInfo[i][2]
                                                break
                                        elif subj_pronoun in models_char.rigid_pronoun:
                                            coref_subj_word = subjInfo[i][1]
                                            coref_subj_chars = subjInfo[i][2]
                                            break

                                # print("subj_word : ",coref_subj_word)
                                # print("subj_chars : ",coref_subj_chars)
                                coref_subj_id = get_model_id(models_fullInfo, coref_subj_word, coref_subj_chars)

                                ################################# Add a new action to action list #######################

                                # action --> cat_num,verb_name,subj_id,obj1_id,obj2_id,action_pos
                                if verb in verb_noObject:
                                    action = (1, verb, coref_subj_id, obj1_id, obj2_id, word.i)
                                elif verb in verb_prep:
                                    action = (2, verb, coref_subj_id, obj1_id, obj2_id, word.i)
                                elif verb in verb_oneObject:
                                    action = (3, verb, coref_subj_id, obj1_id, obj2_id, word.i)
                                else:
                                    action = (4, verb, coref_subj_id, obj1_id, obj2_id, word.i)

                                models_actions.append(action)

                            else:

                                subj_word = current_subject
                                ################################## detect subj type ####################################
                                model_type, object_coref = detect_object_type(str(subj_word), object_coref)
                                if model_type == 'none':
                                    continue
                                ################################# find subj chars #######################################
                                object_chars = []
                                object_chars = detect_object_char(model_type, subj_word)
                                print("subject : ",str(subj_word), object_chars)
                                subj_id = get_model_id(models_fullInfo, str(subj_word), object_chars)

                                ################################# Add a new action to action list #######################

                                # action --> cat_num,verb_name,subj_id,obj1_id,obj2_id,action_pos
                                if verb in verb_noObject:
                                    action = (1, verb, subj_id, obj1_id, obj2_id, word.i)
                                elif verb in verb_prep:
                                    action = (2, verb, subj_id, obj1_id, obj2_id, word.i)
                                elif verb in verb_oneObject:
                                    action = (3, verb, subj_id, obj1_id, obj2_id, word.i)
                                else:
                                    action = (4, verb, subj_id, obj1_id, obj2_id, word.i)

                                models_actions.append(action)

                                ###### check if there is a conj subject ########

                                found_conjSubject =False

                                for child_subj in current_subject.children:
                                    if child_subj.dep_ == "conj":
                                        current_subject = child_subj
                                        found_conjSubject = True
                                        break

                ######################################## if there are conj verbs of the same subject ######################

                if found_subj == False:

                    current_verb = word

                    while (found_subj) == False and current_verb.head.pos_ == "VERB":

                        current_verb = current_verb.head

                        for child_verb in current_verb.children:
                            if child_verb.dep_ == "nsubj":
                                found_subj = True
                                break

                    for verb_info in models_actions:
                        if verb_info[1] == lemmatizer.lemmatize(str(current_verb), 'v'):
                            subj_id = verb_info[2]

                    ################################# Add a new action to action list #######################

                    # action --> cat_num,verb_name,subj_id,obj1_id,obj2_id,action_pos
                    if verb in verb_noObject:
                        action = (1, verb, subj_id, obj1_id, obj2_id, word.i)
                    elif verb in verb_prep:
                        action = (2, verb, subj_id, obj1_id, obj2_id, word.i)
                    elif verb in verb_oneObject:
                        action = (3, verb, subj_id, obj1_id, obj2_id, word.i)
                    else:
                        action = (4, verb, subj_id, obj1_id, obj2_id, word.i)

                    models_actions.append(action)


    return models_actions


models_info = []

models_info.append(['box','box',['green',2,'first'],1])
models_info.append(['car','car',['black',1,'first'],2])
models_info.append(['computer','computer',['red',2,'first'],3])
models_info.append(['box','box',['green',1,'first'],4])
models_info.append(['man','man',[1,"",0,'first'],5])
models_info.append(['man','man',[1,"",0,'second'],6])
models_info.append(['chair','chair',['red',0,'first'],7])
models_info.append(['chair','chair',['red',0,'second'],8])
models_info.append(['boy','boy',[0,"",2,'first'],9])
models_info.append(['gun','gun',['black',1,'first'],10])
models_info.append(['girl','girl',[0,"",0,'first'],11])


#print(extract_models_actions("There is an old tall man. There is a huge green box. The tall man walks towards the green box.",models_info))
#print(extract_models_actions("The short man shoots the boy with a black gun.",models_info))
#print(extract_models_actions("There is an old , tall and smart gentleman in a room. He walks towards a red chair.",models_info))
#print(extract_models_actions("There is a green box. A tall boy carries it.",models_info))
#print(extract_models_actions("There is a red chair. A tall boy walks towards it.",models_info))
#print(extract_models_actions("There is a red chair.There is a tall boy. he walks towards it. he carries a green box.",models_info))
#print(extract_models_actions("There is a tall boy. There is an old man. There is a black gun. He shot him with it.",models_info))
#print(extract_models_actions("The boy moves towards the red chair and then he sits on it.",models_info))
#print(extract_models_actions("The boy moves towards the red chair and sits on it.",models_info))
#print(extract_models_actions("The boy moves towards the red chair and sits on it and carries it.",models_info))
#print(extract_models_actions("The boy is walking towards the red chair.",models_info))
#print(extract_models_actions("The boy is walking towards the red chair. the old man carries the green box.",models_info))
#print(extract_models_actions("The boy and the girl together walk towards the red chair.",models_info))
#print(extract_models_actions("The boy and the man and the girl all walk towards the second red chair.",models_info))
#print(extract_models_actions("The first short man carries the first red chair.",models_info))

