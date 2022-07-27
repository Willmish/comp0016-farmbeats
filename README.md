# comp0016-farmbeats
[![Lintly-Flake8 CI](https://github.com/Willmish/comp0016-farmbeats/actions/workflows/flake8-ci.yml/badge.svg)](https://github.com/Willmish/comp0016-farmbeats/actions/workflows/flake8-ci.yml)

# Project intro:

See the project website for more details: http://students.cs.ucl.ac.uk/2021/group28/

# Setup guide

The Project consists of 2 standalone programs: Raspberry Pi edge program and Desktop GUI program, located repsectively in `src/` directory and `gui_code/` directory. Currently there is a single requirements.txt file for both programs.

## Edge device

Install requirements with `pip install -r requirements.txt`. Also required: Grove library, link to be added @Willmish.

## Dekstop device

Install requirements with `pip install -r requirements.txt`. Also required: Pyodbc and MS odbc driver.

To install pyodbc, ODBC header files are required to build pyodbc buildwheel

For ubuntu, package `unixodbc-dev` is required:

    `sudo apt install unixodbc-dev`
Then, install `pyodbc`:

    `pip install pyodbc`
    
Follow the guide for your OS to install (it should also include an installtion of ODBC header files mentioned above): https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#ubuntu18

# System design

## Overall system design (target)
![farmbeats_architecture-gitflow drawio](https://user-images.githubusercontent.com/26546660/159375322-37a150eb-5d5b-4a86-83e2-f3893e6fc923.png)
Above is the overall target design of the current system.

## Edge device
![farmbeats_architecture-Pubsub message flow drawio](https://user-images.githubusercontent.com/26546660/159303724-5903e01a-397b-4cc7-96f3-81f41a895f9c.png)
This diagram shows the flow of messages in the system using Publisher-Subscriber design pattern along with basic annotation of key events in the system:
* `sensor`s being called to `collect()` data, and sending `SensorData` objects over `pubsub`.
* `analyser`s updating its instances of `PID` class, with new sensor data and getting new `output` results, attaching to the `SensorData` object received and sending over `pubsub`
* `data_streamer`s listening in on messages sent on the `database_update.actuator` topic, and saves the data to the currently selected DB (default is Azure SQL DB in cloud)
* `actuator`s are listening in on messages sent on the `database_update.actuator` and `pid_update.actuator` topics, and the values for the actuators are updated. (fan speed, LED brightness, water pump state, etc)


## Most recent progress
Here is a GIF of the Desktop app displaying live data from the Azure DB, while the Rpi is collecting the data and streaming it to the IoT Hub!

![GUI_IOTHUB_DB_connection](https://user-images.githubusercontent.com/26546660/156930344-6451a020-8f30-40d0-82de-385ffb9b4bdd.gif)
