from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Hauptseite.html')

@app.route('/Zweitseite')
def second_page():
    return render_template('Zweitseite.html')

@app.route('/Test')
def third_page():
    return render_template('Test.html')

@app.route('/Anmelden')
def fourth_page():
    return render_template('Anmelden.html')

@app.route('/Registrieren')
def fifth_page():
    return render_template('Registrieren.html')

if __name__ == "__main__":
    app.run(debug=True)