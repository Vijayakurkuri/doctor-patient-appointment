from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Temporary data storage
doctors = {
    'Dr.shivani': {'password': 'password1', 'name': 'Dr.shivani', 'specialization': 'Cardiologist'},
    'Dr.ravi krishna': {'password': 'password2', 'name': 'Dr.ravi krishna', 'specialization': 'Dermatologist'},
    'Dr.shyamala': {'password': 'password3', 'name': 'Dr.shyamala', 'specialization': 'Orthopedic Surgeon'},
    'dr.prasad': {'password': 'password4', 'name': 'dr.prasad', 'specialization': 'neurologist'},
    'dr.siva': {'password': 'password5', 'name': 'dr.siva', 'specialization': 'dentist'},
    'dr.gayithri': {'password': 'password6', 'name': 'dr.gayithri', 'specialization': 'psychiatrists'},
    'dr.lasya': {'password': 'password6', 'name': 'dr.lasya', 'specialization': 'radiologist'}
 }

appointments = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    name = ''
    if request.method == 'POST' and 'username' in request.form:
        name = request.form['username']
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in doctors:
            return render_template('register.html', error='Username already exists')
        doctors[username] = {'password': password, 'name': '', 'specialization': ''}
        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in doctors and doctors[username]['password'] == password:
            session['username'] = username
            return redirect('/dashboard')
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], doctors=doctors, appointments=appointments)
    return redirect('/')
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        if request.form.get('confirm') == 'yes':
            session.pop('username', None)
            return redirect('/')
        else:
            return redirect('/dashboard')
    return render_template('logout_confirmation.html')



@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if 'username' in session:
        if request.method == 'POST':
            doctor = request.form['doctor']
            date = request.form['date']
            time = request.form['time']
            appointment_datetime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
            if doctor not in appointments:
                appointments[doctor] = []
            appointments[doctor].append(appointment_datetime)
            return render_template('appointment_successful.html', doctor_name=doctors[doctor]['name'], specialization=doctors[doctor]['specialization'], appointment_datetime=appointment_datetime)

        return render_template('schedule.html', doctors=doctors)
    return redirect('/')
@app.route('/appointment_successful')
def appointment_successful():
    return render_template('appointment_successful.html')



if __name__ == '__main__':
    app.run(debug=True)
