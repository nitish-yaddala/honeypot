# Steps to Run

- Clone the project using `git clone git@github.com:Stranger825/honeypot.git`

In terminal 1, activate the virtual environment and install the `honeypots` pip package:
- Run `python3.8 -m pip install virtualenv`
- source `honeypotenv/bin/activate`
- Run `cd logsserver`
- Run `python3 logswebsite.py`


- In terminal 2, run the Logs webserver:
    - Run `python3 -m pip install honeypots`
    - Then run, `sudo -E python3.8 -m honeypots --setup <SERVICE1,SERVICE2,SERVICE3> --config config.json`
- Stop the above process whenever you feel like.

- In terminal 3, run the dummy server:
    - Run `cd httphoneypot`
    - Run `python3 -m http.server 80`

- In terminal 4, start the monitoring script:
- Start the monitoring process daemon for the script `python3 monitor.py`



# Things left to do

- Write an analysis script to detect anomaly.