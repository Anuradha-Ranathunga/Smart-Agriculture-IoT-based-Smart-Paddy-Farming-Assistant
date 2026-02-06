from flask import Flask, request, session, jsonify
from utils.user import User
import pyrebase
import json
from datetime import datetime

app=Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Add secret key for sessions

# Initialize user with app
user=User(app)

# Firebase configuration (using the same config as in the Arduino code)
firebase_config = {
    "apiKey": "AIzaSyCMsRoYBGZnnttlDbtScuMfhHfqYnF57R0",
    "authDomain": "agrisage-85205.firebaseapp.com",
    "databaseURL": "https://agrisage-85205-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "agrisage-85205",
    "storageBucket": "agrisage-85205.appspot.com",
    "messagingSenderId": "123456789",  # Placeholder - not used for database
    "appId": "1:123456789:web:abc123"  # Placeholder - not used for database
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

@app.route("/sign-in", methods=['GET', 'POST'])
def signIn():
    emailAddress = str(request.args['emailAddress'])
    password = str(request.args['password'])
    
    status, user_=user.logInUser(emailAddress=emailAddress, password=password)
    
    if status == "Loging successfull":
        responce={"status": status, 'username': user_['username']}
        
    elif status == "Incorrect password":
        responce={"status": status, 'username': None}
        
    elif status == "User not found":
        responce={"status": status, 'username': None}
        
        
    return jsonify({"responce": responce})


@app.route("/validate-password", methods=['GET', 'POST'])
def validatePassword():
    password = str(request.args['password'])
    
    status=user.validatePassword(password=password)
    
    responce={"status": status}
    
    return jsonify({"responce" : responce})



@app.route("/sign-up", methods=['GET', 'POST'])
def signUp():
    username = str(request.args['username'])
    emailAddress = str(request.args['emailAddress'])
    phoneNumber = str(request.args['phoneNumber'])
    password = str(request.args['password'])
        
    status=user.addUser(username=username, emailAddress=emailAddress, phoneNumber=phoneNumber, password=password)
    
    if status:
        session['loggedIn'] = True
        session['emailAddress'] = emailAddress
        session['username']=username
        
        responce={"status": "success", 'username': username}
        
    else:
        responce={"status": "unsuccess", 'username': None}

    return jsonify({"responce" : responce})


# IoT Data Endpoints
@app.route("/iot-data", methods=['GET'])
def get_iot_data():
    """Get all IoT sensor data"""
    try:
        # Get all data from Firebase
        iot_data = db.child("1234").get().val()
        
        if iot_data:
            return jsonify({
                "status": "success",
                "data": iot_data,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No IoT data available"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/iot-data/<field>", methods=['GET'])
def get_iot_field(field):
    """Get specific IoT sensor data field"""
    try:
        # Get specific field from Firebase
        field_data = db.child("1234").child(field).get().val()
        
        if field_data is not None:
            return jsonify({
                "status": "success",
                "field": field,
                "value": field_data,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"No data available for field: {field}"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/threshold", methods=['GET', 'POST'])
def manage_threshold():
    """Get or set the water level threshold"""
    try:
        if request.method == 'GET':
            # Get current threshold
            threshold = db.child("123").child("threshold").get().val()
            
            if threshold is not None:
                return jsonify({
                    "status": "success",
                    "threshold": threshold
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Threshold not set"
                }), 404
        
        elif request.method == 'POST':
            # Set new threshold
            new_threshold = request.json.get('threshold')
            if new_threshold is not None:
                db.child("123").update({"threshold": new_threshold})
                
                return jsonify({
                    "status": "success",
                    "message": "Threshold updated successfully",
                    "threshold": new_threshold
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Threshold value is required"
                }), 400
                
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/iot-history", methods=['GET'])
def get_iot_history():
    """Get historical IoT data (placeholder - would need to be implemented with timestamped data)"""
    try:
        # For now, return the current data
        iot_data = db.child("1234").get().val()
        
        return jsonify({
            "status": "success",
            "data": iot_data,
            "history_available": False,
            "message": "Historical data not yet implemented in this version"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__=="__main__":
    app.run(debug=True, port=5000)