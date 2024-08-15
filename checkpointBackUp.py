import paramiko
import time
import sys

host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

#Commands for backup and to save the config
commands = ["set clienv rows 0",
            "show configuration",
            "show bgp peers",
            "show bgp peers advertise",
            "save config"
           ]

# Connect to the firewall
session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    session.connect(host,
                    username=username,
                    password=password
                   )

    DEVICE_ACCESS = session.invoke_shell()

    # Create and open the output file
    filename = "backUp.txt"
    with open(filename, "w") as file:
        pass  # Placeholder; we'll add data in the next step

    for cmd in commands:
        DEVICE_ACCESS.send(f'{cmd}\n')
        time.sleep(0.5)
        output = DEVICE_ACCESS.recv(65000)
        print(output.decode(), end='')

        # Write the output to the file
        with open(filename, "a") as file:
            file.write(output.decode())

    # Close the SSH connection
    #session.close()

except paramiko.ssh_exception.AuthenticationException:
    print("Authentication Failed")

except AttributeError:
    print("Parsing Error, Please check the command")

except:
    print("Unable to connect to the Device")

finally:
    # Close the SSH connection
    session.close()