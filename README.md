# prusa2mqtt MK4

I recently purchased a Prusa MK4 3D Printer.  Unfortunately, the official home-assistant integration is not compatible with my printer <https://www.home-assistant.io/integrations/prusalink>.  This project is a quick attempt to get data I needed into a MQTT server, to be ingested by home-assistant.

- [Project Description](#project-description)
- [Features](#features)
- [Usage](#usage)
- [License](#license)

## Project Description

The purpose of this project is to provide a streamlined method for transferring Prusalink data to an MQTT server. By leveraging Python and Docker, this solution offers a straightforward and efficient approach to seamlessly handle data transmission.

## Supported / Tested / Required Prusalink Version
    api: 2.0.0
    server: 2.1.2


## Features

* Simplified Prusalink data integration with an MQTT server.
* Python-based implementation for flexibility and ease of use.
* Docker containerization for effortless deployment and scalability.

## Usage
Open the ".env" file using a text editor of your choice.
Look for the lines in the ".env" file that correspond to your MQTT and PrusaLink servers. 

file:  .env
    
    APP_VERSION="1.0" # Do Not Change
    MQTT_HOST="192.168.0.10"
    MQTT_PORT=1883
    MQTT_USER="mqtt-password" 
    MQTT_PASS="mqtt-password"
    PRUSALINK_HOST="http://192.168.0.20"
    PRUSALINK_USER="maker"
    PRUSALINK_PASS="password"
    PRUSALINK_CALLS="info,version,status" # Do Not Change
    PRUSALINK_UPDATE=30 $ Update Frequency

After you have edited your .env file, run the following commands.

    $ git clone <project>
    $ cd <project>
    $ docker-compose up -d && docker-compose logs -f

## License
    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
