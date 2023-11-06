import json
import datetime
from twisted.protocols.ftp import FTPFactory, FTP
from twisted.cred.portal import Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.internet import reactor
from twisted.python import log

log.startLogging(open("ftp_traffic.log", "a"))

class FTPLoggingProtocol(FTP):
    def connectionMade(self):
        self.log_entry("Connection established")

    def connectionLost(self, reason):
        self.log_entry("Connection lost")

    def lineReceived(self, line):
        command, _, args = line.partition(" ")
        self.log_entry("Command", command=command, args=args)

    def log_entry(self, event, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = self.transport.getPeer().host
        user = self.avatar.username if self.avatar else "Anonymous"

        entry = {
            "timestamp": timestamp,
            "IP": client_ip,
            "User": user,
            "Event": event,
        }
        entry.update(kwargs)

        log.msg(json.dumps(entry))

def main():
    ftp_factory = FTPFactory()
    ftp_factory.protocol = FTPLoggingProtocol
    ftp_factory.allowAnonymous = False

    portal = Portal(SimpleRealm())
    checker = FilePasswordDB("authorized_users.txt")
    portal.registerChecker(checker)
    ftp_factory.portal = portal

    reactor.listenTCP(21, ftp_factory)
    reactor.run()

class SimpleRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], None, lambda: None

if __name__ == "__main__":
    main()
