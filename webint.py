from flask import Flask, render_template, request
import subprocess
import csv

app = Flask(__name__)

p = None

@app.route('/', methods=['GET'])
def home():
    r = open('stockinput.csv', 'r')
    reader = csv.reader(r)
    symbols = {}
    for line in reader:
        k, v = line
        symbols[k] = v
    r.close()
    global p
    if p is None:
        p = subprocess.Popen(["python", "fin.py"])
    return render_template('home.html', symbols=symbols)

@app.route('/edit', methods={'GET'})
def edit():
    global p
    p.terminate()
    p = None
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
    if symbol in symbols:
        cur = symbols[symbol]
        symbols[symbol] = float(cur) + float(shares)
    else:
        symbols[symbol] = shares
    f.close()

    w = open('stockinput.csv', 'w')
    writer = csv.writer(w, delimiter=',', lineterminator='\n')
    for key, val in symbols.items():
        writer.writerow([key, val])
    w.close()
    return render_template('addedStock.html')

@app.route('/deleteStock', methods=['GET'])
def delStock():
    symbol = str(request.args.get('symbol'))
    shares = str(request.args.get('shares'))

    f = open('stockinput.csv', 'r')
    reader = csv.reader(f)
    symbols = {}
    for line in reader:
        if line != '':
            k, v = line
            symbols[k] = v
    if symbol in symbols:
        curshares = symbols[symbol]
        changeshares = float(curshares) - float(shares)
        if changeshares <= 0:
            del symbols[symbol]
        else:
            symbols[symbol] = changeshares
    f.close()

    w = open('stockinput.csv', 'w')
    writer = csv.writer(w, delimiter=',', lineterminator='\n')
    for key, val in symbols.items():
        writer.writerow([key, val])
    w.close()
    return render_template('deletedShares.html')


app.run(host='0.0.0.0', debug=True)
