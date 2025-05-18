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
A simple Python-based clipboard sync tool between a Windows PC and a Linux laptop over the same network.
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
## ⚙️ Setup
### 0. Update IP addresses
0. In `server-linux.py` (Linux), set the correct IP of your Windows PC:
```python
WINDOWS_CLIENT_IP = "192.168.x.x"
```
- **Note:** Use `ipconfig` on Windows to find your correct IP address.
1. in `client-windows.py` (Windows), set the correct IP of your Linux PC:
```python
SERVER_IP = "192.168.x.x"
```
- **Note:** Use `ifconfig` on Linux to find your correct IP address.
### 1. Define Firewall Rules for TCP/65433
#### 1.1: Using GUI
To ensure your Linux server can send data to your Windows clipboard sync client, you need to allow incoming connections on a specific TCP port (e.g., `65433`) in Windows Firewall.
0. `WIN+R => wf.msc => Inbound Rules => New Rule `
	1. Define Allow Rule for Port TCP/65433 
- OR You Can use Powershell
#### 1.2: Using Powershell:
0. **Open PowerShell as Administrator**
   - Press `Win + S`, search for `PowerShell`
   - Right-click and choose **Run as Administrator**
0. **Run the Following Command**:
```powershell
New-NetFirewallRule -DisplayName "Allow Clipboard Sync" `
                    -Direction Inbound `
                    -LocalPort 65433 `
                    -Protocol TCP `
                    -Action Allow
```
3. **Verify the Rule**
	- Open **Windows Defender Firewall with Advanced Security**
	- Go to **Inbound Rules**
	- Look for the rule named **"Allow Clipboard Sync"**
- ### 🛠 Notes
	- You can change `65433` to any other port number if needed — just make sure it matches your Python script.
	- Make sure your Windows machine has a **private or trusted network** profile.
	- No restart is needed; the rule applies immediately.
	- This rule only opens **TCP** traffic on port `65433`.
#### To Delete the Rule Later (Optional)
If you want to remove this rule, run:
```powershell
Remove-NetFirewallRule -DisplayName "Allow Clipboard Sync"
```
- By completing this step, your Windows system is ready to **receive clipboard data from your Linux machine** over the network.
### 2. Install Requirements 
- Install `Python 3.12` on both Windows and Linux
- then on **Windows** open Powershell as Administrator:
```powershell
python -m pip install pyperclip
python -m pip install keyboard
```
- and on **Linux**:
```sh
sudo pip install pyperclip
sudo pip install keyboard
```
- **Note:** keyboard need to install with root access(sudo)
### 3. Run Script
0. On Linux run Server side:
```sh
sudo python3 linux-server.py
```
0. then On Windows open Powershell as Administrator and run Client:
```powershell
python windows-client.py
```
- **Enjoy Script** 😊 
