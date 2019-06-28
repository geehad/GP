import spacy
from spacy import displacy
from colour import Color
from nltk.stem import WordNetLemmatizer
import neuralcoref

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)

lemmatizer = WordNetLemmatizer()

# human age(small(default),old) hair(default(none)) tall(default(1 -> meduim) , 0->short , 2->tall)
#model color(default->none)  size(1->meduim , 0->small , 2->big)

#############################################################################################################
boy_synonymy =['boy','guy','son','brother']
girl_synonymy =['girl','daughter']
boy_girl_synonymy=['child','kid','infant','toddler']

man_synonymy =['man','father','husband','gentleman']
woman_synonymy=['woman','lady','mother','wife','gentlewoman']
man_woman_synonymy=['teacher','doctor']

############ human features #############################
tall_synonymy = ['tall','lanky','soaring','giant','lofty']
short_synonymy = ['short','little','tiny','shortened','stumpy','scrubby','squabby']
old_synonymy = ['old','aged','elderly','senile','antiquated','ancient']
#########################################################

############ Available model(non humans) ################
models_avail = ['bed','chair','ball','plate','food','television','table','bat','box','computer','laptop','car','bottle','cup','couch','toy','knife','sword','desk','piano','gun','playground','room','street','kitchen']

########### Model features ##############################
big_synonymy = ['big','large','massive','enormous','huge','gigantic','sizable','tremendous','colossal','immense']
small_synonymy = ['small','little','tiny']

##########################################################
determiners_newObject = ['a','an','another']
determiners_oldObject = ['the']

######################### check_color  return true if it is a valid color name otherwise return false ######################
def check_color(color):
    try:
        Color(color)
        return True
    except ValueError:
        return False
##############################################################################################################

####################### get_coref   return corefernce of each noun in the input text ########################

def get_coref (input_text):

    doc = nlp(input_text)
    object_coref =[]
    for token in doc:
        if token.pos_ == 'PRON' and token._.in_coref:
            for cluster in token._.coref_clusters:
                object_coref.append((str(cluster.main.text).split()[-1],str(token.text).lower()))

    return object_coref

#############################################################################################################
def extract_models_char(input_text):

    object_coref = get_coref(input_text)
    print(object_coref)

    doc = nlp(input_text)


    unique_id = 1         # auto increment id
    model_full_info=[]    # actual model name(in text) , origin model name (in database) , model chars , unique id

    #model_chars = {}

    for sent in doc.sents:
        for word in sent:
            if word.pos_ == "NOUN":

                num_same_objects = 1  ################## ---------------------------- what is the max num of objects ?
                root_word = lemmatizer.lemmatize(str(word))

                ####################  detect num of same objects #####################   -----------> what is the max no. of objects ??
                for child in word.children:

                    if child.dep_ == "nummod":
                        if str(child) == "two":
                            num_same_objects = 2
                        elif str(child) == "three":
                            num_same_objects = 3
                        elif str(child) == "four":
                            num_same_objects = 4
                        elif str(child) == "five":
                            num_same_objects = 5
                        elif str(child) == "six":
                            num_same_objects = 6
                        elif str(child) == "seven":
                            num_same_objects = 7
                        elif str(child) == "eight":
                            num_same_objects = 8
                        elif str(child) == "nine":
                            num_same_objects = 9
                        else:
                            num_same_objects = 10   ################################### consider max is 10

                #################### detect model type ##############################
                model_type = ""
                ##### 1- check if human
                current_model = root_word.lower()
                if current_model in boy_synonymy:
                    model_type = "boy"
                elif current_model in girl_synonymy:
                    model_type = "girl"
                elif current_model in man_synonymy:
                    model_type = "man"
                elif current_model in woman_synonymy:
                    model_type = "woman"
                elif current_model in boy_girl_synonymy:      # law mfesh coref , eh el default ???
                    found_coref = False
                    for i in range(0,len(object_coref)):
                        if current_model == object_coref[i][0]:

                            found_coref = True

                            ## if coref is He
                            if object_coref[i][1] == 'he':
                                model_type = "boy"
                            elif object_coref[i][1] == 'she':
                                model_type = "girl"

                            object_coref.remove(object_coref[i])

                    if(not found_coref):
                        model_type = "boy"    #-----------------> default is boy

                elif current_model in man_woman_synonymy:  # law mfesh coref , eh el default ???
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
                    if root_word in models_avail:
                        model_type = root_word
                    else:
                        continue


                ########################################################################################

                ############################## detect model characteristics ############################
                object_chars = []

                if (model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
                    object_chars = [0,"none",1]    # not old, no color of hair , meduim height
                else:
                    object_chars = ["none",1]  # no color, meduim size


                is_tall = False
                is_short = False
                is_old = False
                is_big = False
                is_small = False
                is_color = False

                ############## find first adj ##############

                found_newAdj = False

                for child in word.children:

                    if child.dep_ == "amod":
                        found_newAdj = True

                        ####### append only the specific char #################
                        ## 1- check if human
                        if (model_type == 'boy' or model_type == 'girl' or model_type == 'man'  or model_type == 'woman'):
                           if str(child) in tall_synonymy:
                               is_tall = True
                               object_chars[2] = 2
                           elif str(child) in short_synonymy:
                               is_short = True
                               object_chars[2] = 0

                           elif str(child) in old_synonymy:
                               is_old = True
                               object_chars[0] = 1

                        ## 2- not human
                        else:
                            if str(child) in big_synonymy:
                                is_big = True
                                object_chars[1] = 2
                            elif str(child) in small_synonymy:
                                is_small = True
                                object_chars[1] = 0

                            elif check_color(str(child)):
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
                            if (model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
                                if str(child) in tall_synonymy:
                                    is_tall = True
                                    object_chars[2] = 2

                                elif str(child) in short_synonymy:
                                    is_short = True
                                    object_chars[2] = 0

                                elif str(child) in old_synonymy:
                                    is_old = True
                                    object_chars[0] = 1

                            ## 2- not human
                            else:
                                if str(child) in big_synonymy:
                                    is_big = True
                                    object_chars[1] = 2
                                elif str(child) in small_synonymy:
                                    is_small = True
                                    object_chars[1] = 0
                                elif check_color(str(child)):
                                    is_color = True
                                    object_chars[0] = str(child)

                    if (  (  (is_tall or is_short) and is_old) or  ( (is_big or is_small) and is_color) ):       #edit --> add new features
                        break

                #check if it is a new object or not
                is_newObject = False
                if word.head.pos_ == "VERB" and str(word.head) == "are" :
                    for verb_child in word.head.children :
                        if verb_child.dep_ == "expl":
                            is_newObject= True
                else:
                    for each_child in word.children:
                        if each_child.dep_ == "det":
                            if str(each_child) in determiners_newObject:
                                is_newObject = True


                if(is_newObject):
                    for i in range(0,num_same_objects):
                        model_full_info.append([str(word), model_type, object_chars, unique_id])
                        unique_id = unique_id + 1



    return model_full_info



#print(extract_models_char("There is a tall and old teacher.He is happy. There is a red and huge box."))
#print(extract_models_char("There is a red box. There is a green box. The red box is on a black table."))
#print(extract_models_char("There are two red huge boxes and there is another green box."))
