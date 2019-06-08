
from Obj_detection import detect_Obj
from dep_parsing import dep_parsing
from Scene_Inference import support_inference
#input_text = 'There was an old owl that lived in an oak. Yesterday he saw a boy helping an old man to carry a heavy basket. Today he saw a girl shouting at her mother'
#input_text = 'There are two boys playing football in a club'
#input_text = 'There are two boys playing with ball in a club'
#input_text='The girl washes the dishes'
#input_text='I played with a beautiful girl and a green ball'    #wolves -> wolf not wolv so use lemmatization not stemming
#input_text="I saw two big and beutiful dogs"
#input_text="I saw a slightly red flower"
#input_text = "I saw a red and big flower"
#input_text = "I saw a red and big flower"
#input_text = "There is a Computer in a Room"

#input_text = "I saw a very big man"   -- > to do (parsing) give big only
#input_text = "yesterday a smart and beutiful boy go to the club"   ---> smart Noun !! spacy sa7 !!


#input_text = "There is a piece of cake on a table"  -----> not handled


#input_text = 'There was an old owl that lived in an oak. Yesterday he saw a boy helping an old man to carry a heavy basket. Today he saw a girl shouting at her mother'

#input_text = "There is a Room with a Table and a Fork . There is a red Chair to the right of the Table"
#input_text = "There is a Computer in a Room"

#input_text = 'There was an old owl that lived in an oak. Yesterday he saw a boy helping an old man to carry a heavy basket. Today he saw a girl shouting at her mother'

input_text = 'There are two boys playing football in a club'
objects=detect_Obj(input_text)
dep_parsing(objects,input_text)
print("objects are : ",objects)
#print(support_inference(objects))
