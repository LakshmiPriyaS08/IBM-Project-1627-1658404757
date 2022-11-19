
import pickle
import sqlite3 as sql
from flask import Flask, request, render_template

app= Flask(__name__)

model = pickle.load(open('','rb'))
scale = pickle.load(open('','rb'))

@app.route('/')
def home():
    return render_template('frontpage.html')



@app.route('/registerpage')
def registerpage():
    return render_template('register.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['uname']
            password = request.form['password']
            email = request.form['email']

            print(name,password,email)
            with sql.connect("user_login.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (name,password,email) VALUES (?,?,?)", (name, password, email))
                con.commit()
                msg = "Record successfully added!"
                cur.execute("SELECT * FROM user")
                con.commit()
                output = cur.fetchall()
                for row in output:
                    print(row)
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("register.html", msg=msg)
            con.close()




@app.route('/predict',methods=["POST","GET"])
def predict():
    # I have modified the feature names.
    # The model is trained to make prediction with this specific set of data.

    # Make sure you follow the above order when you get the data from the user
    mintmp = float(request.form['MinTemp'])
    maxtemp = float(request.form['MaxTemp'])
    Rainfall = float(request.form['Rainfall'])
    Sunshine = request.form['Sunshine']
    Evaporation = request.form['Evaporation']
    WindGustSpeed = float(request.form['WindGustSpeed'])
    WindSpeed9am = float(request.form['WindSpeed9am'])
    WindSpeed3pm = float(request.form['WindSpeed3pm'])
    Humidity9am = float(request.form['Humidity9am'])
    Humidity3pm = float(request.form['Humidity3pm'])
    Pressure9am = float(request.form['Pressure9am'])
    Pressure3pm = float(request.form['Pressure3pm'])
    Cloud9am = float(request.form['Cloud9am'])
    Cloud3pm = float(request.form['Cloud3pm'])
    Temp9am = float(request.form['Temp9am'])
    Temp3pm = float(request.form['Temp3pm'])

    data = []
    prediction=model.predict(data)
    prob = model.predict_proba(data)
    print (prediction)
    percentage = prob[0][1]*100
    if prediction == "Yes":
        print(f"There is a  chance it will rain today")
        return render_template("chances.html",msg =percentage)
    else:
        print(f"There is a  chance it won't rain today")
        return render_template("noChance.html",msg =percentage)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
