import nltk
from nltk.tokenize import  word_tokenize,sent_tokenize,TreebankWordTokenizer
from nltk.tree import Tree
from nltk.stem import PorterStemmer,WordNetLemmatizer


def detect_Obj(input_text):

    tokinized_sent = nltk.sent_tokenize(input_text)
    print (tokinized_sent)
    object_name = set()

    for i in tokinized_sent:
        #words_befor_Stem = TreebankWordTokenizer().tokenize(i)
        words_befor_Lemmatize = nltk.word_tokenize(i)
        words_Lemmatized = []  # stem only the plural noun
        #ps = PorterStemmer()
        WL=WordNetLemmatizer()

        tagged = nltk.pos_tag(words_befor_Lemmatize)    #list of tuples
        # print("tagged",tagged)

        for t in tagged:
            if t[1] == 'NNS':
                words_Lemmatized.append((WL.lemmatize(t[0]), 'NN'))
            else:
                words_Lemmatized.append(t)

        print("words_Lemmitized : ", words_Lemmatized)

        ChunkGram1 = r"""chunk1: {<DT><RB>*<JJ.?>*<CC>*<JJ.?>*<NN.?>} """  #a boy ,a tall boy, a tall and smart boy
        ChunkParser1 = nltk.RegexpParser(ChunkGram1)
        chunked1 = ChunkParser1.parse(words_Lemmatized)

        ChunkGram2 = r"""chunk2: {<PRP\$><NN>} """      #her mother
        ChunkParser2 = nltk.RegexpParser(ChunkGram2)
        chunked2 = ChunkParser2.parse(words_Lemmatized)

        ChunkGram3 = r"""chunk3: {<CD><NN>} """         #two boys
        ChunkParser3 = nltk.RegexpParser(ChunkGram3)
        chunked3 = ChunkParser3.parse(words_Lemmatized)

        ChunkGram4 = r"""chunk4: {<VB.?><NN.?>} """  # verb + NN/NNS
        ChunkParser4 = nltk.RegexpParser(ChunkGram4)
        chunked4 = ChunkParser4.parse(words_Lemmatized)

        ChunkGram5 = r"""chunk5: {<CD><JJ.?>*<CC>*<JJ.?>*<NN>} """  # two dogs , two big and scary dogs
        ChunkParser5 = nltk.RegexpParser(ChunkGram5)
        chunked5 = ChunkParser5.parse(words_Lemmatized)

        objects_chunks = []

        #not_found = True
        for elt in chunked1:
            if isinstance(elt, Tree):
                objects_chunks.append([word for word, tag in elt])


        for elt in chunked2:
            if isinstance(elt, Tree):
                objects_chunks.append([word for word, tag in elt])

        for elt in chunked3:
            if isinstance(elt, Tree):
                objects_chunks.append([word for word, tag in elt])


        for elt in chunked4:
            if isinstance(elt, Tree):
                objects_chunks.append([word for word, tag in elt])

        for elt in chunked5:
            if isinstance(elt, Tree):
                objects_chunks.append([word for word, tag in elt])


        print("objects_chunks : ", objects_chunks)
        # print("len :",len(objects_chunks))

        for obj_chunk in objects_chunks:
            object_name.add(obj_chunk[len(obj_chunk) - 1])

    #print(object_name)
    return object_name
