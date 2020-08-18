import json
from flask import Flask, request

# Creates and names a new Flask app / web server
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
# default routing (whenever someone navigates to / run main page); accepts both GET and POST methods
def main_page():
    global people
    maxSafe = 580
    if request.method == 'GET':
        # Writes the value of people to terminal
        app.logger.info(people)
        percentage = round(100 * (int(people) / int(maxSafe)))
        color = 'rgb(235, 97, 52)'  # Red Color
        status = 'Not Safe'
        if int(people) < maxSafe:
            color = 'rgb(85,183,75)'  # Green Color
            status = 'Safe'
        # returns this entire block of HTML - should change to a template but stretched for time
        return '''
        <html>
         <meta http-equiv="refresh" content="5" />
            <head>
                <title>Library COVID Tracker</title>
            </head>
            <body style="color: white; font-family: Futura; text-align: center; background-color:''' + color + '''">
                <div style="display: inline-block; width: 100%; white-space: nowrap;">
                    <h1 style="text-align: left; padding-left: 10px; font-size: 50px"> Library </h1>
                    <h1 style="text-align: right; padding-right: 10-px; font-size: 200px">''' + str(percentage) + '''%</h1>
                    <h1 style="font-size: 50px">''' + status + '''</h1>
                </div>
                <div style="background-color: white; padding: 10px; color: black">
                    <p style="text-align: left"> Current Occupancy </p>
                    <p style="text-align: right"> Maximum Safe Occupancy </p>
                    <h1 style="text-align: left">''' + str(people) + '''</h1>
                    <h1 style="text-align: right">''' + str(maxSafe) + '''</h1>
                </div>
            </body>
        </html>'''
    # if its a post request, strip the data of the number of people and update the people variable with it
    elif request.method == 'POST':
        data = request.data
        people = Update(data)
        # Then returns that the update was successful and displays number of people updated with
        return 'Successful Update with: ' + str(people)


def Update(data):
    global people
    data = data.decode("utf-8")
    data = json.loads(data)
    people = data['users']
    app.logger.info(people)
    return people

    # forces to listen to all hosts on port 80
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=True)
