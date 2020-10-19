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


### Setup Ubuntu20.04 WSL for Windows Users

**Steps:**

 1. Installing Ubuntu on Windows<br>
  1.1 Go to the Microsoft Store on your computer and search for Ubuntu 20.04<br>
  1.2 Download and Install Ubuntu 20.04<br>
  1.3 Enable Devloper Mode on Windows:<br>
  &nbsp;&nbsp;1.3.1 Type "Developer" into the Windows search bar and select the option that says "Developer Settings"<br>
  &nbsp;&nbsp;1.3.2 In the page that appears, select the bubble next to the "Developer Model" option.  <br>
  1.4 Enable Windows Subsystem for Linus (WSL):<br>
  &nbsp;&nbsp;1.4.1 Type "Windows Feature" into the Windows search bar and select the option that says "Turn Windows features on or off"<br>
  &nbsp;&nbsp;1.4.2 Scroll down to the point "Windows Subsystem for Linux and check the box.<br>
  &nbsp;&nbsp;1.4.3 Click ok and restart your computer<br>
   
 2. Initialize Ubuntu:<br>
  2.1 Run Ubuntu and wait until the initial installation process finishes<br>
  2.2 Ubuntu will then ask you for a **username** and a **password**, type in and enter your credentials (Be Careful: Remember them or write them somewhere down)

<p>Now when the above steps are done, we can install all dependencies that are necessary to run Airfow.</p>

### Configure Airflow and its Dependencies

**Steps:**

 1. Installing PIP  
  1.1 Run the following sequence of commands in the Ubuntu CLI  
  
        sudo apt-get install software-properties-common  
        sudo apt-add-repository universe
        sudo apt-get update
        sudo apt-get install python3-setuptools
        sudo apt install python3-pip
        sudo -H pip install --upgrade pip
  1.2 Verify the installation:  
        
        pip -V
        
   
 2. Installing Dependencies<br>
  2.1 Run the following commands<br>

        sudo apt-get install libmysqlclient-dev 
        sudo apt-get install libssl-dev 
        sudo apt-get install libkrb5-dev 
        sudo apt-get install libsasl2-dev 

  2.2 Install PostgreSQL for Airflow (Our robust backend database)<br>
    
        sudo apt-get install postgresql postgresql-contrib
    
   ..2.2.1 Start the PostgreSQL service with the following command:<br>
   
        sudo service postgresql start
    
   ..2.2.2 Check the status of the cluster and make sure that it is running by using the following command:<br>
    
        pg_lscluster
    
   ..2.2.3 From the above command's output extract the "Ver", "Cluster" and insert it in the follwing command (When run the output should something like: *Cluster is already running*:<br>
    
        sudo pg_ctlcluster <version> <cluster> start
    
   2.3 Now create a Database for Airflow to use, execute:<br>
    
        sudo -u postgres psql
    
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.3.1 Create a profile and assign the correct privileges:<br>
    
        CREATE ROLE ubuntu;
        CREATE DATABASE airflow;
        GRANT ALL PRIVILEGES on database airflow to ubuntu;
        ALTER ROLE ubuntu SUPERUSER;
        ALTER ROLE ubuntu CREATEDB; 
        ALTER ROLE ubuntu LOGIN;
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ubuntu;
    
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.3.2 Setup a password for the ubuntu server (Again remember this or write it down):<br>

        \password ubuntu
    


## Run a Pipeline

**Steps:**
 1. Go to the directory where you cloned the repository
 2. Copy the file "camvid_seg_pipeline.py" to the dags folder you configured above
 3. Copy the folder "camvid airflow project" in to the dags folder you configured above
 4. Open a Ubuntu CLI (Command Line Interface) and run the following two commands:<br>
   4.1 Run:
   ```
      airflow initdb
   ```
  
   ```
      airflow worker
   ```
 5. Open another Ubuntu CLI and run:
 ```
    airflow scheduler
 ```
 
 6. Open another Ubuntu CLI and run:
 ```
    airflow webserver -p 8080
 ```
 7. Go into your browser to: localhost:8080<br>
   7.1 Click on the Play Button next to your DAG under Links<br>
   7.2 Click Trigger
 
<p>In Case you do not want to trigger the DAG in the Browser:</p>
 
 8. Instead of goint onto your browser open another Ubuntu CLI and run:
 ```
    airflow trigger_dag camvid_seg_pipeline
 ```
  
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
