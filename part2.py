import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
#hi

class Metadata:
     
     def __init__(self, data: pd.DataFrame): 
        self._data = data 
        
     @abstractmethod
     def execute(self): 
        pass

class RowsColumns(Metadata):
 
    def execute(self):
        return self._data.shape  #f"The number of rows of the dataset is {self._data.shape[0]} while the number of columns is {self._data.shape[1]}"            #(number of rows, number of columns)

class ColumnLabel(Metadata):   

    def execute(self):
        # l = []
        # for i in self._data.columns:
            # l += [i] 
        return self._data.columns #f"The labels of the columns are: {l}"
        
class Distinct(Metadata): 

    def execute(self):
        l = self._data.to_numpy()
        column_id = l[:,:1]
        column_symbol = l[:,4]
        unique_id = np.unique(column_id)
        unique_symbol = np.unique(column_symbol)
        
        li = []
        ls = []
        
        for i in unique_id:
            li += [i]
        for e in unique_symbol:
            ls += [e]
       
        #return final_distinct_id, final_distinct_symbol
        return  unique_id, len(unique_id), unique_symbol, len(unique_symbol)
       # l = self._data.to_numpy()
       # column = l[:,:1]
       # final = np.unique(column)
       # lf = []
       # for i in final:
            # lf += [i]
       # final_distinct = (len(final),lf)
       # return final_distinct
  

class Sentence(Metadata):
  
    def execute(self,id_symbol):  
        l = [] 
        
        try:
            int(id_symbol)
            for index_number in range(len(self._data)): #loops over all the indices of the df
                if self._data.iat[index_number, 0] == int(id_symbol):# or self._data.iat[index_number, 0] == int(id_symbol): # .iat gives the element of column 0 , at 'index_number'
                    l.append(self._data.iat[index_number, 1])
        
        except ValueError:
            if id_symbol[:2] in ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']:
                for index_number in range(len(self._data)): #loops over all the indices of the df
                    if self._data.iat[index_number, 0] == id_symbol:# or self._data.iat[index_number, 0] == int(id_symbol): # .iat gives the element of column 0 , at 'index_number'
                        l.append(self._data.iat[index_number, 1])
                   
            else: 
                for index_number in range(len(self._data)): #loops over all the indices of the df
                    if self._data.iat[index_number, 4] == id_symbol: # .iat gives the element of column 0 , at 'index_number'
                        l.append(self._data.iat[index_number, 1] ) #append the element that is found in column 1, at 'index_number'
            
           
        if not l: #empty lists are considered 'False', so if 'l' is empty then:
            return #"No such ID or symbol in the dataframe, try another one."
    
        return l, len(l)#return f"{len(l)} sentences found: {l}"


class MergedDataset(Metadata):
    
    def execute(self): 
        top10 = self._data[['gene_symbol', 'disease_name']].value_counts()[:10].index
        #dataframe_a = pd.DataFrame(a, columns = ['Associations: (Gene,Disease)'])
        return top10, len(top10) #dataframe_a
       
       
class AssociatedDisease(Metadata):
   
   def execute(self, gene):
       
       try: 
           int(gene)
           
           if (int(gene) in self._data['geneid'].unique()):
               l = (self._data).loc[self._data['geneid'] == int(gene)]
               g = l['disease_name'].tolist()
               new_g = set(g)
               new_lg = list(new_g)
               return new_lg, len(new_lg)
           
       except ValueError: 
           
           if (gene in self._data['gene_symbol'].unique()):
               l = (self._data).loc[self._data['gene_symbol'] == gene]
               g = l['disease_name'].tolist()
               new_g = set(g)
               new_lg = list(new_g)
               return new_lg, len(new_lg)
 

class AssociatedGene(Metadata):
    
    def execute(self, disease):
            
         if (disease in self._data['diseaseid'].unique()):
            l = (self._data).loc[self._data['diseaseid'] == disease]
            g = l['gene_symbol'].tolist()
            new_g = set(g)
            new_lg = list(new_g)
            return new_lg, len(new_lg)
            
         if (disease in self._data['disease_name'].unique()):
            l = (self._data).loc[self._data['disease_name'] == disease]
            g = l['gene_symbol'].tolist()
            new_g = set(g)
            new_lg = list(new_g)
            return new_lg, len(new_lg)
