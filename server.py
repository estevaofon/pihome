from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

pins = {
    '24': {'name': 'Ventilador', 'state': 0},
    '23': {'name': 'Lâmpada', 'state': 0}
    }

import os.path
if not os.path.isfile('pins.csv'):
    with open('pins.csv', 'w') as csvfile:
        fieldnames = ['pin', 'name', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'pin': '24', 'name': 'Ventilador', 'state': '0'})
        writer.writerow({'pin': '23', 'name': 'Lâmpada', 'state': '0'})


@app.route("/")
def main():
    with open('pins.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['pin'], row['state'])
            pins[row['pin']]['state'] = int(row['state'])
    templateData = {
        'pins': pins
        }
    return render_template('main.html', **templateData)


@app.route("/<changePin>/<action>")
def action(changePin, action):
    with open('pins.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['pin'], row['state'])
            pins[row['pin']]['state'] = int(row['state'])
    deviceName = pins[changePin]['name']
    if action == "on":
        pins[changePin]['state'] = 1
        message = "Turned " + deviceName + " on."
    if action == "off":
        pins[changePin]['state'] = 0
        message = "Turned " + deviceName + " off."

    with open('pins.csv', 'w') as csvfile:
        fieldnames = ['pin', 'name', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pin in pins:
            writer.writerow({'pin': pin, 'name': pins[pin]['name'],
                             'state': pins[pin]['state']})
    templateData = {
        'message': message,
        'pins': pins
        }
    return render_template('main.html', **templateData)


@app.route("/api")
def api():
    with open('pins.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['pin'], row['state'])
            pins[row['pin']]['state'] = row['state']
    for pin in pins:
        pins[pin]['state'] = str(pins[pin]['state'])

    return jsonify(**pins)

if __name__ == "__main__":
    app.run(debug=True)
