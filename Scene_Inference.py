import pandas as pd


def support_inference (explicit_objects):
    df = pd.read_csv("supportParentGivenChild.csv", sep=",")
    print(df.head())

    total_objects_inScene = explicit_objects.copy()

    for curr_object in explicit_objects:
        print(curr_object)
        df_suggested_supports = df[df["child"]==curr_object]
        print(df_suggested_supports)
        max_prob=df_suggested_supports["p(parent|child)"].max()
        infere_support = df_suggested_supports[ df_suggested_supports["p(parent|child)"] == max_prob]
        infered_object=infere_support["parent"].values[0]
        print(infered_object)
        if( (infered_object in explicit_objects) or (infered_object == 'ROOT')):
            continue
        else:
            total_objects_inScene.add(infered_object)

    return total_objects_inScene