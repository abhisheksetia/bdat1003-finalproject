from flask import Flask, jsonify, request, render_template,Response
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import json
import requests
import schedule
import time

app = Flask(__name__)
url = "http://api.weatherstack.com/current?access_key=54790c67b2580ecbc570b5a6d728b401&query=New%20York"

querystring = {"lat":"35.5","lon":"-78.5"}



response = requests.request("GET", url)

# Connect to MongoDB

client = MongoClient('localhost', 27017)
db = client.test
collection = db["data3"]

# Insert the API response into MongoDB
collection.insert_one(response.json())

print("API data saved")

# Schedule the batch process to run every 24 hours
schedule.every(24).hours.do(collection)

while True:
    schedule.run_pending()
    time.sleep(1)

db = db.Population
#db.insert_many(data)

# Retrieve Data from MongoDB (All data)
cursor=db.find({}, {'_id': False}).sort([('Rank', 1)])
list_cur = list(cursor)
#df_from_mongo = pd.DataFrame(list_cur)

## Web Page Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datatable', methods=("POST", "GET"))
def html_table():
    print(list_cur)
    return render_template('data.html',  data=list_cur)

@app.route('/members')
def html_members():
    return render_template('members.html')

@app.route('/members')
def html_members():
    return render_template('members.html')

@app.route('/googlechart')
def html_members():
    return render_template('googlechart.html')


@app.route('/graph')
def html_songpop():
    data = list_cur[:10]
    fig, ax = plt.subplots()
    ax.pie([c['pop_2022'] for c in data], labels=[c['Country'] for c in data], autopct='%1.1f%%')
    ax.set_title('Top 10 Countries by Population in 2022')
    plt.savefig('static/pie_chart.png')

    
    return render_template('songpop.html', pie_chart='static/pie_chart.png' )



if __name__ == "__main__":
    app.run()



