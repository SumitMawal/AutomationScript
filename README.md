# AutomationScript

“Before deploying the script in production environments, it is essential to thoroughly test it in a LAB environment.”

**checkpointBackUp_v2.py:** 

“This Python script is designed to create a backup of a Checkpoint firewall. It retrieves the configuration using the ‘show configuration’ command and saves it to a local text file.”

**checkpointPrePostChecks_v2.py:** 

“This Python script performs health checks on a Checkpoint firewall. It captures relevant output and saves it locally in a text file. Typically, you would use this script before and after significant Checkpoint-related activities, such as upgrades, to compare pre- and post-conditions and ensure everything is functioning correctly.”

**checkpointVsxBackUp_v2.py:**

“This Python script is designed to create a backup of a VSX Checkpoint firewall (multi-tenancy). It retrieves the configuration using the ‘show configuration’ command and saves it to a local text file. By running this script, you can enter each VSYS context and execute the ‘show configuration’ command, with the output being saved in a local text file.”

**checkpointVsxCpuMonitor.py:**

“With this Python script, we can retrieve the CPU utilization of an individual VSYS (Virtual System) on a VSX Check Point firewall and store it in a database. This allows us to represent the VSYS-wise CPU usage in graphical format or monitor it for each VSYS. When using dynamic core allocation to VSYS, SNMP monitoring alone can be challenging for individual VSYS CPU utilization. The script collects CPU usage data for each VSYS and stores it, enabling you to retrieve and analyze the data as needed. Additionally, instead of storing the data in a database, you can compare VSYS CPU utilization against a threshold and set up alerts (such as email notifications) if a mail server is configured in the Check Point firewall.”
