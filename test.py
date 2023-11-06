print('hello')
from honeypots.honeypots import QSSHServer


print('hello')
qsshserver = QSSHServer(port=9999)
qsshserver.run_server(process=True)
qsshserver.test_server(port=9999)
# INFO:chameleonlogger:['servers', {'status': 'success', 'username': 'test', 'src_ip': '127.0.0.1', 'server': 'ssh_server', 'action': 'login', 'password': 'test', 'src_port': 38696}]
qsshserver.kill_server()