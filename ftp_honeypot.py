from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
import logging
import os

cwd = os.getcwd()

# Configuration
ftp_dir = os.path.join(cwd, "Tempfiles")  # Replace with the directory you want to use
user_file = "authorized_users.txt"
log_file = "ftp_log.txt"

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

# Enable logging
logging.basicConfig(filename=log_file, level=logging.INFO)

# Start the FTP server
if __name__ == "__main__":
    from pyftpdlib.servers import FTPServer

    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()
