import paramiko
import time
import sys
import re

host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

#Prechecks commands
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
    DEVICE_ACCESS.send(b'set clienv rows 0\n')
    DEVICE_ACCESS.send(b'show virtual-system all\n')
    time.sleep(0.5)
    output = (DEVICE_ACCESS.recv(65000).decode('ascii'))
    vsx_match = re.findall(r'^\d+', output, flags=re.MULTILINE)
    #print(vsx_match)

    # Convert the extracted strings to integers
    vs_id = [int(num) for num in vsx_match]
    #print(vs_id)

    # Create and open the output file
    filename = "vsxBackUp.txt"
    with open(filename, "w") as file:
        pass  # Placeholder; we'll add data in the next step

    for id in vs_id:
        DEVICE_ACCESS.send(f'set virtual-system {id}\n')
        time.sleep(0.5)
        for cmd in commands:
            DEVICE_ACCESS.send(f'{cmd}\n')
            time.sleep(0.5)
            output = DEVICE_ACCESS.recv(65000)
            print(output.decode(), end='')

            # Write the output to the file
            with open(filename, "a") as file:
                file.write(output.decode())

    #Close the SSH connection
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