from flask import Flask, render_template, request, url_for, redirect
import requests
from tkinter import messagebox
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

url="https://api.meteomatics.com/"
username="none_bagaria"
password="Ogd10Z1d1U"

have_details=False
var=1
temperature=[]
precipitation=[]
wind_speed=[]
@app.route("/")
def home():
    global have_details
    have_details=False
    
    return render_template("index.html", have_details=have_details)

@app.route('/weather_report', methods=['POST'])
def weather_report():
    global have_details, temperature, precipitation, wind_speed
    have_details=True

    # latlong=request.form['latlong']
    # starting_date=request.form['starting_date']
    # ending_date=request.form['ending_date']
    
    latlong="-25.480877,-49.304424"
    starting_date="2023-07-23"
    ending_date="2023-07-26"

    response=requests.get(f"{url}{starting_date}T00:00:00Z--{ending_date}T00:00:00Z:PT1H/t_2m:C,precip_1h:mm,wind_speed_10m:ms/{latlong}/json", 
                          auth=(username, password)
                          ).json()
    var2=1
    for data in response['data'][0]["coordinates"][0]['dates']:
        scraped_data=[]
        for tuples in data.items():
            scraped_data.append(tuples[1])
            if var2==2:
                date1=scraped_data[0].split('T')[0]
                date2=scraped_data[0].split('T')[1].split(':00Z')[0]
                update_date=f"{date1} {date2}h"
                temperature.append({'date':update_date,'value':scraped_data[1]})
                scraped_data=[]
                var2=0
            var2+=1
    
    var2=1
    for data in response['data'][0]["coordinates"][0]['dates']:
        scraped_data=[]
        for tuples in data.items():
            scraped_data.append(tuples[1])
            if var2==2:
                date1=scraped_data[0].split('T')[0]
                date2=scraped_data[0].split('T')[1].split(':00Z')[0]
                update_date=f"{date1} {date2}h"
                precipitation.append({'date':update_date,'value':scraped_data[1]})
                scraped_data=[]
                var2=0
            var2+=1
       
    var2=1
    for data in response['data'][0]["coordinates"][0]['dates']:
        scraped_data=[]
        for tuples in data.items():
            scraped_data.append(tuples[1])
            if var2==2:
                date1=scraped_data[0].split('T')[0]
                date2=scraped_data[0].split('T')[1].split(':00Z')[0]
                update_date=f"{date1} {date2}h"
                wind_speed.append({'date':update_date,'value':scraped_data[1]})
                scraped_data=[]
                var2=0
            var2+=1
    
    return render_template("index.html", have_details=have_details, temperature=temperature, precipitation=precipitation, wind_speed=wind_speed, var=var)

@app.route('/1')   
def function1():
    global var
    var=1
    return render_template("index.html", have_details=have_details, temperature=temperature, precipitation=precipitation, wind_speed=wind_speed, var=var)
    
@app.route('/2')   
def function2():
    global var
    var=2
    return render_template("index.html", have_details=have_details, temperature=temperature, precipitation=precipitation, wind_speed=wind_speed, var=var)
    
@app.route('/3')   
def function3():
    global var
    var=3
    return render_template("index.html", have_details=have_details, temperature=temperature, precipitation=precipitation, wind_speed=wind_speed, var=var)

if __name__ == '__main__':
    app.run(debug=True)
