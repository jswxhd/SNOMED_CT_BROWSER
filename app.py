from flask import Flask,render_template,request,redirect,url_for,g
from find_terms import sorted_results,sorted_results_2

app = Flask(__name__)

@app.route("/")
def home():

    return render_template('index.html')

@app.route('/search/',methods = ['POST', 'GET'])
def search():  
    if request.method == 'POST' and request.form.get('putin'):
        query = request.form['putin']
        global length,r,sy,fsn,c,p,gc,gp,am,ca,m,fs
        length,r,sy,fsn,c,p,gc,gp,am,ca,m,fs=sorted_results_2(query)
         
        
        return redirect(url_for('result',query =query,page =1,order=0))
        #return query

@app.route('/result/<query>/<int:page>/<int:order>',methods = ['POST', 'GET'])
def result(query,page,order):
    if request.method == 'POST':
        return redirect('search.html')
        
    
    #sorted_results_term, sorted_results_synonmys, sorted_children_term, sorted_parents_term, sorted_grandchildren_term, sorted_grandparents_term=sorted_results(query)

    return render_template('index.html',query=query,sorted_results_term=r, results_amount=length, sorted_results_synonmys=sy, sorted_results_FSN=fsn, sorted_results_children=c, 
                    sorted_results_parents=p, sorted_AM_term=am, sorted_CA_term=ca, sorted_M_term=m, sorted_FS_term=fs, page=page,order=order)



