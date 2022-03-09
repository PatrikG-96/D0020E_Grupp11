from flask import Flask, request
app = Flask(__name__)

@app.route('/login')
def login():
    if request.method == 'GET':
        args = request.args.get('asb')
        print (args)
        return f'Boop'



app.run(port=3456)
