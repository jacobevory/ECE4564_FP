from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    r = open('stockinput.csv', 'r')
    reader = csv.reader(r)
    symbols = {}
    for line in reader:
        k, v = line
        symbols[k] = v
    r.close()
    return render_template('home.html', symbols=symbols)

@app.route('/edit', methods={'GET'})
def edit():
    r = open('stockinput.csv', 'r')
    reader = csv.reader(r)
    symbols = {}
    for line in reader:
        if line != '':
            k, v = line
            symbols[k] = v
    r.close()
    return render_template('edit.html', symbols=symbols)

@app.route('/addStock', methods=['GET'])
def addStock():
    symbol = str(request.args.get('symbol'))
    shares = str(request.args.get('shares'))

    f = open('stockinput.csv', 'r')
    reader = csv.reader(f)
    symbols = {}
    for line in reader:
        if line != '':
            k, v = line
            symbols[k] = v
    symbols[symbol] = shares
    f.close()

    w = open('stockinput.csv', 'w')
    writer = csv.writer(w, delimiter=',', lineterminator='\n')
    for key, val in symbols.items():
        writer.writerow([key, val])
    w.close()
    return render_template('addedStock.html')


app.run(host='0.0.0.0', debug=True)
