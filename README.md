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



### Precautions
* Ensure the ENTIRE installment is done on ONE terminal/session/tab. 
* Ensure the following ports are not being used or blocked by firewall rules: 443, 5601, 55000, 9200, 1514/1515, 514
* Ensure the `wazuh-certificates.tar` file is present with the installer files - this is needed to assign and verify certificated for security
* Ensure credentials and config files are updated accordingly
## Component/features Breakdown

### wazuh-indexer 
* The Wazuh Indexer stores log and other security data aggregated from the user system and Wazuh API in JSON format.
* The Indexer is on the same wazuh_network as the other components and interacts with them to pass around, display, update, or delete  data
* The wazuh-manager forwards vulnerability data to the indexer using a [Filebeat](https://documentation.wazuh.com/current/user-manual/manager/indexer-integration.html#filebeat)  and [Wazuh indexer connector](https://documentation.wazuh.com/current/user-manual/manager/indexer-integration.html#wazuh-indexer-connector)
* Test indexer installation with the command ```curl -k -u admin https://<WAZUH_INDEXER_IP_ADDRESS>:9200```
### wazuh-manager
* The Wazuh Manager handles various responsibilites and actions central to the SIEM's performance such as forwarding data logs, rule management, alerting, and more and is closely connected to the Wazuh Indexer
* Check wazuh-manager configuration by viewing and editing the file at ```/var/ossec/etc/ossec.conf``` 
* Sample excerpts from Wazuh-Manager configs: 
``` 
   <remote>
    <connection>secure</connection>
    <port>1514</port>
    <protocol>tcp</protocol>
    <queue_size>131072</queue_size>
  </remote>
```
Setting Wazuh-Manager port and queue size

```
<cluster>
    <name>wazuh</name>
    <node_name>node01</node_name>
    <node_type>master</node_type>
    <key>aa093264ef885029653eea20dfcf51ae</key>
    <port>1516</port>
    <bind_addr>0.0.0.0</bind_addr>
    <nodes>
        <node>wazuh.manager</node>
    </nodes>
    <hidden>no</hidden>
    <disabled>yes</disabled>
  </cluster>
```
Setting Wazuh-Manager cluster bind addresses, node information, and more. 
### wazuh-dashboard
* The wazuh-dashboard is a user interface webpage that shows a more user-friendly visual representation of all things Wazuh, such as vulnerability data, agents running, access to tools and more
* The wazuh-dashboard aggregates data from the Wazuh Indexer, Wazuh Manager, and Wazuh Agents to create a full-fledges GUI for managing the platform 
* Access dashboard UI by typing in the URL on an browser ```https://<Your_IP>:port```. 
* You can check wazuh-dashboard configuration in ```/it610FinalProject/config/wazuh_dashboard/opensearch_dashboards.yml```
``` 
server.host: 0.0.0.0
server.port: 5601
opensearch.hosts: https://wazuh.indexer:9200
opensearch.ssl.verificationMode: certificate
opensearch.requestHeadersAllowlist: ["securitytenant","Authorization"]
opensearch_security.multitenancy.enabled: false
opensearch_security.readonly_mode.roles: ["kibana_read_only"]
server.ssl.enabled: true
server.ssl.key: "/usr/share/wazuh-dashboard/certs/wazuh-dashboard-key.pem"
server.ssl.certificate: "/usr/share/wazuh-dashboard/certs/wazuh-dashboard.pem"
opensearch.ssl.certificateAuthorities: ["/usr/share/wazuh-dashboard/certs/root-ca.pem"]
uiSettings.overrides.defaultRoute: /app/wz-home
# Session expiration settings
opensearch_security.cookie.ttl: 900000
opensearch_security.session.ttl: 900000
opensearch_security.session.keepalive: true
```
Sample Wazuh Dashboard configuration
### wazuh-agent
* The wazuh-agent(s) are programs that are attached to host devices that primarily report vulnerability data the the Wazuh indexers and utlimately the dashboard and managers. 
* The wazuh-agent(s) can be enrolled either manually via [Wazuh server API](https://documentation.wazuh.com/current/user-manual/agent/agent-enrollment/enrollment-methods/via-manager-API/index.html) or [automatically by agent configuration](https://documentation.wazuh.com/current/user-manual/agent/agent-enrollment/enrollment-methods/via-agent-configuration/index.html).  
* Can check agent status via Dashboard UI or API call ``` GET /agents/<WAZUH_AGENT_ID>/stats/agent ```. Can also check via running log scripts in ```/it610FinalProject/logs/getAgentComponentStats.py```

```  
{
 "data": {
        "affected_items": [
            {
                "buffer_enabled": true,
                "last_ack": "2025-12-05T04:17:31Z",
                "last_keepalive": "2025-12-05T04:17:29Z",
                "msg_buffer": 0,
                "msg_count": 0,
                "msg_sent": 128,
                "status": "connected"
            }
        ],
        "failed_items": [],
        "total_affected_items": 1,
        "total_failed_items": 0
    },
    "error": 0,
    "message": "Statistical information for each agent was successfully read"
}
```
Sample output showing Wazuh Agent status (found and online)
### config.yml
* This file gets created after running the Wazuh Installer from the installation scripts.
*  This file configures the node IP addresses for all the devices running each service (Indexer, Manager, Dashboard, etc). 

### wazuh-certificates.tar
* This .tar directory contains necessary certificates and secrets used to securely verify the authenticity and provide trust between all components in this project.
*  Make sure this is in the main project directory or anywhere services are run so the system can authenticate properly. 

### entrypoint.sh
* Install and start services manually by the binary files after checking for their existence  rather than systemd (for cases where systemd isn't working or isn't available).
*  Wazuh by default runs using systemctl which relies on systemd in Linux. 

## Project Difficulties/Pain Points

### SystemD Running on Manual Single-Container 
* In the midterm I tried running Wazuh manually using install scripts and that ended up failing due to Wazuh's manual installation 
needing SystemD to run which is absent in containers
### Excessive Load & Complexity on Single Container
* The project consists of multiple services (Dashboard, Indexer, Manager, Agent, etc) which cannot run on ONE container due to load issues
* Manual installations constantly ran into missing dependency and networking issues that were resolved in the official images and assisted installation
### Miscellaneous/Other Issues
* Alert indexing was not being sent to Dashboard UI either due to filebeat errors or some other error
* Often filepaths & names on system did not match what was on (old) documentation online, causing execution struggles

