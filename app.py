from flask import Flask, render_template, Response
from find_combinations import main
import json
app = Flask(__name__)

@app.route('/')
def home():
    trips = main(passenger_bags=[0,1,2,3])
    # print(trips)
    for nr_bags, trip_bag in trips.items():
        trips[nr_bags] = sorted(trip_bag, key=lambda k: k['total_price']) 
   
    return render_template('index.html', trips=trips, number_of_bags=trips.keys())


@app.route("/getDataJSON")
def getDataJSON():
    trips = main(passenger_bags=[0,1,2,3])
    trips = json.dumps(trips)
    return Response(
        trips,
        mimetype='application/json',
        headers={"Content-disposition":
                 "attachment; filename=trips.json"})
if __name__  == '__main__':
    app.run(debug=True)