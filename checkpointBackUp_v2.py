import paramiko
import time
import sys
import logging

def connect_to_device(host, username, password):
    """
    Establish an SSH connection to the specified device.

    Args:
        host (str): IP address or hostname of the device.
        username (str): SSH username.
        password (str): SSH password.

    Returns:
        paramiko.SSHClient or None: Connected session or None if connection fails.
    """
    try:
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(host, username=username, password=password)
        return session
    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication Failed")
        return None
    except paramiko.ssh_exception.SSHException:
        print("SSH Error")
        return None
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("No valid connections")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def execute_commands(session, commands, filename):
    """
    Execute a list of commands on the connected device and save output to a file.

    Args:
        session (paramiko.SSHClient): Established SSH session.
        commands (list): List of commands to execute.
        filename (str): Name of the output file.
    """
    try:
        DEVICE_ACCESS = session.invoke_shell()

        with open(filename, "w") as file:
            pass  # Placeholder; we'll add data in the next step

        for cmd in commands:
            time.sleep(0.5)
            DEVICE_ACCESS.send(f"{cmd}\n")
            time.sleep(0.5)
            output = DEVICE_ACCESS.recv(65000)
            print(output.decode(), end='')

            # Write the output to the file
            with open(filename, "a") as file:
                file.write(output.decode())

        logging.info(f"Output saved to {filename}")
        #print(f"Output saved to {filename}")
    except AttributeError:
        print("Parsing Error, Please check the command")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to execute the script.

    Usage:
        python script.py <host> <username> <password>
    """
    if len(sys.argv) != 4:
        print("Usage: python script.py <host> <username> <password>")
        return

    host, username, password = sys.argv[1], sys.argv[2], sys.argv[3]
    commands = ["set clienv rows 0",
                "show configuration",
                "show bgp peers",
                "show bgp peers advertise",
                "save config"    
                ]
    filename = "checkpointBackUp.txt"

    # Set up logging
    logging.basicConfig(filename="checkpointBackUp.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    session = connect_to_device(host, username, password)
    if session:
        logging.info(f"{username} : Successfully connected to the device.")
        execute_commands(session, commands, filename)
        session.close()
        #logging.info("Successfully connected to the device.")
    else:
        print("Unable to connect to the Device")

if __name__ == "__main__":
    main()
