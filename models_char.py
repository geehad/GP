import spacy
from spacy import displacy
from colour import Color

nlp = spacy.load('en')


######################### return true if it is a valid color name otherwise return false ######################
def check_color(color):
    try:
        Color(color)
        return True
    except ValueError:
        return False
##############################################################################################################

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



doc = nlp("The small and red and valuable book is on the table.")
#doc = nlp("There is a red Haired boy.")

model_chars = {}

for sent in doc.sents:
    for word in sent:
        if word.pos_ == "NOUN":

            object_chars = []
            ############## find first adj ##############
            for child in word.children:
                if child.dep_ == "amod":
                    object_chars.append(str(child))  ### edit ----------> select specific features only
                    current_word = child


            ############ find conj adjs ###############
            found_newAdj = True

            while (found_newAdj):
                found_newAdj = False
                for child in current_word.children:
                    if child.dep_ == "conj":
                        found_newAdj = True
                        current_word = child
                        object_chars.append(str(child))  ### edit ----------> select specific features only

            model_chars[str(word)]=object_chars

print(model_chars)


displacy.serve(doc, style='dep')

