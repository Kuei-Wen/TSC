import paramiko
import subprocess
import os

# --- SFTP Configuration ---
SFTP_HOSTNAME = "192.168.31.122"
SFTP_PORT = 22
SFTP_USERNAME = "pi"
SFTP_PASSWORD = "2doigxxi"  # For production, use key-based authentication
REMOTE_FILE_PATH = "/文件/*.dat"
LOCAL_FILE_PATH = os.path.join(os.getcwd(), "downloaded_file.dat")

# --- Program to Execute ---

def download_file_sftp():
    """
    Connects to an SFTP server and downloads a file.
    """
    transport = None
    sftp = None
    try:
        # Establish SFTP connection
        transport = paramiko.Transport((SFTP_HOSTNAME, SFTP_PORT))
        print(f"Connecting to {SFTP_HOSTNAME}...")
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Connection established.")

        # Download the file
        print(f"Downloading file from {REMOTE_FILE_PATH} to {LOCAL_FILE_PATH}...")
        sftp.get(REMOTE_FILE_PATH, LOCAL_FILE_PATH)
        print("File downloaded successfully.")
        return True

    except Exception as e:
        print(f"An error occurred during SFTP operation: {e}")
        return False

    finally:
        # Close the connection
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        print("Connection closed.")



if __name__ == "__main__":
    if download_file_sftp():
        # If the download was successful, execute the other program
        print("down load ok")
    else:
        print("Skipping program execution due to download failure.")
