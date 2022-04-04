import part2
import pandas as pd

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
    
    def __init__(self, dfdisease, dfgene, requested_operation, operations=(part2.MergedDataset,part2.AssociatedDisease,part2.AssociatedGene)):
        ImportDisease.__init__(self, dfdisease)
        ImportGene.__init__(self, dfgene)
        self.merged_dataset = pd.merge(self.dfdisease,self.dfgene,  on = ('pmid','sentence', 'nsentence'), how = "inner")
        #self.merged_dataset_input = pd.merge(self.dfdisease,self.dfgene,  on = ('pmid'), how = "inner")
        self.requested_operation = str(requested_operation)
        self.operations = operations
        
    def operation(self):
        result = part2.MergedDataset(self.merged_dataset).execute()
        return result
                
    def input_gene(self,gene):
        result = part2.AssociatedDisease(self.merged_dataset).execute(gene) 
        return result

    def input_disease(self,disease):
        result = part2.AssociatedGene(self.merged_dataset).execute(disease) 
        return result

class Registry:


    def __init__(self,name_operations = ['RowsColumnsGene','RowsColumnsDisease','ColumnLabelGene','ColumnLabelDisease','DistinctGene','DistinctDisease','MergedDataset'],name_operations_input = ['SentenceDisease','SentenceGene','AssociatedDisease','AssociatedGenes']):
        self.name_operations = name_operations
        self.name_operations_input = name_operations_input
    
    def RowsColumns(self):
        r = {self.name_operations[0]: ImportGene(part2.RowsColumns).operation(),
             self.name_operations[1]: ImportDisease(part2.RowsColumns).operation()}
        return r 
    
    def ColumnLabel(self):

        r = {self.name_operations[2]: ImportGene(part2.ColumnLabel).operation(),
             self.name_operations[3]: ImportDisease(part2.ColumnLabel).operation()}
        return r
            
    def Distinct(self):
    
        r = {self.name_operations[4]: ImportGene(part2.Distinct).operation(),
             self.name_operations[5]: ImportDisease(part2.Distinct).operation()}
        return r
    
    def Merge(self):
        r = {self.name_operations[6]: MergeDataset("disease_evidences.tsv","gene_evidences.tsv",part2.MergedDataset).operation()}
        return r
        
    def Sentences(self,value):
        r = {name_operations_input[0]: ImportDisease(part2.Sentence).input_operation(value), name_operations_input[1]: ImportGene(part2.Sentence).input_operation(value)}
        return r 
  
    def Associations(self,value):
        r = {name_operations_input[2]: MergeDataset("disease_evidences.tsv","gene_evidences.tsv",part2.AssociatedDisease).input_gene(value),name_operations_input[3]: MergeDataset("disease_evidences.tsv","gene_evidences.tsv",part2.AssociatedGene).input_disease(value)} 
        return r

