from flask import Flask, render_template, request, session, make_response, flash

app = Flask(__name__, template_folder='templates')
app.secret_key = 'SECRET KEY'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html', message='index')

@app.route('/set_data')
def set_data():
    session['name'] = 'Precious'
    session['other'] = 'Hello world'
    return render_template('index.html', message='Session data set.')

@app.route('/get_data')
def get_data():
    if 'name' in session.keys() and 'other' in session.keys():
        name = session['name']
        other = session['other']
        return render_template('index.html', message= f'Name: {name}, Other: {other}' )
    else:
        return render_template('index.html', message=f'No session found')

@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('index.html', message='Cookie set'))
    response.set_cookie('cookie_name', 'cookie_value')
    return response

@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies['cookie_name']
    return render_template('index.html', message=f'Cookie')

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    if request.method == 'GET':
        return render_template('enter.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Precious' and password == "password":
            flash('Successful Login!')
            return render_template('index.html', message="")
        else:
            flash('Login Failed!')
            return render_template('index.html', message="")


if __name__ == '__main__':
    app.run(debug=True)