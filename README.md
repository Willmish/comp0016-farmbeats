# comp0016-farmbeats

To install pyodbc, ODBC header files are required to build pyodbc buildwheel

For ubuntu, package `unixodbc-dev` is required:

    `sudo apt install unixodbc-dev`

To connect to Azure DB, ODBC driver is required, in this case ODBC Driver 18 for SQL Server is used.

Follow the guide for your OS to install (it should also include an installtion of ODBC header files mentioned above): https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#ubuntu18

## Most recent progress
Here is a GIF of the Desktop app displaying live data from the Azure DB, while the Rpi is collecting the data and streaming it to the IoT Hub!

![GUI_IOTHUB_DB_connection](https://user-images.githubusercontent.com/26546660/156930344-6451a020-8f30-40d0-82de-385ffb9b4bdd.gif)
