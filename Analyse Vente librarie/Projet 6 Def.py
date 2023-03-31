#!/usr/bin/env python
# coding: utf-8

# ## <FONT COLOR="#FF7D33"> Projet 6 - La Page </FONT>
# 
# <FONT COLOR="#33A2FF"> **Import** </FONT>
# - <a href='#C1'>Import packages et fichiers</a>
# 
# <FONT COLOR="#33A2FF"> **Analyse tables** </FONT>
# - <a href='#C2'> Analyse customers </a>
# - <a href='#C3'> Analyse products </a>
# - <a href='#C4'> Analyse transactions </a>
# 
# <FONT COLOR="#33A2FF"> **Jointures** </FONT>
# - <a href='#C5'> Jointures </a>
# - <a href='#C6'> Nettoyage Dataframe</a>
# 
# <FONT COLOR="#33A2FF"> **Analyses** </FONT>
# - <a href='#C7'> Analyse CA </a>
# - <a href='#C8'>Analyse du CA par categorie</a>
# - <a href='#C9'>Indice Gini</a>
# 
# <FONT COLOR="#33A2FF"> **Tests statistiques** </FONT>
# - <a href='#C10'> Test statistuqes </a>
# 

# # <a name='C1'> <FONT COLOR="#333CFF">  Import packages et fichiers</FONT> </a> 

# In[1]:


import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objs as go
from scipy.stats import spearmanr


# In[2]:


# creation variable parcour des fichiers
path = 'C:/Users/Zacca/OneDrive/Desktop/Projet 6/'


# In[3]:


# import fichiers csv
customers = pd.read_csv(path + 'customers.csv')
products = pd.read_csv(path + 'products.csv')
transactions = pd.read_csv(path + 'transactions.csv')


# # <a name='C2'> <FONT COLOR="#333CFF"> Analyse Customers </FONT> </a>

# In[4]:


# affichage customers
customers.head(3)


# In[5]:


# controles valeurs nulles
customers.isnull().sum()


# In[6]:


# controle type valeurs
customers.dtypes


# In[7]:


# controle doublons
print('il y a', len(customers[customers.duplicated(keep=False)]), 'doublons')


# In[8]:


# controle unicité id_product
products['id_prod'].is_unique


# # <a name='C3'> <FONT COLOR="#333CFF"> Analyse Products </FONT></a>

# In[9]:


# affichage products
products.head(3)


# In[10]:


# controle valeurs nulles
products.isnull().sum()


# In[11]:


# controle type
products.dtypes


# In[12]:


# controle doublons
print('il y a', len(products[products.duplicated(keep=False)]), 'doublons')


# In[13]:


# controle unicité id_product
products['id_prod'].is_unique


# # <a name='C4'><FONT COLOR="#333CFF"> Analyse Transactions </FONT> </a>

# In[14]:


# affichage transactions
transactions.head(3)


# In[15]:


# controle valeurs nulles
transactions.isnull().sum()


# In[16]:


#controle types
transactions.dtypes


# In[17]:


# controle doublons
print('il y a ', len(transactions[transactions.duplicated(keep=False)]), 'doublons')


# In[18]:


# affichage doublons
transactions[transactions.duplicated(keep=False)].head(3)


# In[19]:


# affichage valeurs test table products
products[products['id_prod'] == 'T_0']


# In[20]:


# creation variable test
test = transactions[transactions['date'].str.contains('test')]


# In[21]:


# suppression des valeurs test
transactions = transactions.drop(test.index)


# In[22]:


# controle dboulons
print('il y a ', len(transactions[transactions.duplicated(keep=False)]), 'doublons')


# In[23]:


# conversion type colonne date en datetime
transactions['date'] = pd.to_datetime(transactions['date'])


# # <a name='C5'><FONT COLOR="#333CFF"> Jointures </FONT></a>

# In[24]:


# merge des transactions et products
trans_prod = pd.merge(transactions, products, on='id_prod', how='left', indicator = True)


# In[25]:


# controle des jointures
print('numero des valeurs differentes de both dans la colonne _merge :', len(trans_prod[trans_prod['_merge'] != 'both']))


# In[26]:


# affichage des valeurs
trans_prod[trans_prod['_merge'] != 'both'].head(3)


# In[27]:


# controle numero des valeurs de la categorie id_prod
print('il y a ', len(trans_prod[trans_prod['id_prod'] == '0_2245']), 'produit dans la categerie 0_2245')


# Ces valeurs n'ont pas une prix ni une categorie, mais on peut extraire la categorie de leurs id_prod : 0_2245.
# 1. Creation d'une moyenne par catégorie 
# 2. Ajout de la catégorie dans la colonne Categ
# 3. ajout des valeurs dans la colonne price

# In[28]:


# creation moyenne par catégorie 
means = trans_prod.groupby(['categ'])['price'].mean()


# In[29]:


# affichage valeurs moyenne
means


# In[30]:


# changement valeurs NaN dans la colonne categ
trans_prod['categ'] = trans_prod['categ'].fillna(1)


# In[31]:


# changement des valeurs NaN dans la colonne price
trans_prod['price'].replace(np.nan, 10.638188, inplace=True)


# In[32]:


# controle des valeurs
trans_prod[trans_prod['id_prod'] == '0_2245'].head(3)


# In[33]:


# drop colonne _merge
trans_prod.drop('_merge', axis ='columns', inplace = True)


# In[34]:


# jointure entre trans_prod et customers
df = pd.merge(trans_prod, customers, on='client_id', how='left', indicator=True)


# In[35]:


# controle des jointures
print('numero des valeurs differentes de "both" dans la colonne "_merge" : ', len(df[df['_merge'] != 'both']))


# In[36]:


# drop colonne "_merge"
df.drop('_merge', axis='columns', inplace = True)


# # <a name='C6'><FONT COLOR="#333CFF"> Nettoyage DF </FONT></a>

# In[37]:


# creation colonne An-Mo avec format Année - mois pour manipulation successives
df['An-Mo'] = df['date'].dt.strftime('%Y-%m')


# In[38]:


# creation colonne pour l'âge 
df['age'] = 2023 - df['birth']


# In[39]:


# conversion format date pour la rendre plus lisible
df['date'] = df['date'].dt.strftime('%Y-%m-%d')


# In[40]:


df.head(1)


# In[41]:


# aggregation des valeurs par client
df_cl = df.pivot_table(index='client_id', values ='price', aggfunc='sum')


# In[42]:


# visualisation dans une graphique
fig = px.scatter(df_cl, x=df_cl.index, y="price")
fig.show()


# Présence des quatres outliers importantes.
# On vas les afficher pour en tirer des conclusion sur leur nature.

# In[43]:


# creation variable pour visualiser les clients plus importantes
df_sort = df_cl.sort_values(by=['price'], ascending = False)


# In[44]:


# affichage dataframe sorted
df_sort.head(5)


# Les montants sont importantes, on peut en déduire qu'ils sont des clients importantes, voire des autres business.
# On procede avec la création d'une Dataframe specifique pour eux, pour avoir juste les données B2C.

# In[45]:


# creation variable professional
df_pro = df_sort.head(4).reset_index()


# In[46]:


# suppression vcaleurs pro du df
df = df[df != 'c_1609']
df = df[df != 'c_4958']
df = df[df != 'c_6714']
df = df[df != 'c_3454']


# # <a name='C7'><FONT COLOR="#333CFF"> Analyse du CA </FONT></a>

# In[47]:


# Determination du CA total
chiffre_affaire = np.sum(df['price'])


# In[48]:


# affichage CA
print('Le Ca total est de : ', round(chiffre_affaire,2), 'Euros')


# In[49]:


# creation variable pour créer graphique
df_group = df.groupby(by ='An-Mo').sum()


# In[50]:


# creation colonne moyenne mobile de 12 mois
df_group['moving_avg'] = df_group['price'].ewm(span=12).mean()


# In[51]:


# variable a représenter dans le graphique
vars = ['price', 'moving_avg']


# ## <FONT COLOR="#333CFF"> Moyenne mobile </FONT>

# In[52]:


# creation graphique
fig = px.line(df_group, x=df_group.index, y=vars, labels={'An-Mo' : 'Mois', 'value' :'CA'},title='Analyse du CA')
fig.show()


# ## <FONT COLOR="#333CFF"> Mois octobre </FONT>

# In[53]:


# creation variable pour le mois octobre
df_oct = df[df['An-Mo'] == '2021-10']


# In[54]:


# creation variable pour faire mettre les données en ordre croissante
df_sort_oct = df_oct.sort_values(by = 'date')


# In[55]:


# creation graphique pour visualiser le mois d'octobre
plt.figure(figsize=(20,10))
plt.xticks(rotation=45)
plt.ylabel('Chiffre Affaire')
sns.histplot(data = df_sort_oct, x='date', hue='categ', multiple="stack", palette=('dark') )


# Les valeurs de la catégorie 1.0, entre le 01/10 et le 27/10, n'ont pas été enregistré

# In[56]:


# suppression mois octobre du df
df = df.drop(df_oct.index)


# ## <FONT COLOR="#333CFF"> Moyenne mobile 2.0 </FONT>

# In[57]:


# creation df pour creatio graphique
df_group = df.groupby(by='An-Mo').sum()


# In[58]:


# creation colonne moyenne mobile de 12 mois
df_group['moving_avg'] = df_group['price'].ewm(span=12).mean()


# In[59]:


# creation graphique sans mois d'octobre
fig = px.line(df_group, x=df_group.index, y=vars, labels={'An-Mo' : 'Mois', 'value':'CA'}, title='Analyse du CA')
fig.show()


# # <a name='C8'><FONT COLOR="#333CFF"> Analyse du CA par categorie </FONT> </a>

# In[60]:


# creation variable pour créer graphique 
df_sort1 = df.sort_values(by='An-Mo')


# In[61]:


fig = px.histogram(df_sort1, x='An-Mo', color ='categ', labels={'An-Mo' : 'Mois', 'count' : 'CA'}, title='Chiffre affaire par catégorie ')
fig.show()


# ## <FONT COLOR="#333CFF"> Repartition CA entre Categories </FONT>

# In[62]:


# creation variable pour créer graphique
df_categ = df.groupby(by='categ').sum()


# In[63]:


# création graphique
fig = px.pie(df_categ, values='price', names=df_categ.index)
fig.show()


# ## <FONT COLOR="#333CFF"> Distribution des prix par catégorie </FONT>

# In[64]:


# creation graphique pour représenter la distribution des prix par categorie
plt.figure(figsize=(20,10))
sns.boxplot(data=df, y='categ', x='price', orient='h', showfliers=False)
plt.title('Distribution des prix par catégorie')
plt.xlabel("Prix")
plt.ylabel("Categ")
plt.show()


# # <a name='C9'> <FONT COLOR="#333CFF"> Inégalités entre clients - Indice Gini</FONT> </a>

# In[65]:


# creation courbe lorenz
df_arr = np.sort(df['price'])
arr = np.array(df_arr)

def gini(arr):
    count = arr.size
    coefficient = 2 / count
    indexes = np.arange(1, count + 1)
    weighted_sum = (indexes * arr).sum()
    total = arr.sum()
    constant = (count + 1) / count
    return coefficient * weighted_sum / total - constant

def lorenz(arr):
    # this divides the prefix sum by the total sum
    # this ensures all the values are between 0 and 1.0
    scaled_prefix_sum = arr.cumsum() / arr.sum()
    # this prepends the 0 value (because 0% of all people have 0% of all wealth)
    return np.insert(scaled_prefix_sum, 0, 0)

# show the gini index!
print("l'indice de gini est : ", gini(arr))

lorenz_curve = lorenz(arr)

# we need the X values to be between 0.0 to 1.0
plt.plot(np.linspace(0.0, 1.0, lorenz_curve.size), lorenz_curve)
# plot the straight line perfect equality curve
plt.plot([0,1], [0,1])
plt.show()


# L'indice de GIni montre une inegalite entre clients qui n'est pas trop fort.

# # <a name='C10'> <FONT COLOR="#333CFF"> Test statistiques</FONT> </a>

# ## <FONT COLOR="#333CFF"> Genre et Categorie </FONT>

# Tout d'abord on peut determiner que le Genre est les Catégories sont des données de type Qualitative.

# Analyse de la distribution des age par genre

# In[66]:


# affichage pyramide des ages par genre
fig, axes = plt.subplots(1, 2)
fig.suptitle('Pyramide ages par genre')

sns.histplot(ax=axes[0], y=df[df['sex']=='m']['age'], bins=12)
axes[0].invert_xaxis()
axes[0].set_title('M')
axes[0].set_xlabel('Numero Personnes')
sns.histplot(ax=axes[1], y=df[df['sex']=='f']['age'], bins=12)
axes[1].set_yticklabels([])
axes[1].set_ylabel('')
axes[1].set_title('F')
axes[1].set_xlabel('Numero Personnes')

plt.subplots_adjust(wspace=0, hspace=0)
plt.show()


# Pas des différences importantes

# In[68]:


# Affichage histogramme genre vs categ
fig = px.histogram(df, x='sex', color ='categ', labels={'sex':'Genre', 'categ':'Catégorie'})
fig.show()


# In[69]:


# creation table de contingece 
df_cont = pd.crosstab(index=df['sex'],columns=df['categ'], margins=True)


# In[70]:


# affichage table de contingence
df_cont


# In[71]:


# creation heatmap
tx = df_cont.loc[:,["All"]]
ty = df_cont.loc[["All"],:]
n = len(df)
indep = tx.dot(ty) / n

c = df_cont.fillna(0) # On remplace les valeurs nulles par 0
measure = (c-indep)**2/indep
xi_n = measure.sum().sum()
table = measure/xi_n
sns.heatmap(table.iloc[:-1,:-1],annot=c.iloc[:-1,:-1],fmt="d")
plt.show()


# ### <FONT COLOR="#333CFF"> Test Khi-2 : Genre Vs Categ </FONT>

# In[72]:


# test de Chi 2
table = pd.crosstab(df['categ'], df['sex'], margins=False)
stat, p, dof, expected = stats.chi2_contingency(table)
print('Test Chi 2')
print('Stat = %.3f\np-value = %.35f' % (stat, p))
if p > .05:
    print('H0: Les deux variables sont independants')
else:
    print( 'H1: Il existe une dependance entre les variables.')


# ## <FONT COLOR="#333CFF"> Âge et montant des achats </FONT>

# In[73]:


# creation pivot table
ca_age = df.pivot_table(index=['age'], values=['price'], aggfunc=['sum'])
ca_age = ca_age.reset_index()
ca_age.columns = ca_age.columns.droplevel(1)


# In[74]:


# affichage pivot table
ca_age.head(3)


# In[75]:


# creation scatter plot
fig = px.scatter(ca_age, x='age', y='sum', labels={"age": "Âge", "sum": "Montant des achats"}, title="Montants des achats par âge ")

fig.show()


# In[76]:


# creation graphique
fig = px.bar(ca_age, x='age', y='sum', template="plotly_white",width=600, height=400, text ='sum', 
             labels={"age": "Âge", "sum": "Montant des achats"}, title="Montants des achats par âge ")
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0),title={'text' : "<b>Montant des achats par âge <b>",'x':0.5,'xanchor': 'center'})
fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
fig.show()


# ### <FONT COLOR="#333CFF"> Test Spearman : Age Vs Montant achats </FONT>

# In[77]:


# spearman test
data1 = ca_age['sum']
data2 = ca_age['age']
coef, p = spearmanr(data1, data2)
print('Spearmans correlation coefficient: %.3f' % coef)
# interpret the significance
alpha = 0.05
if p > alpha:
 print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
else:
 print('Samples are correlated (reject H0) p=%.3f' % p)


# ## <FONT COLOR="#333CFF"> Âge et Catégories </FONT>

# In[78]:


# creation table de contingece 
df_cont_a = pd.crosstab(index=df['age'],columns=df['categ'], margins=True)


# In[79]:


# affichage table
df_cont_a.head(2)


# In[80]:


# creation graphique pour représenter la distribution des prix par categorie sans outliers
plt.figure(figsize=(20,10))
sns.boxplot(data=df, y='categ', x='age', orient='h', showfliers=False)
plt.title('Distribution age par categorie')
plt.xlabel("age")
plt.ylabel("Categ")
plt.show()


# ### <FONT COLOR="#333CFF"> Test Anova : Age Vs Catégorie </FONT>

# In[81]:


# Methode Anova age vs categ

def eta_squared(x,y):
    moyenne_y = y.mean()
    classes = []
    for classe in x.unique():
            
        yi_classe = y[x==classe]
        classes.append({'ni': len(yi_classe),
                        'moyenne_classe': yi_classe.mean()})
    SCT = sum([(yj-moyenne_y)**2 for yj in y])
    SCE = sum([c['ni']*(c['moyenne_classe']-moyenne_y)**2 for c in classes])
    return SCE/SCT
    
print('Valeur de correlation est de :',eta_squared(df['categ'],df['age']), 'Valeur proche de  0, donc il y à une correlation entre categ et age.' )


# ## <FONT COLOR="#333CFF"> Age et Panier moyen </FONT>

# In[82]:


# Creation pivot table
df_ca_mean = df.pivot_table(index=["age"], values=["price"], aggfunc=['count'])
df_ca_mean = df_ca_mean.reset_index()
df_ca_mean.columns = df_ca_mean.columns.droplevel(1)


# In[83]:


# affichage table
df_ca_mean.head(2)


# In[84]:


# creation scatter plot
fig = px.scatter(df_ca_mean, x='age', y='count',
 labels={"age": "Âge", "count": "Taille panier moyen"}, title="Taille panier moyen par âge")
fig.show()


# In[85]:


# creation graphique
fig = px.bar(df_ca_mean, x='age', y='count', template="plotly_white",width=600, height=400)
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0),title={'text' : "<b> Taille panier moyen par âge <b>",'x':0.5,'xanchor': 'center'})
fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
fig.show()


# ### <FONT COLOR="#333CFF"> Test Spearman : Âge Vs Taille Panier Moyen </FONT>

# In[86]:


# spearman test
data1 = df_ca_mean['count']
data2 = df_ca_mean['age']
coef, p = spearmanr(data1, data2)
print('Spearmans correlation coefficient: %.3f' % coef)
# interpret the significance
alpha = 0.05
if p > alpha:
 print('Il n y a pas de correlation (pas de rejete H0) p=%.3f' % p)
else:
 print('Il y a une correlation (rejet H0) p=%.3f' % p)


# ## <FONT COLOR="#333CFF"> Fréquence achats et Age </FONT>

# In[87]:


df_ca_mean_1 = df.pivot_table(index=["client_id",'age'], values=["date"], aggfunc=['count'])
df_ca_mean_1 = df_ca_mean_1.reset_index()
df_ca_mean_1.columns = df_ca_mean_1.columns.droplevel(1)


# In[88]:


df_ca_mean_1.head(3)


# In[89]:


plt.figure(figsize=(16,4))
sns.boxplot(
    data=df_ca_mean_1 ,
    y='count', x='age', showfliers=False)
plt.xticks(rotation=90)
plt.title('Distribution des fréquences achat, par âge')
plt.show()


# In[90]:


# creation scatter plot
fig = px.scatter(x=df_ca_mean_1['age'], y=df_ca_mean_1['count'])
fig.show()


# ### <FONT COLOR="#333CFF"> Test Spearman : Age Vs Fréquence Achats </FONT>

# In[91]:


# spearman test
data1 = df_ca_mean_1['count']
data2 = df_ca_mean_1['age']
coef, p = spearmanr(data1, data2)
print('Spearmans correlation coefficient: %.3f' % coef)
# interpret the significance
alpha = 0.05
if p > alpha:
 print('Il n y a pas de correlation (pas de rejete H0) p=%.3f' % p)
else:
 print('Il y a une correlation (rejet H0)  p=%.3f' % p)

