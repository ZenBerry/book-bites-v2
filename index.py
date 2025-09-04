from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Haha'

@app.route('/about')
def about():
    return 'Horse'

if __name__ == "__main__":
    app.run(port=3000, debug=True)
