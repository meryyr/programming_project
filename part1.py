import part2
from abc import ABC, abstractmethod
import pandas as pd
from typing import Set


class ImportDisease:

    def __init__(self, requested_operation, operations=(part2.RowsColumns, part2.ColumnLabel, part2.Distinct, part2.Sentence), datadisease="disease_evidences.tsv"):
        self.dfdisease = pd.read_csv(datadisease, delimiter="\t")
        self.operations = operations
        self.requested_operation = str(requested_operation)

    def operation(self):
        for op in self.operations:
            if str(op) == self.requested_operation:
                operation = op(self.dfdisease)
                result = operation.execute()
                return result
    
    def input_operation(self,value):
        result = part2.Sentence(self.dfdisease).execute(value) 
        return result  

class ImportGene:

    def __init__(self, requested_operation, operations=(part2.RowsColumns, part2.ColumnLabel, part2.Distinct, part2.Sentence), datagene="gene_evidences.tsv"):
        self.dfgene = pd.read_csv(datagene, delimiter="\t")
        self.operations = operations
        self.requested_operation = str(requested_operation)

    def operation(self):
        for op in self.operations:
            if str(op) == self.requested_operation:
                operation = op(self.dfgene)
                result = operation.execute() 
                return result

    def input_operation(self,value):
        result = part2.Sentence(self.dfgene).execute(value) 
        return result   
        
 

class MergeDataset(ImportDisease,ImportGene):
    
    def __init__(self, dfdisease, dfgene, requested_operation, operations=(part2.Merge,part2.AssociatedDisease,part2.AssociatedGene)):
        ImportDisease.__init__(self, dfdisease)
        ImportGene.__init__(self, dfgene)
        self.merged_dataset = pd.merge(self.dfdisease,self.dfgene,  on = ('pmid','sentence', 'nsentence'), how = "inner")
        #self.merged_dataset_input = pd.merge(self.dfdisease,self.dfgene,  on = ('pmid'), how = "inner")
        self.requested_operation = str(requested_operation)
        self.operations = operations
        
    def operation(self):
        result = part2.Merge(self.merged_dataset).execute()
        return result
                
    def input_gene(self,gene):
        result = part2.AssociatedDisease(self.merged_dataset).execute(gene) 
        return result

    def input_disease(self,disease):
        result = part2.AssociatedGene(self.merged_dataset).execute(disease) 
        return result

class Registry:
  
    # def name_operations(self):
        # n_o = ['Rows and columns of Gene dataset','Rows and columns of Disease dataset','Columns'labels of Gene dataset,'Columns'labels of Disease dataset','Distinct genes','Distinct diseases','Sentences associated to a given gene','Sentences associated to a given disease','10 top most associations', '']
        # return n_o
        
    def name_operations(self):
        n_o = ['RowsColumnsGene','RowsColumnsDisease','ColumnLabelGene','ColumnLabelDisease','DistinctGene','DistinctDisease','Merge']
        return n_o
    
    def name_operations_input(self):
        n = ['SentenceDisease','SentenceGene','AssociatedDisease','AssociatedGenes']
        return n
    
    # def execute_operation(self):
        # l = ['RowsColumns']
        # return l

    def RowsColumns(self):
        r = {'RowsColumnsGene': ImportGene(part2.RowsColumns).operation(),
             'RowsColumnsDisease': ImportDisease(part2.RowsColumns).operation()}
        return r 
    
    def ColumnLabel(self):
        r = {'ColumnLabelGene': ImportGene(part2.ColumnLabel).operation(),
             'ColumnLabelDisease': ImportDisease(part2.ColumnLabel).operation()}
        return r
            
    def Distinct(self):
        r = {'DistinctGene': ImportGene(part2.Distinct).operation(),
             'DistinctDisease': ImportDisease(part2.Distinct).operation()}
        return r
    
    def Sentences(self,value):
        r = {'SentenceGene': ImportGene(part2.Sentence).input_operation(value),
             'SentenceDisease': ImportDisease(part2.Sentence).input_operation(value)}
        return r
        
    def Merge(self):
        r = {'Merge': MergeDataset("disease_evidences.tsv","gene_evidences.tsv",part2.Merge).operation()}
        return r 
        
    def Associations(self,value):
      r = {'AssociatedDiseases': MergeDataset("disease_evidences.tsv","gene_evidences.tsv",part2.AssociatedDisease).input_gene(value), 'AssociatedGenes': MergeDataset("disease_evidences.tsv","gene_evidences.tsv",part2.AssociatedGene).input_disease(value)}
      return r


  
#z = ImportGene.input_operation('part2.Sentence')
#d = {'RowsColumnsGene','RowsColumnsDisease','ColumnLabelGene','ColumnLabelDisease','DistinctGene','DistinctDisease','SentenceGene','SentenceDisease','Merge'}
#dg = pd.read_csv("gene_evidences.tsv", delimiter="\t")     
# z = (part2.Sentence(dg)).execute_input()
# print(z)
#display = Registry().Sentences(1)
#print(display)


# display = Registry().Sentences('part2.Sentence',1)
# print(display)

#print(MergeDataset("disease_evidences.tsv","gene_evidences.tsv").merge())

dd = pd.read_csv("disease_evidences.tsv", delimiter="\t")
dg = pd.read_csv("gene_evidences.tsv", delimiter="\t")

# merged_dataset = pd.merge(dfdisease,dfgene, on = ('pmid','sentence', 'nsentence'))

    
print(part2.AssociatedGene(pd.merge(dd,dg,  on = ('pmid','sentence', 'nsentence'), how = "inner")).execute('C5139167'))

