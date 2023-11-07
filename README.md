# Steps to Run

- Run `chmod a+x install.sh`
- Run `sudo ./install.sh`
- To run the Logs webserver:
    - Run `cd deploy-server`
    - Run `python3 logswebsite.py`
- Then run the dummy server:
    - Run `cd dummyserver`
    - Run `python3 -m http.server 80`

- Start the monitoring process daemon for the script `monitor.py`

- Then run `sudo -E python3.8 -m honeypots --setup <SERVICE1,SERVICE2,SERVICE3> --config config.json`



# Things left to do

- Write a proper configuration for all the services (FTP, SSH, TELNET).
- 