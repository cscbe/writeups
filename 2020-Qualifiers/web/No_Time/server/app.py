from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "I have no time for this!"

@app.route("/login", methods=["POST"])
def login():
    pin = "198519891990"
    
    data = request.get_json()
    tried_pin = data["pin"]
    if not isinstance(tried_pin, str):
        return jsonify({ "message": "pin should be of type String" }), 400

    if len(tried_pin) != len(pin):
        return jsonify({ "message": "pin length is not correct" }), 400
    else:
        i = 0
        pin_correct = True

        while (pin_correct and i < len(pin)):
            if tried_pin[i] != pin[i]:
                pin_correct = False
                return jsonify({ "message": "wrong pin" }), 200
            i += 1
            time.sleep(0.5)
    return jsonify({ "message": "login successful", "flag": "CSCBE{M4rty_W3ve_G0T_to_GO_B4ck_1n_T1M3}" }), 200


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=4000)