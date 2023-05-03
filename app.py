from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename #used to store the image file with a name void of any accessing issues
import telegram_bot

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# @app.route('/get_trends')
# def get_trends():
#     # get stored sensor data and current trends about the traffic
    
#     # return the response as JSON so as to render it in HTML
#     return jsonify({"N":15,"S":21,"E":37,"W":22})

# will be used in the server side
@app.route('/traffic/',methods=["GET","POST"])
def traffic_rules():
    if request.method == "POST":
        print(request.files)
        if "file" in request.files:
            f = request.files["file"]
            f.save(f"./images/{secure_filename(f.filename)}")
            """
                do an async function call to a new function that will run the model
                on the image and alert the telegram user in case the traffic rules are
                violated using the telegram_bot.send_alert_telegram routine
            """
            # telegram_bot.send_alert_telegram()
            return "File uploaded"
        else:
            return "Wrong input format"
    elif request.method == "GET":
        return "Upload an image using POST request"

@app.route("/get_code/<name>")
def code_da(name):
    return send_file(f"{name}.py")

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)