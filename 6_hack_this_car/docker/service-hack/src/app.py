#!/usr/bin/python3

from flask import Flask, render_template, request, make_response
import my_i2c
import time

app = Flask(__name__, static_url_path="", static_folder="templates")

ic2_bus = my_i2c.make_bus()
my_i2c.motor_slow(ic2_bus)

headlights_on = False

# Encrypted random words so it can't be guessed
valid_cookies = ["63757274696365", "61584d3d", "59513d3d", "67616d6572"]

@app.route("/robots.txt")
def robots():
    response = make_response("User-agent: *\nDisallow: /s3cr3t-p4g3/")
    response.headers["content-type"] = "text/plain"
    return response

@app.route("/s3cr3t-p4g3/")
def secret_page():
    return render_template('secret-page.html')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        response = make_response(render_template('index.html'))
        req_cookie = request.cookies.get('SESSION')
        if req_cookie is None:
            response.set_cookie('SESSION', '0.0.0.0')
            
        return response
    else:
        response = make_response("")
        req_cookie = request.cookies.get('SESSION')
        if req_cookie is None:
            response.set_cookie('SESSION', '0.0.0.0')
            return response
        else:
            actual_cookies = req_cookie.split('.')
            
            motor_status = {
                "forward-movement": "disabled",
                "left-movement": "disabled",
                "right-movement": "disabled",
                "backward-movement": "disabled"
            }
            
            if actual_cookies[0] == valid_cookies[0]:
                motor_status['forward-movement'] = "enabled"
            if actual_cookies[1] == valid_cookies[1]:
                motor_status['left-movement'] = "enabled"
            if actual_cookies[2] == valid_cookies[2]:
                motor_status['right-movement'] = "enabled"
            if actual_cookies[3] == valid_cookies[3]:
                motor_status['backward-movement'] = "enabled"
            
            return motor_status
            

@app.route("/flag-auth/", methods=['POST'])
def authenticate_flag():
    flags_dictionary = {
        "forward-movement": "flag{w3b_cr4w13r_ru135}",
        "left-movement": "flag{3ncrypt_y0ur_c00k135}",
        "right-movement": "flag{p05tm4n_p4t}",
        "backward-movement": "flag{d0nt_u53_3v41}"
    }
    
    data = request.json;
    cookies = request.cookies.get('SESSION').split('.')
    
    motor = data['motor']
    flag = data['flag']
    if flag == flags_dictionary[motor]:
        response = make_response("flag_correct")
        if motor == "forward-movement":
            cookies[0] = valid_cookies[0]
        elif motor == "left-movement":
            cookies[1] = valid_cookies[1]
        elif motor == "right-movement":
            cookies[2] = valid_cookies[2]
        elif motor == "backward-movement":
            cookies[3] = valid_cookies[3]
        
        response.set_cookie('SESSION', cookies[0] + '.' + cookies[1] + '.' + cookies[2] + '.' + cookies[3])
        
        return response
    else:
        return "flag_incorrect"
    
@app.route("/calculator", methods=['GET', 'POST'])
def calculator():
    if request.method == 'GET':
        return render_template('calculator.html')
    else:
        return str(eval(request.json['equation']))
        
@app.route("/flag-generator/", methods=['GET', 'POST'])
def generator():
    if request.method == 'GET':
        return render_template('generator.html')
    else:
        return "flag{p05tm4n_p4t}"
        
@app.route("/login/")
def admin():
    cookie = request.cookies.get('ADMIN')
    if cookie == 'true':
        return render_template('admin.html')
    else:
        response = make_response(render_template('login.html'))
        response.set_cookie('ADMIN', 'false')
        return response
    
@app.route('/movement/', methods=['POST'])
def movement():
    content = request.json
    cookies = request.cookies.get('SESSION').split('.')

    if content['direction'] == "forward":
        if cookies[0] == valid_cookies[0]:
            print("Moving forward...")
            my_i2c.forward(ic2_bus)
            return "Moving forward..."
        else:
            return "Forward movement not authorized"

    elif content['direction'] == "left":
        if cookies[1] == valid_cookies[1]:
            my_i2c.turn_left(ic2_bus)
            print("Moving left...")
            return "Moving left..."
        else:
            return "Leftward movement not authorized"

    elif content['direction'] == "right":
        if cookies[2] == valid_cookies[2]:
            my_i2c.turn_right(ic2_bus)
            print("Moving right...")
            return "Moving right..."
        else:
            return "Rightward movement not authorized"

    elif content['direction'] == "backward":
        if cookies[3] == valid_cookies[3]:
            my_i2c.backward(ic2_bus)
            print("Moving backward...")
            return "Moving backward..."
        else:
            return "Backward movement not authorized"

    elif content['direction'] == "stop":
        my_i2c.stop(ic2_bus)
        print("Stopping...")
        return "Stopping..."
        
    elif content['direction'] == "lights_on":
        my_i2c.lights_on(ic2_bus)
        print("Lights on")
        return "Lights on"
        
    elif content['direction'] == "lights_off":
        my_i2c.lights_off(ic2_bus)
        print("Lights off")
        return "Lights off"
        
    elif content['direction'] == "spin":
        if cookies[1] == valid_cookies[1] and cookies[2] == valid_cookies[2]:
            my_i2c.turn_left(ic2_bus)
            time.sleep(0.2)
            my_i2c.turn_right(ic2_bus)
            time.sleep(0.2)
            my_i2c.turn_left(ic2_bus)
            time.sleep(5)
            my_i2c.stop(ic2_bus)
            return "Spin cycle complete!"
        else:
            return "Unlock left and right movement to enable the spin cycle"

    else:
        return "Bad movement request"
        
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
