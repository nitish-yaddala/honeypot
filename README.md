# Suggested python version 3.10.12
## Steps to Run:

- Clone the project using `git clone git@github.com:Stranger825/honeypot.git`

- Run `sudo python3 -m pip install honeypots` 
- Run `sudo apt install dbus-x11`
- Run `start_honeypot.sh` bash sript to start the services in the honeypot.
- Run `stop_honeypot.sh` bash sript to stop the services in the honeypot.

OR

- Manually run all the below commands.

### Start logswebsite service for remote monitoring through a browser.
In terminal 1:
- Run `cd logsserver`
- Run `python3 logswebsite.py` 

### Choose and start required services in the honeypot. Make sure honeypots module is installed.
- In terminal 2, run the Logs webserver:
    - Then run, `sudo -E python3.10 -m honeypots --setup <SERVICE1,SERVICE2,SERVICE3> --config config.json`
- Stop the above process whenever you feel like.

### Start HTTP Honeypot.
- In terminal 3, run the dummy server:
    - Run `cd httphoneypot`
    - Run `sudo python3 -m http.server 80`

### Monitor modifications in the logs files.
- In terminal 4, start the monitoring script:
- Start the monitoring process daemon for the script `python3 monitor.py`



## Things left to do

- Write an analysis script to detect anomaly.
- Snort log monitoring.
- Firewall configuration.
