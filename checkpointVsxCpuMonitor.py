import paramiko
import time
import re
import mysql.connector
import logging

def establish_ssh_connection(hostname, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=22, username=username, password=password)
        return client
    except paramiko.AuthenticationException:
        logging.error(f"{username} : Authentication failed. Check your credentials.")
    except paramiko.SSHException as e:
        logging.error(f"SSH error: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

def get_expert_shell(client, expertpwd):
    shell = client.invoke_shell()
    shell.send('lock database override\n')
    shell.send('expert\n')

    timeout = 10
    while timeout > 0:
        askPwd = shell.recv(4096).decode()
        if 'Password:' in askPwd or 'Enter expert password:' in askPwd:
            break
        time.sleep(1)
        timeout -= 1

    if timeout == 0:
        logging.error("Timed out waiting for prompt.")
        return None

    shell.send(expertpwd + '\n')
    return shell

def extract_cpu_data(output):
    process_pattern = r"fwk\d+_dev"
    cpu_dict = {}

    lines = output.strip().split("\n")
    for line in lines:
        if re.search(process_pattern, line):
            fields = line.split()
            process_name = fields[-1]
            cpu_percent = float(fields[8])  # Assuming %CPU is the 9th field
            cpu_dict[process_name] = cpu_percent

    return cpu_dict

def insert_or_update_data(cpu_dict, db_host, db_user, db_password, db_name):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cpu_data (
                process_name VARCHAR(255) PRIMARY KEY,
                cpu_percent REAL
            )
        """)

        for process_name, cpu_percent in cpu_dict.items():
            cursor.execute("""
                INSERT INTO cpu_data (process_name, cpu_percent)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE cpu_percent = VALUES(cpu_percent)
            """, (process_name, cpu_percent))

        conn.commit()
        logging.info("Data inserted or updated successfully!")
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()

def main():
    hostname = "192.168.9.100"
    username = "admin"
    password = "Raje@4590"
    expertpwd = "W!11P0wer"

    #logging.basicConfig(level=logging.INFO)

    #Set up logging to a text file.
    log_file = "checkpointVsxCpuMonitor.log"
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    client = establish_ssh_connection(hostname, username, password)
    if client:
        logging.info(f"{username} : Successfully connected to the device.")
        shell = get_expert_shell(client, expertpwd)
        if shell:
            shell.send("top -b -n 1\n")
            time.sleep(0.5)
            output = shell.recv(4096).decode()
            print(output)
            cpu_dict = extract_cpu_data(output)
            print(cpu_dict)
            client.close()

            insert_or_update_data(cpu_dict, 'localhost', 'root', 'Raje@4590', 'my_database')

if __name__ == "__main__":
    main()
