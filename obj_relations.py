import spacy
from spacy import displacy
from colour import Color
from nltk.stem import WordNetLemmatizer
import models_char
import re

nlp = spacy.load('en')

lemmatizer = WordNetLemmatizer()


################################################################################################
rel_avail = ['in','on','behind','front','right','left']
################################################################################################


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


##############################################################################################################

def Objs_relations(input_text,models_fullInfo):


    object_coref = models_char.get_coref(input_text)
    #print(object_coref)

    doc = nlp(input_text)

    relations = []

    for sentence in doc.sents:

        for word in sentence:
            current_prep = pnoun = pobj = " "

            pnoun_id = -1
            pobj_id = -1

            if word.pos_ == "ADP" and (str(word) in rel_avail )and (  (str(word.head.pos_) != "VERB") or (lemmatizer.lemmatize(str(word.head),'v') == "be" )):   #make sure that it isn't a prep with a verb

                pnoun_word = word
                pobj_word = word

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
                        pnoun_word=current_word.head.head
                        print("pnoun_word 1",pnoun_word)
                    else:
                        for child in children_verb:
                            if child.dep_ == "nsubj" or child.dep_ == "nsubjpass":
                                pnoun = str(child)
                                pnoun_word=child
                                print("pnoun_word 2", pnoun_word)


                else:
                    #print("not Verb")
                    pnoun = str(current_word.head)
                    pnoun_word=current_word.head
                    print("pnoun_word 3", pnoun_word)

                print("pnoun_word 22", pnoun_word)
                ################################## detect pnoun type ####################################
                model_type = ""
                ##### 1- check if human
                current_model = str(pnoun_word).lower()
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
                    for i in range(0, len(object_coref)):
                        if current_model == object_coref[i][0]:

                            found_coref = True

                            ## if coref is He
                            if object_coref[i][1] == 'he':
                                model_type = "boy"
                            elif object_coref[i][1] == 'she':
                                model_type = "girl"

                            object_coref.remove(object_coref[i])

                    if (not found_coref):
                        model_type = "boy"  # -----------------> default is boy

                elif current_model in models_char.man_woman_synonymy:  # law mfesh coref , eh el default ???
                    found_coref = False
                    for i in range(0, len(object_coref)):
                        if current_model == object_coref[i][0]:

                            found_coref = True

                            ## if coref is He
                            if object_coref[i][1] == 'he':
                                model_type = "man"
                            elif object_coref[i][1] == 'she':
                                model_type = "woman"

                            object_coref.remove(object_coref[i])

                    if (not found_coref):
                        model_type = "man"  # -----------------> default is man

                #### 2- not human

                else:
                    if str(pnoun_word) in models_char.models_avail:
                        model_type = str(pnoun_word)
                    else:
                        continue


                ################################## get pnoun char #######################################

                object_chars = []

                if (model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
                    object_chars = [-1, "none", -1]  # not mentioned, not mentioned , not mentioned
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

                print("pnoun_word",pnoun_word)
                for child in pnoun_word.children:
                    print("child",str(child))

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

                print(str(pnoun_word),object_chars)
                pnoun_id= get_model_id(models_fullInfo,pnoun,object_chars)
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
                            pobj_word = child

                            print("pnoun_pobj",pobj_word)

                            ################################## detect pnoun type ####################################
                            model_type = ""
                            ##### 1- check if human
                            current_model = str(pobj_word).lower()
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
                                for i in range(0, len(object_coref)):
                                    if current_model == object_coref[i][0]:

                                        found_coref = True

                                        ## if coref is He
                                        if object_coref[i][1] == 'he':
                                            model_type = "boy"
                                        elif object_coref[i][1] == 'she':
                                            model_type = "girl"

                                        object_coref.remove(object_coref[i])

                                if (not found_coref):
                                    model_type = "boy"  # -----------------> default is boy

                            elif current_model in models_char.man_woman_synonymy:  # law mfesh coref , eh el default ???
                                found_coref = False
                                for i in range(0, len(object_coref)):
                                    if current_model == object_coref[i][0]:

                                        found_coref = True

                                        ## if coref is He
                                        if object_coref[i][1] == 'he':
                                            model_type = "man"
                                        elif object_coref[i][1] == 'she':
                                            model_type = "woman"

                                        object_coref.remove(object_coref[i])

                                if (not found_coref):
                                    model_type = "man"  # -----------------> default is man

                            #### 2- not human

                            else:
                                if str(pobj_word) in models_char.models_avail:
                                    model_type = str(pobj_word)
                                else:
                                    continue

                            ################################## get pnoun char #######################################

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

                            print("pnoun_pobj", pobj_word)
                            for child in pobj_word.children:
                                print("child", str(child))

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

                            print(pobj, object_chars)
                            pobj_id = get_model_id(models_fullInfo, pobj, object_chars)
                            #########################################################################################


                            ######################################### add new relation ##############################
                            rel = [current_prep, pnoun,pnoun_id, pobj,pobj_id]
                            relations.append(rel)

                ###########################################################################################
        #displacy.serve(parsed_sentence, style='dep')

    return relations

