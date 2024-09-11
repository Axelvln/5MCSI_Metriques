from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)       

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def moncontact():
    return render_template("contact.html")
  
#@app.route("/commits/")
#def moncommits():
#    return render_template("commits.html")

@app.route('/commits/')
def show_commits():
    data = get_commits()
    return render_template('commits.html', chart_data=data)

def get_commits():
    url = "https://api.github.com/repos/blablapola/5MCSI_Metriques/commits"
    
    # Utiliser urllib pour faire une requête GET
    response = urlopen(url)
    
    # Lire et décoder la réponse
    raw_data = response.read().decode('utf-8')
    
    # Charger la réponse JSON
    commits = json.loads(raw_data)
    
    # Dictionnaire pour compter les commits par minute
    commit_per_minute = defaultdict(int)

    for commit in commits:
        commit_date_str = commit['commit']['author']['date']
        commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
        commit_minute = commit_date.strftime("%Y-%m-%d %H:%M")
        commit_per_minute[commit_minute] += 1

    # Préparer les données pour le graphique
    chart_data = [["Minute", "Nombre de commits"]]
    for minute, count in sorted(commit_per_minute.items()):
        chart_data.append([minute, count])

    return chart_data

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
  
if __name__ == "__main__":
  app.run(debug=True)
