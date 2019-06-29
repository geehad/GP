import spacy
nlp = spacy.load('en')

class ModelsAction:
    def __init__(self,cat_num,action,subject,object1,object2,action_pos):
        self.cat_num = cat_num
        self.action = action
        self.subject=subject
        self.object1=object1
        self.object2=object2
        self.action_pos=action_pos
    def concatenate(self):
        return self.action+'.'+self.action_pos

def sequence(text):
    f=open("model_actions.txt", "r")
    out= open("ActionSequence.txt","w+")
    withoutSeq={}
    lines=f.readlines()
    Locations=[]
    for line in lines:
        line = line.split()
        action=ModelsAction(line[0],line[1],line[2],line[3],line[4],line[5])
        withoutSeq[action.concatenate()]=action
        Locations.append(int(action.action_pos))

    doc = nlp(text)
    #
    # for token in doc:
    #     print(token.text,token.i)

    Timing=["after","before","then"]

    Seq= {}
    seq_num=0
    Sentences=[]
    j=0

    for sent in doc.sents:
        Sentences.append(sent[0].i)
    k=0
    while k<len(Locations):

        if k+1 >=(len(Locations)):
            break
        found = False
        FA=Locations[k]
        SA=Locations[k+1]
        for i in range (Locations[k],Locations[k+1]):
            fist_action=""
            secAction=""
            if i in Sentences :
                if any(str(doc[i]).lower()== s for s in ["after","before","while","during"]):
                    found=True
                    k+=1
                    FA = Locations[k]
                    SA = Locations[k + 1]
                    if str(doc[i]).lower() == "after":
                        first_action= str(doc[FA].lemma_)+'.'+str(FA)
                        secAction=str(doc[SA].lemma_)+'.'+str(SA)
                        if first_action not in Seq:
                            seq_num += 1
                            Seq[first_action]=seq_num
                        if secAction not in Seq:
                            seq_num=seq_num+1
                            Seq[secAction]=seq_num
                        k += 1
                        break
                    elif (str(doc[i]).lower() =="before"):
                        first_action = str(doc[SA].lemma_)+'.'+str(SA)
                        secAction = str(doc[FA].lemma_)+'.'+str(FA)
                        if first_action not in Seq:
                            seq_num += 1
                            Seq[first_action] = seq_num
                        if secAction not in Seq:
                            seq_num=seq_num+1
                            Seq[secAction] = seq_num
                        k += 1
                        break

            if any(str(doc[i]).lower()== s for s in Timing):
                found=True
                if str(doc[i]).lower() == "after":
                    first_action = str(doc[FA].lemma_) + '.' + str(FA)
                    secAction = str(doc[SA].lemma_) + '.' + str(SA)
                    if first_action  not in Seq:
                        seq_num += 1
                        Seq[first_action] = seq_num
                    if secAction not in Seq:
                        seq_num = seq_num + 1
                        Seq[secAction] = seq_num
                elif str(doc[i]).lower()=="then" or (str(doc[i]).lower()=="before"):
                    first_action = str(doc[FA].lemma_) + '.' + str(FA)
                    secAction = str(doc[SA].lemma_) + '.' + str(SA)
                    if first_action not in Seq:
                        seq_num += 1
                        Seq[first_action] = seq_num
                    if secAction not in Seq:
                        seq_num=seq_num+1
                        Seq[secAction] = seq_num
                k+=1
                break
        if found==False:
            Seq[str(doc[SA].lemma_) + '.' + str(SA)]=seq_num
            Seq[str(doc[FA].lemma_) + '.' + str(FA)]=seq_num
            k+=1

    for key,value in Seq.items():
        out.write(str(Seq[key])+' '+withoutSeq[key].cat_num+' '+withoutSeq[key].subject+' '+withoutSeq[key].action+' '+withoutSeq[key].object1+' '+withoutSeq[key].object2+'\n')

    return

