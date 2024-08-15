import paramiko
import time
import sys
import re
import logging

def connect_to_firewall(host, username, password):
    """
    Establish an SSH connection to the firewall.

    Args:
        host (str): Firewall IP address or hostname.
        username (str): SSH username.
        password (str): SSH password.

    Returns:
        paramiko.SSHClient or None: Established SSH session or None if connection failed.
    """
    try:
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(host, username=username, password=password)
        return session
    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Failed")
        return None
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH Error: {e}")
        return None
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Unable to connect to the Device")
        return None

def execute_commands(session, commands):
    """
    Execute specified commands on the firewall.

    Args:
        session (paramiko.SSHClient): Established SSH session.
        commands (list): List of commands to execute.
    """
    DEVICE_ACCESS = session.invoke_shell()
    DEVICE_ACCESS.send(b'set clienv rows 0\n')
    DEVICE_ACCESS.send(b'show virtual-system all\n')
    time.sleep(0.5)
    output = DEVICE_ACCESS.recv(65000).decode('ascii')
    vsx_match = re.findall(r'^\d+', output, flags=re.MULTILINE)
    vs_id = [int(num) for num in vsx_match]

    filename = "vsxBackUp.txt"
    with open(filename, "w") as file:
        pass

    for id in vs_id:
        DEVICE_ACCESS.send(f'set virtual-system {id}\n')
        time.sleep(0.5)
        for cmd in commands:
            DEVICE_ACCESS.send(f'{cmd}\n')
            time.sleep(0.5)
            output = DEVICE_ACCESS.recv(65000)
            print(output.decode(), end='')

            with open(filename, "a") as file:
                file.write(output.decode())

    session.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <host> <username> <password>")
        sys.exit(1)

    host, username, password = sys.argv[1], sys.argv[2], sys.argv[3]
    commands = [
        "show configuration",
        "show bgp peers",
        "show bgp peers advertise",
        "save config"
    ]

    # Set up logging
    logging.basicConfig(filename="firewall_backup.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    session = connect_to_firewall(host, username, password)
    if session:
        execute_commands(session, commands)
        logging.info(f"{username} : Backup completed successfully.")
    else:
        logging.error("Backup failed due to connection issues.")
