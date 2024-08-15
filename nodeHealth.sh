#!/bin/bash

# Set the process name and threshold
process_name="fwk3_dev_0"
threshold=90

# Run top command and filter the output for the process
top_output=$(top -b -n 1)
process_lines=$ (echo "$top_output" | grep "$process_name")

# Extract the CPU utilization percentage
if [ -n "$process_lines" ]; then
    cpu_utilization=$(echo "$process_lines" | awk '{print $9}')
else
    echo "No process named $process_name found in top output."
    exit 1
fi

#Check if CPU utilization exceeds the threshold
if (( $(echo "$cpu_utilization > $threshold" | bc -l) )); then
    # Send an email alert
    subject="High CPU utilization for $process_name"
    body="The CPU utilization for $process_name is $cpu_utilization% (threshold: $threshld%)"
    recipient="yourMail@example.com"

    #Asuming you have a mail command available
    echo "$body" | mail -s "$subject" "$recipient"
    echo "Alert email sent to $recipient."
else
    echo "CPU utilization for $process_name is within the threshold."
fi