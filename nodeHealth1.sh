#!/bin/bash

# Set the threshold for CPU utilization
threshold=90

# Run top command and filter the output for process names
process_lines=$(top -b -n 1 | grep -E 'fwk[0-9]+_dev_0')

# Extract process names and their CPU utilization percentages
while read -r line; do
    process_name=$(echo "$line" | awk '{print $12}') #Process name is in the 12th column
    cpu_utilization=$(echo "$line" | awk '{print $9}')

    #Check if CPU utilization exceeds the threshold
    if (( $(echo "$cpu_utilization > $threshold" | bc -l) )); then
        # Send an email alert using an external SMTP server
        subject="High CPU utilization for $process_name"
        body="The CPU utilization for $process_name is $cpu_utilization% (threshold: $threshld%)"
        recipient="yourMail@example.com"
    
        #Send mail
        echo -e "Subject:$subject\n$body" | sendmail -f "sender@example.com" "$recipient"
        echo "Alert email sent to $recipient."
    else
        echo "CPU utilization for $process_name is within the threshold."
    fi
done <<< "$process_lines"