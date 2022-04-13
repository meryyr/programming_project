from flask import Flask, render_template, request
from part1 import *
import os
app = Flask(__name__, template_folder='template')


@app.route('/')
def home_page():                                                  #page for viewing the list of operations
    operations= Registry().name_operations
    op_input = Registry().name_operations_input
    return render_template('home.html', operations = operations, op_input = op_input)

@app.route('/gene')                                               #page for viewing the gene tsv file
def gene(): 
    filename = 'gene_evidences.tsv' 
    data = pd.read_csv(filename, header=0, delimiter = '\t') 
    data = data.to_html()                                  
    size = os.path.getsize('gene_evidences.tsv')            
    return render_template('gene.html', data = data, size = size)

@app.route('/disease') #page for viewing the disease tsv file
def disease(): 
    filename = 'disease_evidences.tsv' 
    data = pd.read_csv(filename, header=0, delimiter = '\t') 
    data = data.to_html()
    size = os.path.getsize('disease_evidences.tsv')
    return render_template('disease.html', data = data, size = size) 
  

@app.route('/operation_SentenceGene', methods = ['GET','POST'])   #page for viewing the sentences associated to the gene input
def sentencegene(): 
    if request.method == 'POST':
       value = request.form['value']
       display = Registry().Sentences(value)['SentenceGene']
       return render_template('sentencegene.html', display=display, value= value)
    else: 
       value = 'No input yet'
       return render_template('sentencegene.html', value= value)



@app.route('/operation_SentenceDisease', methods=['GET','POST'])  #page for viewing the sentences associated to the disease input
def sentencedisease():
    if request.method == 'POST':
        value = request.form['value']
        display = Registry().Sentences(value)['SentenceDisease']
        return render_template('sentencedisease.html', display=display, value= value)        
    else: 
        value = 'No input yet'
        return render_template('sentencedisease.html', value=value)


@app.route('/operation_AssociatedDiseases', methods=['GET','POST']) #page for viewing the diseases associated to the gene input
def associatedisease():
    if request.method == 'POST':
        value = request.form['value']        
        display = Registry().Associations(value)['AssociatedDiseases']
        return render_template('associatedisease.html', display=display, value= value)
    else:
        value = 'No input yet'
        return render_template('associatedisease.html', value= value)



@app.route('/operation_AssociatedGenes', methods=['GET','POST']) #page for viewing the genes associated to the disease input
def associatedgene():
    if request.method == 'POST':
        value = request.form['value']  
        display = Registry().Associations(value)['AssociatedGenes']
        return render_template('associatedgene.html', display=display,value= value)
    else: 
        value = 'No input yet'
        return render_template('associatedgene.html',value= value)


@app.route('/operation')                                        #page for viewing the operations that do not require an input
def operation():
    
    my_operation = request.args.get('type')
    
    if  (my_operation == 'RowsColumnsGene') or (my_operation == 'RowsColumnsDisease'):
        display = Registry().RowsColumns()[my_operation]
        return render_template('operation.html', title=my_operation, operation=my_operation, display=display)
    
    elif (my_operation == 'ColumnLabelGene') or (my_operation == 'ColumnLabelDisease'):
       display = Registry().ColumnLabel()[my_operation]
       return render_template('operation.html', title=my_operation, operation=my_operation, display=display)
       
    elif (my_operation == 'DistinctGene') or (my_operation == 'DistinctDisease'):
        display = Registry().Distinct()[my_operation]
        return render_template('operation.html', title=my_operation, operation=my_operation, display=display)
     
    elif (my_operation == 'MostFrequentAssociations'):
         display = Registry().Merge()[my_operation]
         return render_template('operation.html', title=my_operation, operation=my_operation, display=display)


if __name__ == '__main__':
    app.run(debug=True)
