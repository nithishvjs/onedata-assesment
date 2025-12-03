from flask import Flask

app = Flask(__name__)

@app.route('/todo')
def hello():
    return '<h1>Hello, From Todo😊!!</h1>'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

