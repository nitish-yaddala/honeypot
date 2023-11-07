# Steps to Run

- Clone the project using `git clone git@github.com:Stranger825/honeypot.git`
- Run `cd honeypot`
- Run `chmod a+x install.sh`
- Run `sudo ./install.sh`


- In terminal 1, run the Logs webserver:
    - Run `cd logsserver`
    - Run `python3 logswebsite.py`

- In terminal 2, run the dummy server:
    - Run `cd httphoneypot`
    - Run `python3 -m http.server 80`

- In terminal 3, run `sudo -E python3.8 -m honeypots --setup <SERVICE1,SERVICE2,SERVICE3> --config config.json`
- Stop the above process whenever you feel like.

- Start the monitoring process daemon for the script `monitor.py`



# Things left to do

- Write an analysis script to detect anomaly.