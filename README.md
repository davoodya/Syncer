# SyncerMan

SyncerMan is a powerful, cross-platform synchronization tool designed to bridge the gap between Windows and Linux environments. It enables real-time, bi-directional sharing of clipboard content, text messages, files, and directories over a local network using TCP sockets.

Built with Python, SyncerMan runs efficiently in the background, listening for global hotkeys to trigger instant data transfer without interrupting your workflow.

- [✨ Features](#%E2%9C%A8%20Features)
- [🧰 Requirements](#%F0%9F%A7%B0%20Requirements)
	- [Windows (Client)](#Windows%20(Client))
	- [Linux (Server)](#Linux%20(Server))
- [⚙️ Setup](#%E2%9A%99%EF%B8%8F%20Setup)
	- [0. Update IP addresses](#0.%20Update%20IP%20addresses)
	- [1. Define Firewall Rules for TCP/65433](#1.%20Define%20Firewall%20Rules%20for%20TCP/65433)
		- [1.1: Using GUI](#1.1:%20Using%20GUI)
		- [1.2: Using Powershell:](#1.2:%20Using%20Powershell:)
		- [To Delete the Rule Later (Optional)](#To%20Delete%20the%20Rule%20Later%20(Optional))
	- [2. Install Requirements](#2.%20Install%20Requirements)
	- [3. Run Script](#3.%20Run%20Script)

# Clipboard Syncer (Windows ↔ Linux)
A Python-based clipboard sync tool between a Windows PC and a Linux laptop over the same network.
## ✨ Features
- Send copied text from Windows **(using `Ctrl + Alt + C`)** to Linux:
  - Text gets appended to `PCRecieved.txt`
  - Also copied last received text into the Linux clipboard.
- Send clipboard content from Linux **(using `Ctrl + Shift + V`)** to Windows:
  - Text gets appended to `LinuxReceived.txt`
  - Also copied last received text into the Windows clipboard.

## 🧰 Requirements

### Windows (Client)
- Python 3.x
- Modules:
  - `pyperclip`
  - `keyboard`
### Linux (Server)
- Python 3.x
- Modules:
  - `pyperclip`
  - `keyboard`
- Note: **Linux side** Must **run with `sudo`** due to `keyboard` requiring root access permission.

## Setup and Run Syncer Man 

### 0. Install Requirements 
#### 0.1: Windows 
- Install `Python 3.12` on both Windows and Linux.
- Then, on **Windows**, open PowerShell as Administrator and run:

```powershell
python -m pip install pyperclip
python -m pip install keyboard
```

#### 0.2: Linux
- Install the following libraries:

```sh
sudo pip install pyperclip
sudo pip install keyboard
```

- **Note:** The `keyboard` package must be installed with root access (`sudo`).

### 1. Update IP addresses
0. In `server-linux.py` (Linux), set the correct IP address of your Windows PC:
```python
WINDOWS_CLIENT_IP = "192.168.x.x"
```
- **Note:** Use `ipconfig` on Windows to find your correct IP address.

1. In `client-windows.py` (Windows), set the correct IP address of your Linux PC:
```python
SERVER_IP = "192.168.x.x"
```
- **Note:** Use `ifconfig` (or `ip a`) on Linux to find your correct IP address.

### 2. Define Firewall Rules for TCP/65433

#### 2.1: Windows 

##### 2.1: Using GUI
To ensure your Linux server can send data to your Windows clipboard sync client, you need to allow incoming connections on a specific TCP port (e.g., `65433`) in Windows Firewall.

0. `WIN+R => wf.msc => Inbound Rules => New Rule`
	1. Define an Allow rule for TCP port `65433`.

- OR you can use PowerShell.

##### 2.2: Using Powershell:
0. **Open PowerShell as Administrator**
   - Press `Win + S`, search for `PowerShell`
   - Right-click and choose **Run as Administrator**

1. **Run the following command**:

```powershell
New-NetFirewallRule -DisplayName "Allow Clipboard Sync" `
                    -Direction Inbound `
                    -LocalPort 65433 `
                    -Protocol TCP `
                    -Action Allow
```

2. **Verify the rule**
	- Open **Windows Defender Firewall with Advanced Security**
	- Go to **Inbound Rules**
	- Look for the rule named **"Allow Clipboard Sync"**

- ### 🛠 Notes
	- You can change `65433` to any other port number if needed — just make sure it matches your Python script.
	- Make sure your Windows machine is using a **Private or Trusted network** profile.
	- No restart is needed; the rule applies immediately.
	- This rule only opens **TCP** traffic on port `65433`.
	
##### 2.3: Note: To Delete the Rule Later (Optional)
If you want to remove this rule, run:

```powershell
Remove-NetFirewallRule -DisplayName "Allow Clipboard Sync"
```

#### 2.4: Linux Debian Based 
- If your Linux system is not using a firewall, you can skip this step.  
- If a firewall is enabled, configure it according to your Linux distribution.

##### 2.4.0: Debian Based 
0. If you are using the `ufw` firewall, add the following command:

```sh
sudo ufw allow 65433/tcp comment 'Allow Clipboard Sync'
```

1. If you want to remove the rule after uninstalling the app, use the following command:

```sh
sudo ufw delete allow 65433/tcp
```

##### 2.4.1: RedHat Based 
0. Add the rule using `firewall-cmd`:

```sh
sudo firewall-cmd --permanent --add-port=65433/tcp
sudo firewall-cmd --reload
```

1. If you want to remove the rule after uninstalling the app, use the following command:

```sh
sudo firewall-cmd --permanent --remove-port=65433/tcp
sudo firewall-cmd --reload
```

- By completing this step, your Windows and Linux systems will be ready to **receive/send data** over the network.

### 3. Run Script
0. On Linux, run the server side:

```sh
sudo python3 linux-server.py
```

0. Then, on Windows, open PowerShell as Administrator and run the client:

```powershell
python windows-client.py
```

- Note: You can change the server and client execution locations. For example, you can run the server on Windows and the client on Linux. The choice is yours.


- **Enjoy Script** 😊 
