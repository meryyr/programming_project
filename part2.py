import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class Data(ABC): #abstract superclass to give data to any of its subclasses
     
     def __init__(self, data: pd.DataFrame): 
        self._data = data 
        
     @abstractmethod
     def execute(self): 
        pass

class RowsColumns(Data): #subclass to find dimensions, uses either gene_evidences or disease_evidences
 
    def execute(self):
        return self._data.shape
        
class ColumnLabel(Data): #subclass to find column labels, uses either gene_evidences or disease_evidences

    def execute(self):
        return self._data.columns 
        
class Distinct(Data): #subclass to find distinct elements, uses either gene_evidences or disease_evidences

    def execute(self):
        l = self._data.to_numpy() #pandas to numpy
        column_id = l[:,:1] #take 2nd column
        column_symbol = l[:,4] #take 5th column
        unique_id = np.unique(column_id)
        unique_symbol = np.unique(column_symbol)       
        return  unique_id, len(unique_id), unique_symbol, len(unique_symbol)

class Sentence(Data): #subclass to find associated sentences, uses either gene_evidences or disease_evidences
  
    def execute(self,id_symbol):  
        l = [] 
        
        try:
            int(id_symbol) #try to make an int of the input, to see if input is a geneid
            for index_number in range(len(self._data)): #loop over index numbers of the dataframe
                if self._data.iat[index_number, 0] == int(id_symbol): #check 1st column of the dataframe
                    l.append(self._data.iat[index_number, 1])
        
        except ValueError: #if the input is a string:
            if id_symbol[:2] in ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']: #check if input is a disease_id
                for index_number in range(len(self._data)):
                    if self._data.iat[index_number, 0] == id_symbol: 
                        l.append(self._data.iat[index_number, 1])
                   
            else: 
                for index_number in range(len(self._data)):
                    if self._data.iat[index_number, 4] == id_symbol: #check 5th column of the dataframe
                        l.append(self._data.iat[index_number, 1] )
            
           
        if not l: 
            return #return if nothing is found
    
        return l, len(l) 


class MostFrequentAssociations(Data): #subclass to find 10-top most associated genes/diseases, uses the merged dataset 
    
    def execute(self): 
        top10 = self._data[['gene_symbol', 'disease_name']].value_counts()[:10].index #pandas value_counts function to find highest frequency 
        return top10, len(top10)
       
       
class AssociatedDisease(Data): #subclass to find associated genes to a given disease, uses the merged dataset
   
   def execute(self, gene):
       
       try: 
           int(gene) #try to make int of input
           
           if int(gene) in self._data['geneid'].unique(): #check if input is in the geneid column
               l = (self._data).loc[self._data['geneid'] == int(gene)] #make dataframe only with rows containing elements equal to input
               g = l['disease_name'].tolist() #make list of disease_name column
               new_g = set(g)
               return new_g, len(new_g)
           
       except ValueError: 
           
           if gene in self._data['gene_symbol'].unique():
               l = (self._data).loc[self._data['gene_symbol'] == gene]
               g = l['disease_name'].tolist()
               new_g = set(g)
               return new_g, len(new_g)
 

class AssociatedGene(Data): #subclass to find associated genes to a given disease, uses the merged dataset
    
    def execute(self, disease):
            
         if disease in self._data['diseaseid'].unique(): #check if input is in the diseaseid column
            l = (self._data).loc[self._data['diseaseid'] == disease] #make dataframe only with rows containing elements equal to input
            g = l['gene_symbol'].tolist() #make list of gene_symbol column
            new_g = set(g)
            return new_g, len(new_g)
            
         if disease in self._data['disease_name'].unique(): #check if input is in the diseas_name column
            l = (self._data).loc[self._data['disease_name'] == disease]
            g = l['gene_symbol'].tolist()
            new_g = set(g)
            return new_g, len(new_g)
