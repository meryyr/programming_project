from flask import Flask, render_template, request,redirect, url_for
from part1 import *
import os
app = Flask(__name__, template_folder='template')


@app.route('/')
def home_page():
    operations= Registry().name_operations
    op_input = Registry().name_operations_input
    return render_template('home.html', operations = operations, op_input = op_input)

@app.route('/gene') #page for viewing the gene tsv file
def gene(): 
    filename = 'gene_evidences.tsv' 
    data = pd.read_csv(filename, header=0, delimiter = '\t') #reading
    data = data.to_html() #making an html table of the file
    size = os.path.getsize('gene_evidences.tsv') #getting the size of the file, which we get in bits/bytes 
    return render_template('gene.html', data = data, size = size) #forwarding 'data' which is an html table of the tsv file, and 'size' which is the size..

@app.route('/disease') #page for viewing the disease tsv file
def disease(): 
    filename = 'disease_evidences.tsv' 
    data = pd.read_csv(filename, header=0, delimiter = '\t') 
    data = data.to_html()
    size = os.path.getsize('disease_evidences.tsv')
    return render_template('disease.html', data = data, size = size) 
  
@app.route('/operation_SentenceGene')
def SentenceGene():
    value = 'No input yet'
    return render_template('sentencegene.html', value= value)
   
@app.route('/operation_SentenceGene', methods=['POST'])
def sentence_gene():
    value = request.form['value']
    display = Registry().Sentences(value)[str('SentenceGene')]
    return render_template('sentencegene.html', display=display, value= value)


@app.route('/operation_SentenceDisease')
def SentenceDisease():
    value = 'No input yet'
    return render_template('sentencedisease.html', value=value)

@app.route('/operation_SentenceDisease', methods=['POST'])
def sentence_disease():
    value = request.form['valued']
    display = Registry().Sentences(value)[str('SentenceDisease')]
    return render_template('sentencedisease.html', display=display, value= value)



@app.route('/operation_AssociatedDiseases')
def AssociatedDisease():
    value = 'No input yet'
    return render_template('associatedisease.html', value= value)

@app.route('/operation_AssociatedDiseases', methods=['POST'])
def associate_disease():
    value = request.form['valuedis']        
    display = Registry().Associations(value)[str('AssociatedDiseases')]
    return render_template('associatedisease.html', display=display, value= value)



@app.route('/operation_AssociatedGenes')
def AssociatedGenes():
    value = 'No input yet'
    return render_template('associatedgene.html',value= value)

@app.route('/operation_AssociatedGenes', methods=['POST'])
def associated_gene():
    value = request.form['valueg']  
    display = Registry().Associations(value)[str('AssociatedGenes')]
    return render_template('associatedgene.html', display=display,value= value)



@app.route('/operation', methods=['GET'])
def operation():
    
    my_operation = request.args.get('type')
    

    if str(my_operation) == 'RowsColumnsGene' or str(my_operation) == 'RowsColumnsDisease' :
        display = Registry().RowsColumns()[str(my_operation)]
        return render_template('operation.html', title=my_operation, operation=my_operation, display=display)
    
    elif str(my_operation) == 'ColumnLabelGene' or str(my_operation) == 'ColumnLabelDisease' :
       display = Registry().ColumnLabel()[str(my_operation)]
       return render_template('operation.html', title=my_operation, operation=my_operation, display=display)
       
    elif str(my_operation) == 'DistinctGene' or str(my_operation) == 'DistinctDisease' :
        display = Registry().Distinct()[str(my_operation)]
        return render_template('operation.html', title=my_operation, operation=my_operation, display=display)
     
  
    elif str(my_operation) == 'MostFrequentAssociations':
         display = Registry().Merge()[str(my_operation)]
         return render_template('operation.html', title=my_operation, operation=my_operation, display=display)

    


if __name__ == '__main__':
    app.run(debug=True)
