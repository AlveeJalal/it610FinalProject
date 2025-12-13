# it610FinalProject

## Introduction
This project is meant to install, configure, and run an instance of the Wazuh SIEM (Security Information and Event Management) software. The Wazuh SIEM is a tool used to monitor activity on systems to ultimately assist with cyber security efforts(Incident response, prevention, recovery, etc). The midterm intention was to run Wazuh SIEM on a single container. However it was ultimately discovered that Wazuh cannot run this way due to its multi-service architecture requiring multiple containers. It was then run on the host as per Professor's directions. This FINAL project however separates the Wazuh components into multiple containers on the same network using docker-compose for better load balancing and separation of concerns. This documentation explains the process, background, and other "need to know" information on running a mult-container pre-packaged Wazuh SIEM project on any device using docker-compose.

### What is Wazuh?
Wazuh is a Security Information And Event Management(SIEM) System used to monitor a system's security. Wazuh constantly scans for threats and aggregates findings to a log. Wazuh provides data to display to users and possible mitigation solutions. Wazuh's Agent system can monitor activity and flag any concerns for the user to examine and escalate. This a great and free tool to use, and it is a great software to demonstrate containerization and systems administration on because of its flexible configuration. 

### Prerequisites
* OS: Linux(Either Native, Virtualized, or WSL2) Preferred with **ROOT** access, as this was tested on WSL2 Ubuntu(Debian). Possible on Windows with PowerShell(anything with a terminal)
* Software: Docker Desktop with a DockerHub account. Access to GitHub with an account, Git, and possibly SSH keys to pull from this [repository](https://github.com/AlveeJalal/it610FinalProject). 
* Browser access with ports 443, 5601, 55000, 9200, 1514/1515, 514 unblocked
 
## Setting up & Running the Software Package


### Environment Setup
Always ensure your environment is up to date with the latest software to minimize interruption during Wazuh setup
```
    sudo apt-get update
    sudo apt-get upgrade
```

Secure Credentials - Create a .env file (if not existing) and enter your new credentials that will be created upon running and starting the image container. Use the following format in the .env file:
```
WAZUH_USER = username
WAZUH_PASSWORD = password
INDEXER_USERNAME= username
INDEXER_PASSWORD= password
API_USERNAME = username
API_PASSWORD= password
API_JWT = jwt
```

### Initialization and Execution
Have a project directory where you will clone and run the software. Become root and clone the repository from GitHub into your local machine, setup necessary variables and ports, and run the services using docker-compose.  The container successfully running means the software was successfully pulled and started
```
    su -
    git clone git@github.com:AlveeJalal/it610FinalProject.git
    docker-compose up -d
```
You can also go into the bash shell to use the container environment:
```     docker exec -it <Custom Container Name> bash ```

Ensure to give yourself ownership & permissions to read/write/execute to the entire project recursively including current and subdirectories
``` chown -R alvee .
    chmod 744 . 
```
Become root and Change directory (CD) into the ```/it610FinalProject/config```  directory to access the config files for the Indexer & Dashboard in the ```wazuh_dashboard``` & ```wazuh_indexer``` subdirectories to ensure network.host(can be 0.0.0.0), node.name, cluster.name, are correct 
to your liking
Example configuration for wazuh.indexer.yml. Feel free to copy:
```
network.host: "0.0.0.0"
node.name: "wazuh.indexer"
cluster.name: "wazuh-cluster"
path.data: /var/lib/wazuh-indexer
path.logs: /var/log/wazuh-indexer
discovery.type: single-node
http.port: 9200-9299
transport.tcp.port: 9300-9399
```

Access Wazuh on your browser using your set IP(Can be Host, VM, or Localhost IP) and port number(typically 443) for the dashboard  with the URL: ``` https://<Your_IP>:port ```
<img width="1918" height="1198" alt="wazuh_dashboard_startup" src="https://github.com/user-attachments/assets/f635b5d7-d535-4a6e-b01c-23ff13c3df3b" />
Dashboard should look like the above

## Running on Host OS
### Environment Setup
### Keeping Services Persistent

If using WSL2, create a script and have it run on startup. Make sure it is executable
```
sudo vi /etc/wsl.conf
```
Add this line ``` command="bash /usr/local/bin/wazuh-startup.sh" ```

Create the script
``` sudo nano /usr/local/bin/wazuh-startup.sh ```
The script will run the services on startup
```
#!/bin/bash
# Wait a few seconds for networking to stabilize
sleep 5

# Start all Wazuh services
systemctl start wazuh-indexer
systemctl start wazuh-manager
systemctl start wazuh-dashboard

```



### Precautions
* Ensure the ENTIRE installment is done on ONE terminal/session/tab. 
* Ensure the following ports are not being used or blocked by firewall rules: 443, 5601, 55000, 9200, 1514/1515, 514
* Ensure the `wazuh-certificates.tar` file is present with the installer files - this is needed to assign and verify certificated for security
* Ensure credentials and config files are updated accordingly
## Component/features Breakdown

### indexer_starter.sh,  server_starter.sh,  dashboard_starter.sh 
Scripts to install, setup & run the Wazuh Indexer, manager & dashboard Generates config files, creates and sets a node, & initialized cluster security/certification script. Overwrites existing installations.

### config.yml
This file gets created after running the Wazuh Installer from the installation scripts. This file configures the node IP addresses for all the devices running each service (Indexer, Manager, Dashboard, etc). 

### wazuh-certificates.tar
This .tar directory contains necessary certificates and secrets used to securely verify the authenticity and provide trust between all components in this project. Make sure this is in the main project directory or anywhere services are run so the system can authenticate properly. 

### entrypoint.sh
Install and start services manually by the binary files after checking for their existence  rather than systemd (for cases where systemd isn't working or isn't available). Wazuh by default runs using systemctl which relies on systemd in Linux. 


