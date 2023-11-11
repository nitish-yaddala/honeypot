#!/bin/bash

# Get the current working directory
current_directory=$(pwd)

# Execute three Python files in separate terminals

# Terminal 1
gnome-terminal --title="Log Sever" --working-directory="$current_directory"/logserver -- bash -c "python3 '$current_directory'/logserver/logswebsite.py; exec bash"

# Prompt the user for services in Terminal 2
gnome-terminal --title="Honeypot Setup" -- bash -c 'echo "Enter the services separated by commas (e.g., SERVICE1,SERVICE2,SERVICE3):"; read services; sudo -E python3 -m honeypots --setup $services --config config.json; exec bash'

# Terminal 3
gnome-terminal --title="HTTP Honeypot"  --working-directory="$current_directory"/httphoneypot -- bash -c 'echo "Enter the port number for the HTTP service"; read port; sudo python3 -m http.server $port; exec bash'

# Terminal 4
gnome-terminal --title="Service Log Monitoring" --working-directory="$current_directory" -- bash -c "python3 monitor.py; exec bash"