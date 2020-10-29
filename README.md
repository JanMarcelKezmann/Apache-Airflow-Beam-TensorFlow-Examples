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

 - [Examples](#examples)
 - [Installation and Setup](#installation-and-setup)
 - [Run a Pipeline](#run-a-pipeline)
 - [Citing](#citing)
 - [License](#license)
 - [References](#references)
 
## Examples
 
<p>Here all the current example DAGs are listed, this list will be updated over time, while the installation and setup process should stay the same.</p>
<p>For more details about the example look at <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/tree/main/dags/">this</a> README.md.</p>

- <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/blob/main/dags/classification_dag.py">Classification DAG</a>, is an Image Classification example, for classifying 6 different classes. the Utils files can be found <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/tree/main/dags/classification_pipeline">here</a>.

In Progress:
 - Semantic Segmentation Pipeline
 
## Installation and Setup

<p>To get the repository running just check the following requirements.</p>

**Requirements**
1) Python 3.8
2) tensorflow >= 2.3.0
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

**Setup Ubuntu and configure Airflow**

<p>Take a look at <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/blob/main/Installation-And-Setup.md">Markdown</a> file, to get a detailed setup tutorial for Ubuntu on Windows and for the correct configuration of Airflow.</p>

<p>The Setup process for Ubuntu and Airflow is heavily based on the Medium Article written by Ryan Roline. It's main differences are the Python Version and the installation of apache-airflow including the Celery package. Therefore I recommend to read the full article if some problems with the below mentioned steps occur, but be aware to use the correct Versions and Ubuntu Instance for the Setup. The URL reference can be found at the end of the README.</p>

<p>Once you are finished setting up Airflow and its dependencies, you can run a pipeline as explained below, access the browser and run <a href="http://localhost:8080"><strong>localhost:8080</strong></a> in a new tab. A local page showing the current DAGs should load. Here all your dags, which are in the above configured "dags_folder" should appear (as far as the code has no bugs in the DAGs Pipeline)

## Run a Pipeline

<p>This is the example procedure to run one of the DAGs in the repositories dags folder.</p>
<p>Everything should run, but in order to make it work, either convert the data in the <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/tree/main/dags/classification_pipeline/data/Image_Classification">Image Classification</a> directory by running the following command:</p>

    cd /mnt/c/dags/classification_pipeline/
    python3 convert_data_to_tfrecord.py
    
<p>this should transform the small sample of the original dataset to a tfrecord file, or simply Add Image data yourself into that directory and convert it to a tfrecord by applying small changes to the "convert_data_to_tfrecord.py" file.</p>
<p>Once the data is set up, you can continue with the following steps:</p>

**Steps:**

<ol>
 <li>Go to the directory where you cloned the repository</li>
 <li>Copy the file "classification_dag.py" to the dags folder you configured above</li>
 <li>Copy the folder "classification_pipeline" in to the dags folder you configured above</li>
 <li>Open a Ubuntu CLI (Command Line Interface) and run the following two commands:
  <ol>
   <li>Run:</li>
  
    airflow initdb
   
   <li>Then Run:</li>
   
    airflow webserver -p 8080
   
  </ol>
 </li>
 <li>Open another Ubuntu CLI and run:</li>

    airflow scheduler
 
 <li>Open another Ubuntu CLI and run:</li>
 
    airflow worker
 
 <li>Running the DAGGo into your browser to: localhost:8080
  <ol>
   <li>First Method: Using a Webbrowser
    <ol>
     <li>Go into you webbrowser of choice and enter: localhost:8080</li>
     <li>Click on the Play Button next to the DAG under Links</li>
     <li>Click Trigger</li>
    </ol>
   </li>
   <li>Second Method: Using the CLI
    <ol>
     <li>Open another CLI</li>
     <li>Run:</li>
     
    airflow trigger_dag classification_dag
  
   </ol>
   </li>
  </ol>
 </li>
</ol>
  
 Finished!

<p>The DAG is now running you can now take a closer look if you click on the name of your DAG to see the details.</p>

## Citing

    @misc{Kezmann:2020,
      Author = {Jan-Marcel Kezmann},
      Title = {Apache Airflow Beam TensorFlow Examples},
      Year = {2020},
      Publisher = {GitHub},
      Journal = {GitHub repository},
      Howpublished = {\url{https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples}}
    }

## License

Project is distributed under <a href="https://github.com/JanMarcelKezmann/Apache-Airflow-Beam-TensorFlow-Examples/blob/master/LICENSE">MIT License</a>.

## References

 - Ryan Roline, Installing Apache Airflow on Windows, Medium.com, <a href="https://medium.com/@ryanroline/installing-apache-airflow-on-windows-10-5247aa1249ef">Installing Apache Airflow on Windows</a>
 - TensorFlow, TensorFlow TFX Guide, Github.com, <a href="https://github.com/tensorflow/tfx/tree/master/docs/guide">TFX Guide</a>
 - TensorFlow, TFX Guide, TensorFlow.org, <a href="https://www.tensorflow.org/tfx/guide/">TFX Guide</a>
 - Hannes Hapke & Catherine Nelson, Building Machine Learning Pipelines, Github.com, <a href="https://github.com/Building-ML-Pipelines/building-machine-learning-pipelines">Building ML Pipelines</a>
 - Puneet Bansal, Intel Image Classification, kaggle.com, <a href="https://www.kaggle.com/puneet6060/intel-image-classification">Intel Image Classification</a>
