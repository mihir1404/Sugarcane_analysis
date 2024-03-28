#!/usr/bin/env python
# coding: utf-8

# # Importing libraries
# 

# In[1]:


import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# # Load the dataset
# 

# In[2]:


df = pd.read_csv('List of Countries by Sugarcane Production.csv')


# In[3]:


df.head()


# In[4]:


df.shape


# # Data Cleaning

# In[5]:


df['Production (Tons)']=df['Production (Tons)'].str.replace(".","")
df['Production per Person (Kg)'] = df['Production per Person (Kg)'].str.replace(".","").str.replace(",",".")
df['Acreage (Hectare)'] = df['Acreage (Hectare)'].str.replace(".","")



# In[6]:


df['Yield (Kg / Hectare)'] = df['Yield (Kg / Hectare)'].str.replace(".","").str.replace(",",".")


# In[7]:


df.head()


# In[8]:


df.rename(columns = {"Production (Tons)":"Production_(Tons)"},inplace=True)
df.rename(columns = {"Production per Person (Kg)":"Production_per_Person_(Kg)"},inplace=True)
df.rename(columns = {"Acreage (Hectare)":"Acreage_(Hectare)"},inplace=True)
df.rename(columns = {"Yield (Kg / Hectare)":"Yield_(Kg/Hectare)"},inplace=True)


# In[9]:


df


# In[10]:


df.isnull().sum()


# In[11]:


df[df['Acreage_(Hectare)'].isnull()]


# In[12]:


df = df.dropna().reset_index()


# In[13]:


df.head()


# In[14]:


df.drop(['index','Unnamed: 0'],axis=1,inplace=True)


# In[15]:


df


# In[16]:


df.isnull().sum()


# In[17]:


df.dtypes


# In[19]:


df['Production_(Tons)'] = df['Production_(Tons)'].astype(float)
df['Production_per_Person_(Kg)'] = df['Production_per_Person_(Kg)'].astype(float)
df['Acreage_(Hectare)'] = df['Acreage_(Hectare)'].astype(float)
df['Yield_(Kg/Hectare)'] = df['Yield_(Kg/Hectare)'].astype(float)


# In[20]:


df.dtypes


# In[21]:


df.nunique()


# # Univariate Analysis
# 

# ## How many countries produce sugarcane from each continent?

# In[22]:


df['Continent'].value_counts()


# In[23]:


df['Continent'].value_counts().plot(kind='bar')


# ## Distribution of columns

# In[24]:


plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
sns.distplot(df['Production_(Tons)'])
plt.subplot(2,2,2)
sns.distplot(df['Production_per_Person_(Kg)'])
plt.subplot(2,2,3)
sns.distplot(df['Acreage_(Hectare)'])
plt.subplot(2,2,4)
sns.distplot(df['Yield_(Kg/Hectare)'])


# ## Checking Outliers

# In[25]:


plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
sns.boxplot(df['Production_(Tons)'])
plt.subplot(2,2,2)
sns.boxplot(df['Production_per_Person_(Kg)'])
plt.subplot(2,2,3)
sns.boxplot(df['Acreage_(Hectare)'])
plt.subplot(2,2,4)
sns.boxplot(df['Yield_(Kg/Hectare)'])


# In[26]:


df.describe()


# # Bivariate Analysis

# In[27]:


df_new = df[['Country','Production_(Tons)']].set_index('Country')


# In[29]:


df_new


# In[30]:


df_new['Production(Tons)_percent'] = ((df_new['Production_(Tons)']*100)/df_new['Production_(Tons)'].sum())


# In[31]:


df_new


# In[36]:


plt.figure(figsize=(10,5))
plt.pie(df_new['Production_(Tons)'],labels=df['Country'],autopct="%1.1f%%")
plt.show()


# In[38]:


df_new['Production_(Tons)'].head(10).plot(kind='bar')


# In[41]:


ax = sns.barplot(data=df.head(10),x='Country',y='Production_(Tons)')
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
plt.show()


# # Which country has highest land?

# In[44]:


df_acr = df.sort_values('Acreage_(Hectare)',ascending=False)
ax = sns.barplot(data=df_acr.head(10),x='Country',y='Acreage_(Hectare)')
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
plt.show()


# # Which Country has highest yield per hectare?

# In[47]:


df_hec = df.sort_values('Yield_(Kg/Hectare)',ascending=False)
ax = sns.barplot(data=df_hec.head(10),x='Country',y='Yield_(Kg/Hectare)')
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
plt.show()


# # Which Country has the highest production?

# In[48]:


df_prod = df.sort_values('Production_(Tons)',ascending=False)
ax = sns.barplot(data=df_prod.head(10),x='Country',y='Production_(Tons)')
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
plt.show()


# In[53]:


df.dtypes


# In[56]:


df


# In[57]:


subset_df = df[['Production_(Tons)','Production_per_Person_(Kg)','Acreage_(Hectare)','Yield_(Kg/Hectare)']]


# In[59]:


subset_df.corr()


# # Do Countries with highest land produce more sugarcane?

# In[62]:


sns.scatterplot(data=df,x='Acreage_(Hectare)',y='Production_(Tons)')


# In[61]:


sns.heatmap(subset_df.corr(),annot=True,cmap='Greens')


# # Do Countries which yield more sugarcane per hectare produces more sugarcane in total?

# In[63]:


sns.scatterplot(data=df,x='Yield_(Kg/Hectare)',y='Production_(Tons)')


# # Analysis for continent

# ## Which continent produces maximum sugarcane?

# In[64]:


df_continent = df.groupby("Continent").sum()


# In[65]:


df_continent


# In[70]:


df['Continent'].value_counts()


# ## Which continent produces maximum sugarcane?

# In[69]:


df_continent['Production_(Tons)'].sort_values(ascending=False).plot(kind='bar')


# In[71]:


df_continent['Acreage_(Hectare)'].sort_values(ascending=False).plot(kind='bar')


# ## Do number of continents in a continent effects production of sugarcane?

# In[73]:


df_continent['number_of_countries'] = df.groupby("Continent").count()['Country']


# In[74]:


df_continent


# In[75]:


continent_names =df_continent.index.to_list()
sns.lineplot(data=df_continent,x='number_of_countries',y='Production_(Tons)')
plt.xticks(df_continent['number_of_countries'],continent_names,rotation = 90)
plt.show()


# In[77]:


df_continent['Production_(Tons)'].plot(kind='pie',autopct="%.2f")
plt.legend()

