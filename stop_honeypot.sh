#!/bin/bash

# Stop all services

# Function to stop a service
stop_service() {
    service_name=$1
    echo "Stopping $service_name..."
    
    # Find all PIDs associated with the service excluding the current script
    pids=$(pgrep -f "$service_name" | grep -v $$)
    
    if [ -n "$pids" ]; then
        # Loop through each PID and kill the process
        for pid in $pids; do
            sudo kill "$pid"
            echo "Process with PID $pid for $service_name has been stopped."
        done
    fi
}

# Stop Logs Website
stop_service "logswebsite.py"

# Stop Honeypot Services
stop_service "python3 -m honeypots"

# Stop HTTP Honeypot
stop_service "python3 -m http.server"

# Stop Monitor
stop_service "monitor.py"