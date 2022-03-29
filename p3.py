from flask import Flask, render_template, request,redirect, url_for
from part1 import *
app = Flask(__name__, template_folder='template')


@app.route('/')
def home_page():
    operations= Registry().name_operations()
    op_input = Registry().name_operations_input()
    return render_template('home.html', operations = operations, op_input = op_input)
  
  
@app.route('/operation_SentenceGene')
def SentenceGene():
    return render_template('sentencegene.html')
   
@app.route('/operation_SentenceGene', methods=['POST'])
def sentence_gene():
    value = request.form['value']
    display = Registry().Sentences(value)[str('SentenceGene')]
    return render_template('sentencegene.html', display=display)


@app.route('/operation_SentenceDisease')
def SentenceDisease():
    return render_template('sentencedisease.html')

@app.route('/operation_SentenceDisease', methods=['POST'])
def sentence_disease():
    value = request.form['valued']
    display = Registry().Sentences(value)[str('SentenceDisease')]
    return render_template('sentencedisease.html', display=display)

@app.route('/operation_AssociatedDisease')
def AssociatedDisease():
    return render_template('associatedisease.html')

    
@app.route('/operation_AssociatedDisease', methods=['POST'])
def associate_disease():
    value = request.form['valuedis']        
    display = Registry().Associations(value)[str('AssociatedDiseases')]
    return render_template('associatedisease.html', display=display)

@app.route('/operation_AssociatedGenes')
def AssociatedGenes():
    return render_template('associatedgene.html')

@app.route('/operation_AssociatedGenes', methods=['POST'])
def associated_gene():
    value = request.form['valueg']        
    display = Registry().Associations(value)[str('AssociatedGenes')]
    return render_template('associatedgene.html', display=display)


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
     
  
    elif str(my_operation) == 'Merge':
         display = Registry().Merge()[str(my_operation)]
         html = display.to_html()
        
         text_file = open("merge.html", "w")
         text_file.write(html)
         text_file.close()
         return render_template('merge.html')


if __name__ == '__main__':
    app.run(debug=True)
