from flask import Flask,render_template,redirect,json,session,url_for,request
import os
app=Flask(__name__)

app.secret_key = 'your_secret_key'  # Set a secret key for session management


login_data_file = "static/username.json"
## _______File System_________


if not os.path.exists(login_data_file):
    with open(login_data_file, 'w') as file:
        file.write('[]')  # Initialize with an empty list


# Read the JSON data from file
def read(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

# Write the JSON data to file
def write(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


## _________Routes_____________
@app.route("/")
# @guest
def home():
    # if 'email' in session:
    return redirect(url_for('movielab'))
    # return render_template("login.html")



@app.route("/login", methods=["POST", "GET"])
# @guest
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        login_data = read(login_data_file)
        for user_data in login_data:
            if user_data['email'] == email:
                if user_data['password'] == password:
                    session['email'] = email  # Store the username in the session
                    return redirect(url_for('movielab'))
                else:
                    return render_template("login.html", myMsg="Invalid password")
        else:
            return render_template("login.html", myMsg="User is not registered, Please Register ! ")      
    return render_template("login.html")



@app.route("/logout")
# @auth
def logout():
    session.pop('email', None)  # Remove the username from the session
    session.clear()
    return redirect(url_for('movielab'))


@app.route("/movielab")
def movielab():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)