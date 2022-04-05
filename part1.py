import part2
import pandas as pd

class ImportDisease:

    def __init__(self, requested_operation, operations=(part2.RowsColumns, part2.ColumnLabel, part2.Distinct), datadisease="disease_evidences.tsv"):
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

    def __init__(self, requested_operation, operations=(part2.RowsColumns, part2.ColumnLabel, part2.Distinct), datagene="gene_evidences.tsv"):
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
    
    def __init__(self, dfdisease, dfgene):
        ImportDisease.__init__(self, dfdisease)
        ImportGene.__init__(self, dfgene)
        self.merged_dataset = pd.merge(self.dfdisease,self.dfgene,  on = ('pmid','sentence', 'nsentence'), how = "inner")
        
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

    def __init__(self,name_operations = ['RowsColumnsGene','RowsColumnsDisease','ColumnLabelGene','ColumnLabelDisease','DistinctGene','DistinctDisease','MergedDataset'],name_operations_input = ['SentenceDisease','SentenceGene','AssociatedDiseases','AssociatedGenes']):
        self.name_operations = name_operations
        self.name_operations_input = name_operations_input
        self.datsetdisease = "disease_evidences.tsv"
        self.datasetgene = "gene_evidences.tsv"
    
    def RowsColumns(self):
        operation = part2.RowsColumns
        r = {self.name_operations[0]: ImportGene(operation).operation(),
             self.name_operations[1]: ImportDisease(operation).operation()}
        return r 
    
    def ColumnLabel(self):
        operation = part2.ColumnLabel
        r = {self.name_operations[2]: ImportGene(operation).operation(),
             self.name_operations[3]: ImportDisease(operation).operation()}
        return r
            
    def Distinct(self):
        operation = part2.Distinct
        r = {self.name_operations[4]: ImportGene(operation).operation(),
             self.name_operations[5]: ImportDisease(operation).operation()}
        return r
    
    def Merge(self):
        operation = part2.MergedDataset
        r = {self.name_operations[6]: MergeDataset(self.datsetdisease,self.datasetgene,operation).operation()}
        return r
        
    def Sentences(self,value):
        operation = part2.Sentence
        r = {self.name_operations_input[0]: ImportDisease(operation).input_operation(value), self.name_operations_input[1]: ImportGene(operation).input_operation(value)}
        return r 
  
    def Associations(self,value):
        operation_disease = part2.AssociatedDisease
        operation_gene = part2.AssociatedGene
        r = {self.name_operations_input[2]: MergeDataset(self.datsetdisease,self.datasetgene,operation_disease).input_gene(value),self.name_operations_input[3]: MergeDataset(self.datsetdisease,self.datasetgene,operation_gene).input_disease(value)} 
        return r
