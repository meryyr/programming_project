import part2
import pandas as pd


class Registry:

    def __init__(self):
        self.name_operations = ['RowsColumnsGene','RowsColumnsDisease','ColumnLabelGene','ColumnLabelDisease','DistinctGene','DistinctDisease','MostFrequentAssociations']
        self.name_operations_input = ['SentenceDisease','SentenceGene','AssociatedDiseases','AssociatedGenes']
      
        self.__dfdisease = pd.read_csv("disease_evidences.tsv", delimiter="\t")
        self.__dfgene = pd.read_csv("gene_evidences.tsv", delimiter="\t")
        
        self.__merged_dataset = pd.merge(self.__dfdisease,self.__dfgene, on = ('pmid','sentence', 'nsentence'), how = "inner")  
    
    def RowsColumns(self):
        operation = part2.RowsColumns
        r = {self.name_operations[0]: operation(self.__dfgene).execute(),
             self.name_operations[1]: operation(self.__dfdisease).execute()}
        return r 
    
    def ColumnLabel(self):
        operation = part2.ColumnLabel
        r = {self.name_operations[2]: operation(self.__dfgene).execute(),
             self.name_operations[3]: operation(self.__dfdisease).execute()}
        return r
            
    def Distinct(self):
        operation = part2.Distinct
        r = {self.name_operations[4]: operation(self.__dfgene).execute(),
             self.name_operations[5]: operation(self.__dfdisease).execute()}
        return r
    
    def Merge(self):
        operation = part2.MostFrequentAssociations
        r = {self.name_operations[6]:operation(self.__merged_dataset).execute()}
        return r
        
    def Sentences(self,value):
        operation = part2.Sentence
        r = {self.name_operations_input[0]: operation(self.__dfdisease).execute(value) , self.name_operations_input[1]: operation(self.__dfgene).execute(value)}
        return r 
  
    def Associations(self,value):
        operation_disease = part2.AssociatedDisease
        operation_gene = part2.AssociatedGene
        r = {self.name_operations_input[2]: operation_disease(self.__merged_dataset).execute(value),self.name_operations_input[3]: operation_gene(self.__merged_dataset).execute(value)} 
        return r


