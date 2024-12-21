from flask import Flask, render_template_string, jsonify
from sense_emu import SenseHat
import time

app = Flask(__name__)

# Initialize the SenseHat object
sense = SenseHat()

@app.route('/')
def index():
    # HTML template embedded within the Python script
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sense HAT Data</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            function fetchSensorData() {
                $.get('/get_sensor_data', function(data) {
                    // Update the HTML with the received data
                    $('#temperature').text(data.temperature + ' °C');
                    $('#humidity').text(data.humidity + ' %');
                    $('#pressure').text(data.pressure + ' hPa');
                    $('#joystick').text(data.joystick);
                });
            }

            // Fetch data every 2 seconds
            $(document).ready(function() {
                fetchSensorData(); // Fetch initial data
                setInterval(fetchSensorData, 2000); // Fetch data every 2 seconds
            });
        </script>
    </head>
    <body>
        <h1>Sensor Information</h1>
        <p><strong>Temperature:</strong> <span id="temperature"></span></p>
        <p><strong>Humidity:</strong> <span id="humidity"></span></p>
        <p><strong>Pressure:</strong> <span id="pressure"></span></p>

        <h2>Joystick Status</h2>
        <p>Current joystick position: <span id="joystick"></span></p>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/get_sensor_data')
def get_sensor_data():
    # Get sensor data from the Sense HAT
    tem = sense.temperature
    hum = sense.humidity
    pressure = sense.pressure

    # Get events from the joystick
    events = sense.stick.get_events()
    joystick_state = "Center"
    for event in events:
        if event.action == "pressed":
            if event.direction == "up":
                joystick_state = "Up"
            elif event.direction == "down":
                joystick_state = "Down"
            elif event.direction == "left":
                joystick_state = "Left"
            elif event.direction == "right":
                joystick_state = "Right"
            elif event.direction == "middle":
                joystick_state = "Pressed"

    # Return sensor data as JSON
    return jsonify({
        'temperature': tem,
        'humidity': hum,
        'pressure': pressure,
        'joystick': joystick_state
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)