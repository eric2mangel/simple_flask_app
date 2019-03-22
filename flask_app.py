from flask import Flask,render_template
import sklearn
import pickle
import os
import pandas as pd
import json

CHEMIN_PICKLE = os.getcwd()+"/bdd/"

d2 = pickle.load(open(CHEMIN_PICKLE+'DATA', 'rb'))
TDFIDF2 = pickle.load(open(CHEMIN_PICKLE+'TDFIDF_MAT', 'rb'))
KNN12 = pickle.load(open(CHEMIN_PICKLE+'KNN12', 'rb'))
AS = pickle.load(open(CHEMIN_PICKLE+'Annee_Score', 'rb'))


def GCN(row):
    dico={}
    datatest=d2.copy()
    #datatest['movie_title']=datatest.index
    #print(datatest.shape)
    datatest.reset_index(inplace=True)
    #print(datatest.head())
    distances, indices = KNN12.kneighbors(TDFIDF2.getrow(row))
    #print(indices)
    names_similar = pd.Series(indices.flatten()).map(datatest.reset_index()['movie_title'])
    #print(names_similar)
    result = pd.DataFrame({'distance':distances.flatten(), 'movie_title':names_similar})
    result=result.set_index('movie_title')
    result = pd.concat([result, AS], axis=1,join='inner')
    result.iloc[:,1]=result.iloc[:,1]-result.iloc[0,1]
    result.iloc[:,2]=result.iloc[:,2]-result.iloc[0,2]
    result['Distance_finale']=result['distance']*10+result['title_year'].abs()+result['imdb_score']*(-1.5)
    result['ID']=indices.flatten()
    result = result.sort_values(by='Distance_finale', ascending=1)
    #result=result.reset_index()
    #print(result)
    fin=result.copy()
    fin.reset_index(inplace=True)
    fin = fin[['ID','movie_title']]
    dico=json.dumps(fin.iloc[1:6].to_dict('records'))
    return dico
    #lili=result.index.tolist()
    ##Constitution du dico en rajoutant les id
    ##print(lili)
    #return lili[0:6]
    #return 'OK'
  
#On crée une appli vide
app=Flask(__name__)


@app.route('/')
def home():
    #return os.getcwd()
    return str('Connecté')


@app.route('/recommand/<int:id>')
def posts_show(id):
    proches=GCN(id)
    return proches
    #Retour="Les films les plus proches de " + proches[0] + " sont"+'\n'+str(proches[1:6])
    #return Retour
    #return str(GCN(id))


if __name__=='__main__': #=Si on exécute notre fichier directement alors on lance app
    app.run(debug=True,port=5000)

#Retour attentdu
#{
#    "_results": [
#        { "id": "645657", "name": "Eternal sunshine of the spotless mind" },
#        { "id": "543556", "name": "500 Days of Summer" },
#        { "id": "873453", "name": "Lost in Translation" }
#    ]
#}

