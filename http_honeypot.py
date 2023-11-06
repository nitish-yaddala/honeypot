from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
import socket, json, datetime, csv
from twisted.cred.portal import Portal


# Global variable to store the listening ports
listening_ports = {}

class HoneypotResource(resource.Resource):
    isLeaf = True
    print("got here 1")

    allowedMethods = ["HEAD", "GET"]  # Allow both HEAD and GET methods

    def __init__(self, port):
        self.port = port

    def render(self, request):
        client_ip = request.getClientAddress().host
        actual_port = self.port

        if actual_port == 80:
            return self.handle_http_request(request, client_ip, actual_port)
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
    
    def log_entry(self, log_entry, json_filename):
        with open(json_filename, "a") as json_file:
            json.dump(log_entry, json_file, indent=4)
            json_file.write("\n\n")


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
