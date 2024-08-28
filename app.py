from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/login.html')
def home():
    return render_template("login.html")

@app.route('/register.html')
def register():
    return render_template("register.html")

@app.route('/forgotten.html')
def forgotten():
    return render_template('forgotten.html')

if __name__ == '__main__':
    app.run(debug=True)