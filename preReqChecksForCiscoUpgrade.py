from netmiko import ConnectHandler

# Device details
device = {
    'device_type': 'cisco_ios',
    'host': '10.10.20.181',  # Replace with your device's IP address
    'username': 'developer',    # Replace with your username
    'password': 'C1sco12345', # Replace with your password
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
    print("Connected to the device successfully!")

    # Get available space for IOS image
    space_command = 'dir flash:'  # You may adjust this command based on device configuration
    space_output = connection.send_command(space_command, expect_string=r'#', read_timeout=60)
    print("Available Space for IOS Image:")
    print(space_output)

    # Parse available space from the output
    available_space = None
    for line in space_output.splitlines():
        if 'bytes free' in line:
            available_space = line.split()[0]
            break

    if available_space:
        print(f"Available space: {available_space} bytes")
    else:
        print("Could not determine available space")

    # Get model
    model_command = 'show version | include Model'
    model_output = connection.send_command(model_command, expect_string=r'#', read_timeout=60)
    print("\nModel:")
    print(model_output)

    # Get IOS version
    ios_command = 'show version | include Version'
    ios_output = connection.send_command(ios_command, expect_string=r'#', read_timeout=60)
    print("\nIOS Version:")
    print(ios_output)

    # Extract the version number
    ios_version = None
    for line in ios_output.splitlines():
        if 'Version' in line:
            ios_version = line.split('Version')[1].split(',')[0].strip()
            break

    if ios_version:
        print(f"IOS Version: {ios_version}")
    else:
        print("Could not determine IOS version")

    # Check conditions and take actions
    if ios_version == '17.15.01' and '6164324352' in available_space:
        image_check_command = 'dir flash: | include image_name.txt'  # Replace <image_name> with the actual image name
        image_check_output = connection.send_command(image_check_command, expect_string=r'#', read_timeout=60)
        
        if 'image_name.txt' in image_check_output:  # Replace <image_name> with the actual image name
            print("Already present")
        else:
            # Upload the image to flash (this is a placeholder, actual upload logic will depend on your setup)
            connection.send_command('copy tftp:image_name.txt flash:image_name.txt', expect_string=r'#', read_timeout=300)  # Example command, adjust as needed
            print("Successfully uploaded")
    else:
        print("Version is not 17.15.01 or need to make space")

    connection.disconnect()

except Exception as e:
    print(f"An error occurred: {e}")
