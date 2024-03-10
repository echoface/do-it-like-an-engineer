# setup xrdp on ubuntu machine

## server
```
--------------------------------------------
Xrdp Server (Remote Desktop) Installation:
--------------------------------------------

Tested in Ubuntu 22.04.03 LTS

1. Update Environment

$ sudo apt-get update
$ sudo apt-get upgrade

2. Install XRDP

$ sudo apt install xrdp

3. Check status of XRDP: ( XRDP runs automatically after installation)

$ sudo systemctl status xrdp


4. add the xrdp user to the ssl-cert group

$ sudo adduser xrdp ssl-cert

5. Restart xrdp service:

$ sudo systemctl restart xrdp

6. Configuring Firewall
Xrdp daemon listens on port 3389. You must open the Xrdp port if your Ubuntu server is protected by a firewall.

$ sudo ufw allow from 192.168.33.0/24 to any port 3389

here, replace given with with your computer ip. (check by $ ip a )

$ sudo ufw allow 3389

--------------------------------
Connecting to the Xrdp Server
-------------------------------
The default RDP client is accessible if you have a Windows PC.
Enter "remote" in the Windows search box and click on "Remote Desktop Connection".
The RDP client will open as a result.
Enter the IP address of the remote server in the "Computer" field and click "Connect".

On the login screen, enter your username and password before clicking on “OK.”



---------------------------------
Xrdp Configuration : FOR UNDERSTANDING ONLY
---------------------------------
The directory /etc/xrdp contains the Xrdp configuration files. You do not need to modify the configuration files for simple Xrdp connections.

Xrdp uses the default X Window desktop environment (Gnome or XFCE).

xrdp.ini is the main configuration file. This file is divided into sections and lets you set global configuration settings such as security and listening addresses, as well as create separate Xrdp login sessions.

You must restart the Xrdp service after making any configuration file changes.

To start an X session, Xrdp uses the startwm.sh file. Edit this file if you want to use a different X Window desktop.



-----------------------------------------
IMPORTANT: Multi User Setup Configuration
-----------------------------------------
1. Install D-BUS

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install dbus-x11


2. modify your /etc/xrdp/startwm.sh file

$ sudo nano /etc/xrdp/startwm.sh

At the below line before this line test -x /etc/X11/Xsession && exec /etc/X11/Xsession.

ADD THESE LINES

export $(dbus-launch)

Then save the file.

3. Restart the System:

$ sudo reboot



----------------------
REFERENCES:
----------------------
https://vegastack.com/tutorials/how-to-install-xrdp-server-on-ubuntu-22-04/
https://devicetests.com/fix-xrdp-login-blank-screen-issues
https://bonguides.com/black-screen-remote-desktop-to-ubuntu-from-windows-with-xrdp/
http://c-nergy.be/blog/?p=12043
```


### remove anoying `thinclient_drives`
```bash

This is a good way for me:

edit the /etc/xrdp/sesman.ini

# comment this line: L122
#FuseMountName=thinclient_drives

# and uncomment this line: L120
FuseMountName=/run/user/%u/thinclient_drives
```
