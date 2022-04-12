import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class Data(ABC):                                    #abstract superclass to provide the correct DataFrame to any of its subclasses
     
     def __init__(self, data: pd.DataFrame): 
        self._data = data 
        
     @abstractmethod
     def execute(self): 
        pass

class RowsColumns(Data):                            #subclass which returns dimensions of the DataFrame
 
    def execute(self):
        return self._data.shape
        
class ColumnLabel(Data):                            #subclass which returns column labels

    def execute(self):
        return self._data.columns 
        
class Distinct(Data):                               #subclass which returns distinct elements of the DataFrame

    def execute(self):
        l = self._data.to_numpy()           #pandas to numpy
        column_id = l[:,0]                  #take 1st column
        column_symbol = l[:,4]              #take 4th column
        unique_id = np.unique(column_id)
        unique_symbol = np.unique(column_symbol)       
        return  unique_id, len(unique_id), unique_symbol, len(unique_symbol)

class Sentence(Data):                               #subclass which returns associated sentences
  
    def execute(self,id_symbol):  
        l = [] 
        
        try:
            int(id_symbol) 
            for index_number in range(len(self._data)):               
                if self._data.iat[index_number, 0] == int(id_symbol): 
                    l.append(self._data.iat[index_number, 1])
        
        except ValueError: #if the input is a string:
            if id_symbol[:2] in ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']:     #check if input is a disease_id
                for index_number in range(len(self._data)):
                    if self._data.iat[index_number, 0] == id_symbol: 
                        l.append(self._data.iat[index_number, 1])
                   
            else: 
                for index_number in range(len(self._data)):
                    if self._data.iat[index_number, 4] == id_symbol:
                        l.append(self._data.iat[index_number, 1] )
                
        if not l: 
            return                                         
    
        return l, len(l) 


class MostFrequentAssociations(Data):                                   #subclass which returns 10-top most associated genes and diseases 
    
    def execute(self): 
        top10 = self._data[['gene_symbol', 'disease_name']].value_counts()[:10].index 
        return top10, len(top10)
       
       
class AssociatedDisease(Data):                                          #subclass which returns associated diseases to a given gene
   
   def execute(self, gene):
       
       try: 
           int(gene) 
           
           if int(gene) in self._data['geneid'].unique(): 
               l = (self._data).loc[self._data['geneid'] == int(gene)]  
               g = l['disease_name'].tolist() 
               new_g = set(g)
               return new_g, len(new_g)
           
       except ValueError: 
           
           if gene in self._data['gene_symbol'].unique():
               l = (self._data).loc[self._data['gene_symbol'] == gene]
               g = l['disease_name'].tolist()
               new_g = set(g)
               return new_g, len(new_g)
 

class AssociatedGene(Data):                                          #subclass which returns associated genes to a given disease
    
    def execute(self, disease):
            
         if disease in self._data['diseaseid'].unique():
            l = (self._data).loc[self._data['diseaseid'] == disease] 
            g = l['gene_symbol'].tolist() 
            new_g = set(g)
            return new_g, len(new_g)
            
         if disease in self._data['disease_name'].unique(): 
            l = (self._data).loc[self._data['disease_name'] == disease]
            g = l['gene_symbol'].tolist()
            new_g = set(g)
            return new_g, len(new_g)
