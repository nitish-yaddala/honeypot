import logging
from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
import socket, json, datetime, csv
from twisted.protocols.ftp import FTPFactory, FTP
from twisted.cred.portal import Portal

# Global variable to store the listening ports
listening_ports = {}


class FTPRealm:
    def __init__(self, root_directory):
        self.root_directory = root_directory

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IFTPShell in interfaces:
            avatar = FTP()
            avatar.root_directory = self.root_directory
            return IFTPShell, avatar, lambda: None
        raise NotImplementedError("Only IFTPShell interface is supported.")


class HoneypotResource(resource.Resource):
    isLeaf = True

    allowedMethods = ["HEAD", "GET"]  # Allow both HEAD and GET methods

    def __init__(self, port):
        self.port = port

    def render(self, request):
        client_ip = request.getClientAddress().host
        actual_port = self.port

        if actual_port == 80:
            return self.handle_http_request(request, client_ip, actual_port)
        elif actual_port == 21:
            return self.handle_ftp_request(request, client_ip, actual_port)
        else:
            # Handle other ports here or respond with 404
            request.setResponseCode(404)
            return b""

    def handle_http_request(self, request, client_ip, actual_port):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_params = request.args
        cookies = request.received_cookies
        payload = request.content.read() if request.method == b"POST" else None

        log_entry = {
            "timestamp": timestamp,
            "IP": client_ip,
            "Port": actual_port,
            "Method": request.method.decode("utf-8"),
            "URI": request.uri.decode("utf-8"),
            "Headers": dict(
                (key.decode("utf-8"), value.decode("utf-8"))
                for key, value in request.getAllHeaders().items()
            ),
            "QueryParams": dict(
                (key.decode("utf-8"), [value.decode("utf-8") for value in values])
                for key, values in query_params.items()
            ),
            "Cookies": dict(
                (key.decode("utf-8"), value.decode("utf-8"))
                for key, value in cookies.items()
            ),
            "Payload": payload.decode("utf-8") if payload is not None else None,
        }

        self.log_entry(log_entry, "honeypot_log_http.json")

        request.setResponseCode(404)
        return b""

    def handle_ftp_request(self, request, client_ip, actual_port):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gather relevant FTP information
        ftp_command = request.command.decode("utf-8")
        ftp_args = request.args.decode("utf-8")
        user = request.client_username.decode("utf-8")
        password = request.client_password.decode("utf-8")

        # Retrieve authorized user credentials from the FTP factory
        authorized_user = self.factory.authorized_user

        log_entry = {
            "timestamp": timestamp,
            "IP": client_ip,
            "Port": actual_port,
            "FTP_Command": ftp_command,
            "FTP_Args": ftp_args,
            "User": user,
            "Password": password,
        }

        # Log the FTP entry
        self.log_entry(log_entry, "honeypot_log_ftp.json")

        if (
            user == authorized_user["username"]
            and password == authorized_user["password"]
        ):
            print(f"Authorized FTP user logged in: {user}")
            request.setResponseCode(230)
        else:
            print("Unauthorized FTP login attempt.")
            request.setResponseCode(530)
        request.finish()

    def log_entry(self, log_entry, json_filename):
        with open(json_filename, "a") as json_file:
            json.dump(log_entry, json_file, indent=4)
            json_file.write("\n\n")


class HoneypotFTP(FTP):
    def connectionMade(self):
        self.sendLine("220 Welcome to My FTP Server")
        FTP.connectionMade(self)


def is_port_open(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set a timeout for the connection attempt
            s.bind(("0.0.0.0", port))
            return True  # Port is available
    except (OSError, socket.timeout):
        return False  # Port is already in use


def start_honeypot(port):
    if is_port_open(port):
        if port in listening_ports:
            print(f"Honeypot is already running on port {port}.")
        else:
            if port == 80:
                honeypot_resource = HoneypotResource(port)
                site = server.Site(honeypot_resource)
                listening_ports[port] = reactor.listenTCP(port, site)
                print(f"HTTP Honeypot started on port {port}...")
            elif port == 21:
                # Define authorized user credentials for FTP here
                authorized_user = {
                    "username": "username",  # Replace with the desired username
                    "password": "password",  # Replace with the desired password
                }

                honeypot_resource = HoneypotResource(port)
                ftp_factory = FTPFactory()
                ftp_factory.protocol = HoneypotFTP
                ftp_factory.welcomeMessage = "Welcome to the FTP server"
                ftp_factory.allowAnonymous = True
                ftp_factory.permitAnonymous = True
                ftp_factory.authorized_user = (
                    authorized_user  # Pass the authorized user
                )

                root_directory = "C:/Users/ynikki/OneDrive/Desktop/Honeypot+/Tempfiles"
                ftp_realm = FTPRealm(root_directory)
                ftp_factory.portal = Portal(ftp_realm)
                ftp_factory.protocol.portal = ftp_factory.portal

                listening_ports[port] = reactor.listenTCP(port, ftp_factory)
                print(f"FTP Honeypot started on port {port} with authorized user.")
            else:
                print(f"Port {port} is not configured for a dummy service.")
    else:
        print(f"Port {port} is already in use. Please choose a different port.")


def stop_honeypot(port):
    if port in listening_ports:
        listening_ports[port].stopListening()
        del listening_ports[port]
        print(f"Honeypot on port {port} stopped.")
    else:
        print(f"Honeypot on port {port} is not running.")


def menu():
    while True:
        print("Honeypot Menu:")
        print("1. Start Honeypot on a Port")
        print("2. Stop Honeypot on a Port")
        print("3. List Running Honeypots")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            try:
                port = int(input("Enter the port number to start the honeypot: "))
                start_honeypot(port)
            except ValueError:
                print("Invalid port number. Please enter a valid integer.")
        elif choice == "2":
            try:
                port = int(input("Enter the port number to stop the honeypot: "))
                stop_honeypot(port)
            except ValueError:
                print("Invalid port number. Please enter a valid integer.")
        elif choice == "3":
            if len(listening_ports) == 0:
                print("No Running Ports on Honeyport")
            else:
                print("Running Honeypots:")
                for port in listening_ports:
                    print(f"Port {port}: Running")
        elif choice == "4":
            for port in listening_ports.copy():
                stop_honeypot(port)
            reactor.stop()
            break
        else:
            print("Invalid choice. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    deferToThread(menu)
    reactor.run()
