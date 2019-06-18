import spacy
from spacy import displacy
from colour import Color
import neuralcoref

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)



#############################################################################################################
boy_synonymy =['boy','guy','son','brother']
girl_synonymy =['girl','daughter']
boy_girl_synonymy=['child','kid','infant','toddler']

man_synonymy =['man','father','husband','gentleman']
woman_synonymy=['woman','lady','mother','wife','gentlewoman']
man_woman_synonymy=['teacher','doctor']

############ human features #############################
tall_synonymy = ['tall','lanky','soaring','giant','lofty']
old_synonymy = ['old','aged','elderly','senile','antiquated','ancient']
########################################################

########### Model features ##############################
big_synonymy = ['big','large','massive','enormous','huge','gigantic','sizable','tremendous','colossal','immense']

##########################################################

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

    model_chars = {}

    for sent in doc.sents:
        for word in sent:
            if word.pos_ == "NOUN":

                #################### detect model type ##############################
                model_type = ""
                ##### 1- check if human
                current_model = (str(word)).lower()
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
                    model_type=str(word)

                ########################################################################################

                ############################## detect model characteristics ############################
                object_chars = []

                if (model_type == 'boy' or model_type == 'girl' or model_type == 'man' or model_type == 'woman'):
                    object_chars = [False,False,""]    # is_tall,is_old,hair_color
                else:
                    object_chars = [False,""]  # is_big,color

                is_tall = False
                is_old = False
                is_big = False
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
                               object_chars[0] = True

                           elif str(child) in old_synonymy:
                               is_old = True
                               object_chars[1] = True

                        ## 2- not human
                        else:
                            if str(child) in big_synonymy:
                                is_big = True
                                object_chars[0] = True
                            elif check_color(str(child)):
                                is_color = True
                                object_chars[1] = str(child)

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
                                    object_chars[0] = True

                                elif str(child) in old_synonymy:
                                    is_old = True
                                    object_chars[1] = True

                            ## 2- not human
                            else:
                                if str(child) in big_synonymy:
                                    is_big = True
                                    object_chars[0] = True
                                elif check_color(str(child)):
                                    is_color = True
                                    object_chars[1] = str(child)

                    if (  (is_tall and is_old) or  (is_big and is_color) ):       #edit --> add new features
                        break


                model_chars[model_type] = object_chars

    return model_chars





#displacy.serve(doc, style='dep')
#doc = nlp("The small and red and valuable book is on the table.")
#  doc = nlp("There is a red Haired boy.")

#print(extract_models_char("There is a tall and old teacher.He is happy. There is a red and huge box."))
print(extract_models_char("There is a beutiful and tall teacher. she is tall."))

