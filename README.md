# Apache-Airflow-Beam-TensorFlow-Examples
Various examples for TensorFlow Extended using Apache Beam and Airflow

## Preface

<p>The Goal of the repository is to show what is possible for Machine Learning End2End Pipelines for Computer Vision problems.</p>
<p>In this repository the possiblities of TensorFlow Extended in combination with Apache Airflow and Apache Beam will be discovered. In order to do that, some Pipelines will be created and presented, which will run the different DAGs (Directed Acyclic Graphs). While showing a basic example with CSV Data, there will be a focus on Computer Vision tasks. Therefore at least an Image Classification and a Semantic Segmantation Pipeline will be presented.</p>
<p>Since I only have an Windows Computer I will run everything on the Ubuntu20.04 WSL (Windows Subsystem for Linux) and will write a guide for a proper setup. Furthermore with the right setup every example and code file should be executable on any Windows (and of courde Linux) computer.</p>

## Main Library Features

 - Introduction on how to set up Apache Beam and Airflow on Windows
 - Multiple end2end pipelines build on top of TensorFlow, Apache Beam and Apache Airflow
 
# Table of Contents

 - [Installation and Setup](#installation-and-setup)
   - [Setup Ubuntu WSL for Windows Users](#setup-ubuntu-wsl-for-windows-users)
   - [Configure Airflow and its Dependencies](#configure-airflow-and-its-dependencies)
 - [Run a Pipeline](#run-a-pipeline)
 - [Examples](#examples)
 - [Citing](#citing)
 - [License](#license)
 - [References](#references)
 
## Installation and Setup

<p>To get the repository running just check the following requirements.</p>

**Requirements**
1) Python 3.8
2) tensorflow >= 2.3.0 (>= 2.0.0 is sufficient if no efficientnet backbone is used)
3) tfx == 0.24.0
4) apache-beam == 2.24.0
5) apache-airflow[celery] == 1.10.12
6) psycopg2 == 2.8.6
7) tfx == 0.24.0
8) tensorflow_advanced_segmentation_models
9) albumenatations
10) numpy

<p>Furthermore just execute the following command to download and install the git repository.</p>

**Clone Repository**

    $ git clone https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples.git


### Setup Ubuntu WSL for Windows Users

**Steps:**

<ol>
 <li>Installing Ubuntu on Windows
  <ol>
   <li>Go to the Microsoft Store on your computer and search for Ubuntu 20.04</li>
   <li>Download and Install Ubuntu 20.04</li>
   <li>Enable Devloper Mode on Windows:
    <ol>
     <li>Type "Developer" into the Windows search bar and select the option that says "Developer Settings"</li>
     <li>1.3.2 In the page that appears, select the bubble next to the "Developer Model" option.</li>
    </ol>
   </li>
   <li>Enable Windows Subsystem for Linus (WSL):
    <ol>
     <li>Type "Windows Feature" into the Windows search bar and select the option that says "Turn Windows features on or off"</li>
     <li>Scroll down to the point "Windows Subsystem for Linux and check the box.</li>
     <li>Click ok and restart your computer</li>
    </ol>
   </li>
  </ol>
 </li>
 <li>Initialize Ubuntu:
  <ol>
   <li>Run Ubuntu and wait until the initial installation process finishes</li>
   <li>Ubuntu will then ask you for a **username** and a **password**, type in and enter your credentials (Be Careful: Remember them or write them somewhere down)</li>
  </ol>
 </li>
</ol>

<p>Now when the above steps are done, we can install all dependencies that are necessary to run Airfow.</p>

### Configure Airflow and its Dependencies

**Steps:**

<ol>
 <li>Installing PIP
  <ol>
   <li>Run the following sequence of commands in the Ubuntu CLI</li>
  
        sudo apt-get install software-properties-common  
        sudo apt-add-repository universe
        sudo apt-get update
        sudo apt-get install python3-setuptools
        sudo apt install python3-pip
        sudo -H pip install --upgrade pip
     
  <li>Verify the installation:</li>
        
        pip -V
        
  </ol>
 </li>
 <li>Installing Dependencies
  <ol>
   <li>Run the following commands</li>

        sudo apt-get install libmysqlclient-dev 
        sudo apt-get install libssl-dev 
        sudo apt-get install libkrb5-dev 
        sudo apt-get install libsasl2-dev 

   <li>Install PostgreSQL for Airflow (Our robust backend database)
    
        sudo apt-get install postgresql postgresql-contrib
        
   <ol>
   <li>Start the PostgreSQL service with the following command:</li>
   
        sudo service postgresql start
    
   <li>Check the status of the cluster and make sure that it is running by using the following command:</li>
    
        pg_lscluster
    
   <li>From the above command's output extract the "Ver", "Cluster" and insert it in the follwing command (When run the output should something like: *Cluster is already running*:</li>
    
        sudo pg_ctlcluster <version> <cluster> start
   </ol>
   </li>
  
   <li>Now create a Database for Airflow to use, execute:
    
        sudo -u postgres psql
   <ol> 
   <li>Create a profile and assign the correct privileges:</li>
    
        CREATE ROLE ubuntu;
        CREATE DATABASE airflow;
        GRANT ALL PRIVILEGES on database airflow to ubuntu;
        ALTER ROLE ubuntu SUPERUSER;
        ALTER ROLE ubuntu CREATEDB; 
        ALTER ROLE ubuntu LOGIN;
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ubuntu;
    
   <li>Setup a password for the ubuntu server (Again remember this or write it down):</li>

        \password ubuntu
   
   <li>Finally confirm the password and type \q to quit.</li>
   </ol>
   </li>
   <li>Connect to the Airflow database and verify the connection information:
 
        postgres-# \c airflow
         
   <ol>
   <li>Run the following to receive response for valid working connection:</li>
    
        \conninfo
        
   <li>Hit Ctrl + Z to stop the session and enter the following command to navigate to the config file:</li>
   
        cd /etc/postgresql/*/main/
        ls
   <li>Open the file pg_hba.conf:</li>
   
        sudo nano pg_hba.conf
        
   <li>Modify the file: Modify the line underneath #IPv4 local connections under the column ADDRESS to 0.0.0.0/0</li>
   <li>Press Ctrl + S to save and Ctrl + X to exit</li>
   <li>Now, open postgresql.conf</li>
    
        sudo nano postgresql.conf
        
   <li>Modify the file: Under the "CONNECTIONS AND AUTHENTICATION", modify the following: listen_adresses = '*'</li>
   <li>Press Ctrl + S to save and Ctrl + X to exit</li>
   </ol>
   </li>
   <li>Finally, restart postgresql to save and load the changes:
   
        sudo service postgresql restart
        
   <ol>
   <li>Go back to the root directory, by executing the command:</li>
 
        cd ~
      
   </ol>
   </li>
  </ol>
 </li>
 <li>Installing Apache Airflow, for a quick start guide look <a href="https://airflow.apache.org/docs/stable/start.html">here</a>.
  <ol>
   <li>To install Airflow, run the following command:</li>
   
        sudo SLUGIFY_USES_TEXT_UNIDECODE=yes pip install apache-airflow[celery]
        
   <li>Add the path to PATH within the terminal, change in the following the <username> to your username</li>
   
        export PATH=$PATH:/home/<username>/.local/bin
        
   <li>Apache Airflow is now installed, close the Ubuntu instance and reopen it again</li>
  </ol>
 </li>
 <li>Apache Airflow Setup
  <ol>
   <li>Initialize the Database</li>
   
        airflow initdb
        
   <li>When completed, the necessary config files were being created in the airflow directory, now make changes to the airflow.cfg file
 
        cd airflow
        ls
        sudo nano airflow.cfg
        
   <ol>
   <li>Make the following changes to the config file: (You can change the directory of the dags_folder and base_log_folder to any directory you want) (Insert the password you created previously in the <password> section of the sql_alchemy_conn value.)</li>

        dags_folder = /mnt/c/dags
        base_log_folder = /mnt/c/dags/logs
        executor = CeleryExecutor
        load_examples = False
        expose_config = True
        sql_alchemy_conn = postgresql+psycopg2://ubuntu:<password>@localhost:5432/airflow
        broker_url = amqp://guest:guest@localhost:5672//
        result_backend = amqp://guest:guest@localhost:5672//
        
   <li>Enter Ctrl + S to save and Ctrl + X to exit</li> 
   </ol>
   </li>
   <li>Once the above step is finished, initialize airflow again:
        
        airflow initdb
   
   <ol>
   <li>Error Handling: If error relating to the psycopg2 package is received, run the following commands:</li>
        
        sudo apt-get update -y
        sudo apt-get install -y libpq-dev
        pip install psycopg2
    
   </ol>
   </li>
   <li>Install Rabbitmq</li>
        
        sudo apt install rabbitmq-server
        
   <ol>
   <li>Go to the config file of rabbitmq:</li>
 
        sudo nano /etc/rabbitmq/rabbitmq-env.conf
   
   <li>Change the node IP adress to: NODE_IP_ADDRESS=0.0.0.0</li>
   <li>Now start the RabbitMQ Server</li>
   
        sudo service rabbitmq-server start
   </ol>
   <li>Run Airflow initdb one last time:</li>
   
        airflow initdb
  </ol>
 </li>
 <li>Final Steps to launch Webserver, Scheduler and Celery Worker
  <ol>
   <li>In the first terminal run:</li>
    
        airflow webserver -p 8080
        
   <li>Open a new Ubuntu Terminal and run:</li>
 
        airflow scheduler
        
        
   <li>Open another Ubuntu Terminal and run:</li>
   
        airflow worker
  </ol>
 </li>
</ol>

<p>You are now finished setting up Airflow and its dependencies, now when the Airflow Webserver has startet, go into your browser and run <a href="http://localhost:8080"><strong>localhost:8080</strong></a> in a new tab. A local page showing the current DAGs should load. Here all your dags, which are in the above configured "dags_folder" should appear (as far as the code has no bugs in the DAGs Pipeline)

## Run a Pipeline

**Steps:**

<ol>
 <li>Go to the directory where you cloned the repository</li>
 <li>Copy the file "camvid_seg_pipeline.py" to the dags folder you configured above</li>
 <li>Copy the folder "camvid airflow project" in to the dags folder you configured above</li>
 <li>Open a Ubuntu CLI (Command Line Interface) and run the following two commands:
  <ol>
   <li>Run:</li>
  
    airflow initdb
   
   <li>Then Run:</li>
   
    airflow worker
   
  </ol>
 </li>
 <li>Open another Ubuntu CLI and run:</li>

    airflow scheduler
 
 <li>Open another Ubuntu CLI and run:</li>
 
    airflow webserver -p 8080
 
 <li>Running the DAGGo into your browser to: localhost:8080
  <ol>
   <li>First Method: Using a Webbrowser
    <ol>
     <li>Go into you webbrowser of choice and enter: localhost:8080</li>
     <li>Click on the Play Button next to your DAG under Links</li>
     <li>Click Trigger</li>
    </ol>
   </li>
   <li>Second Method: Using the CLI
    <ol>
     <li>Open another CLI</li>
     <li>Run:</li>
     
    airflow trigger_dag <your_pipeline_name>
  
   </ol>
   </li>
  </ol>
 </li>
</ol>
  
 Finished!

<p>The DAG is now running you can now take a closer look if you click on the name of your DAG to see the details.</p>
 
## Examples

## Citing

    @misc{Kezmann:2020,
      Author = {Jan-Marcel Kezmann},
      Title = {YourCookBook},
      Year = {2020},
      Publisher = {GitHub},
      Journal = {GitHub repository},
      Howpublished = {\url{https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Exampless}}
    }

## License

Project is distributed under <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/blob/master/LICENSE">MIT License</a>.

## References
