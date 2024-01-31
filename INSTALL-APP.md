# OpenSpecimen & FAIR Data Point Setup Instructions 

The application can be installed either within the BIBBOX environment or as a stand-alone solution. Installation instructions can be found within the BIBBOX, followed by setup instructions required once the application has been successfully installed.

## Installation within the BIBBOX

Once you've selected the desired App for your BIBBOX instance, you can choose from the available versions, as shown in the following figure.

![Screenshot01](assets/OpenSpecimenFDP_install1.png)

Clicking "Install App" will open a new window, as illustrated in the following figure. Here, you can define the necessary entries. Some fields come pre-filled with suggested options, and if left unchanged, these default values will be used as the entries.

![Screenshot02](assets/OpenSpecimenFDP_install2.png)

After confirming by clicking "Install," the App will be installed as a BIBBOX instance. Once the installation is complete, you only need to follow a few steps to use the App for the first time, which are described below.

## Setup after BIBBOX or stand-alone installation


### Start OpenSpecimen

* Install the application from the FAIR Toolbox store
* Wait for the installation to finish
* After installation in FAIR Toolbox, Open Specimen will take some minutes to set up internally
* Start the application from the FAIR Toolbox application screen
* Log in to Open Specimen with default admin user "admin" and password "Login@123"

### Log in with the default credentials 
The default admin user name is "admin". The default admin password is "Login@123".

* After logging into the application, the user will have access to the Open Specimen dashboard and the application is ready to use
* Don't forget to change the default access credentials!
* See the [OpenSpecimen Manual](https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/7700605/User+Manual+Community+Edition) for more information

#### FAIRification
Follow these steps to make the app FAIR (**F**indable, **A**ccessible, **I**nteroperable and **R**eusable).

The FAIR Data Point will take the required information from the collection protocols as well as specifically designed forms:
1) In order to upload the FDP form (data/openspecimen_fdp_form/cp_fdp_attributes.xml) to Openspecimen: 
   1) In OpenSpecimen, use the Menu bar to navigate to the Forms page
   2) Here, click import and select the cp_fdp_attributes.xml file. The imported form will open, click "done" at the bottom of the page.
   3) After importing, we have to tell OpenSpecimen where we would like to attach this form to.  Click on the wrench icon next to the form. ![attach_form](assets/attach_form.png)
   4) Select "Collection Protocol Custom Fields" in the next window and attach the form to all present and future collection protocols. 
2) When you now create a new "**collection protocol**" or edit an already existing one, you can enter the FDP required information at the bottom ![cp_with_fdp_attributes](assets/cp_with_fdp_attributes.png) 



#### Set up FAIR Data Point.

Open Jupyter via the app details in the Bibbox Instances-page or by changing the subdomain of the URL to `<instancename>-jupyter`:
![os_jupyter_dashboard](assets/os_jupyter_dashboard.png)
Access Token is: FDP
1) Open Jupyter Notebook (/work/fillFDP.ipynb) 
    
2) Set user credentials for the FAIR Data Point and OpenSpecimen
FDP default credentials: email "albert.einstein@example.com", Password: "password"
OpenSpecimen default credentials: user: "admin", password: "Login@123"
![jupyter_set_login](assets/jupyter_os_fdp_login.png)

3) Execute the jupyter notebook by clicking the fast forward symbol (&#9193;) at the top. Make sure, that all collection protocols have the FDP form attached and the attributes are set. 

4) Open the FDP client to view the result, either via the dashboard or by changing the subdomain of the URL to `<instancename>-fdp-client`
![os_fdp_dashboard](assets/os_fdp_dashboard.png)
![os_fdp](assets/os_fdp.png)
Browsing data is possible without login! 

#### Set up Provenance Access Point
Open the Neo4j Browser, either via the app dashboard or by changing the subdomain of the URL to `<instancename>-pap-noe4j`
Login with username: "neo4j", password: "neo4j". You will be asked to set a new password, remember it!


Open Jupyter via the app dashboard or by changing the subdomain of the URL to `<instancename>-jupyter`:
![os_jupyter_dashboard](assets/os_jupyter_dashboard.png)
Access Token is: FDP
1) Open jupyter notebook (/work/fillPAP.ipynb) 
    
2) Set user credentials for the Neo4j database and OpenSpecimen
Neo4j password has been set by the user earlier!
OpenSpecimen default credentials: user: "admin", password: "Login@123"

3) Execute the jupyter notebook by clicking the fast forward symbol (&#9193;) at the top. The script will iterate through all collection protocols and all patients and add the provenance information for each specimen to the Neo4j database 

4) Open the Neo4j Browser and login to view the result
![neo4j](assets/neo4j.png)
