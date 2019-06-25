from models_char import extract_models_char
from obj_relations import Objs_relations
from model_actions import extract_models_actions
from Scene_Inference import support_inference

####################### files for the following modules ###########################
file_models_char = open("models_char.txt", "w")
file_models_actions = open("model_actions.txt", "w")
file_models_relations = open("models_relations.txt", "w")
##################################################################################
file_input_text = open("input_text.txt", "r")

###################### input text ###############################################     ---------- > take from GUI

input_text = file_input_text.read()
#print(input_text)
#input_text = "There is an old , tall and smart gentleman in a room. He has a small white cat and he carries it. There is a small black table behind a huge red chair. There is a black laptop to the right of a large brown bed."


################################################################################

models_info=extract_models_char(input_text)
relations_models=Objs_relations(input_text)
model_actions =extract_models_actions(input_text)

########################### write model chars ######################
for i in range(0,len(models_info)):
    current_model_name = models_info[i][1]
    current_model_chars = models_info[i][2]
    file_models_char.write(current_model_name + " ")
    for j in range(0, len(current_model_chars)):
        file_models_char.write(str(current_model_chars[j]) + " ")

    file_models_char.write(str(models_info[i][3]) + "\n")

########################## write model actions #######################   --------------> edit after finish
for i in range(0,len(model_actions)):
    file_models_actions.write(model_actions[i][1]+" ")
    file_models_actions.write(model_actions[i][0]+" ")
    list_objects = model_actions[i][2]
    for j in range(0,len(list_objects)):
        if len(list_objects) == 1:
            file_models_actions.write(list_objects[j]+"\n")
        elif len(list_objects) == 2 and j==0:
            file_models_actions.write(list_objects[j]+" ")
        else:
            file_models_actions.write(list_objects[j]+"\n")

########################### write models relations ####################   --------------> edit after finish
for i in range(0,len(relations_models)):
    file_models_relations.write(relations_models[i][0]+" "+relations_models[i][1]+" "+relations_models[i][2]+"\n")


#print(support_inference(objects))

