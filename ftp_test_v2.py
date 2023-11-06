import json
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
import logging
import os
import datetime

cwd = os.getcwd()

# Configuration
ftp_dir = os.path.join(cwd, "Tempfiles")  # Replace with the directory you want to use
user_file = "authorized_users.txt"
log_file = "ftp_log.json"

# Create an authorizer with authorized users
authorizer = DummyAuthorizer()
try:
    with open(user_file, "r") as users:
        for line in users:
            username, password = line.strip().split(",")
            authorizer.add_user(username, password, ftp_dir, perm="elradfmw")
except FileNotFoundError:
    print(f"User file '{user_file}' not found. No authorized users set up.")

# Define an anonymous user
authorizer.add_anonymous(ftp_dir)

# Create an FTP handler
handler = FTPHandler
handler.authorizer = authorizer

# Create a logger and configure it with a custom JSON formatter
log_format = {
    'event': '%(message)s',
    'client_info': '%(client_info)s',
    'other_info': '%(other_info)s',
    'timestamp': '%(asctime)s',
}
json_formatter = logging.Formatter(json.dumps(log_format))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configure the logger to write to the JSON file
log_handler = logging.FileHandler(log_file)
log_handler.setFormatter(json_formatter)
logger.addHandler(log_handler)

# Define a function to handle FTP commands
def handle_ftp_command(client, command, arguments):
    """Handles an FTP command and logs the event."""

    client_info = {"client_ip": client.getpeername()[0], "command": command, "arguments": arguments}
    other_info = {}
    log_event = {
        "event": "command",
        "client_info": client_info,
        "other_info": other_info,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Log the event
    logger.info(json.dumps(log_event))
    
    # Handle the command
    handler.handle_command(client, command, arguments)

# Start the FTP server
if __name__ == "__main__":
    from pyftpdlib.servers import FTPServer

    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

# The log entries will be written to the JSON file in the specified format.
