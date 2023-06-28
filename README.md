# HERO

<img align="left" width="80" height="80" src="./img/hero_icon.png">
Hospitality Enterprise Revenue Optimizer (HERO) builds on the [rezaware](https://github.com/waidyanatha/rezaware/wiki "hero logo") platform and is inherited as a submodule. The README file is intended for Rezgateway affiilates working on the HERO project. It povides an introduction to getting started with the available tools and code. Thereafter, refer to the WIKI for complete documentation on the system's components, and interfaces. 

## Introduction

The HERO app pipelines support Revenue Managers with applying analytics to gain insights for data-informed decision-making. There 4 key apps:
1. _Mining_ - Arificial Intelligence (AI) and Machine Learning (ML) analytic pipelines
1. _Wrangler_ - for processing data extract, transform, and load automated pipelines
1. _Visuals_ - interactive dashboards with visual analytics for Business Intelligence (BI)
1. _rezaware_ - framework utility packages extended by the above apps

## Quickstart
__Linux Only__

### Clone HERO
* Fork the HERO project from ```https://gitlab/rezcorp.com/data-science/HERO``` into your gitlab personal projects (e.g., https://gitlab/rezcorp.com/<my-rezgate-gitlab-username>/HERO)
* Clone the HERO project into your workspace and execute the following commands in from your shell
   * ```cd myworkspace``` (e.g., cd ~/workspace/rezprojects/)
   * ```git init```
   * ```git clone https://gitlab/rezcorp.com/<my-rezgate-gitlab-username>/HERO

### Init HERO
* Initialize the instance
   * ```cd HERO/rezaware```
   * ```python3 -m 000_setup --app=rezaware --with_ini_files```
   * this will generate the respective __app.ini__ files in the _module entity packages_

### Conda environment
* Create a conda environment
   * if you are not in the rezaware folder
      * ```cd HERO/rezaware```
   * create a python 3.8 environment and install __rezaware__ requirements packages
      * ```conda create -n <a_name_you_give> python=3.8 -r requirements.txt```
   * ```conda list``` will print a list to stdout like this

        ```
        
        # packages in environment at /home/nuwan/anaconda3/envs/reza:
        #
        # Name                    Version                   Build  Channel
        _libgcc_mutex             0.1                        main  
        _openmp_mutex             5.1                       1_gnu  
        absl-py                   1.2.0                    pypi_0    pypi
        alembic                   1.8.1                    pypi_0    pypi
        amqp                      5.1.1                    pypi_0    pypi
        aniso8601                 9.0.1                    pypi_0    pypi
        anyio                     3.6.1                    pypi_0    pypi
        apache-airflow            2.3.4                    pypi_0    pypi
        apache-airflow-providers-celery 3.0.0              pypi_0    pypi
        ...
        
        ```
* Install HERO requirements
   * change directory to HERO
      * ```cd myworkspace/HERO```
   * excute the requirements file
      * ```python3 -m pip install -r requirements.txt```
      
### Configure Apps
* Depending on your pyspark, hadoop, mongodb, postgresql installations
   * edit the rezaware __app.cfg__ file; rezaware uses these as default settings
   * similarly edit the mining, wrangler, and visuals __app.cfg__ files.

### Test instance
* Test the new setup with __pytest__
   * ```cd myworkspace/HERO```
   * ```pytest```

___Please note that the getting started steps have not been tested and should be revised with missing steps.___

