The following application setup guide has only been tested on Ubuntu 16.04 LTS. 

#### Service dependencies

- Virtualenv
- Flask
- Numpy
- GDAL

#### Installation Steps
1. Installing system dependencies: `sudo apt-get install -y python-pip python-psycopg2 python-dev libpq-dev libgdal-dev libgdal1i gdal-bin virtualenv`

2. Check the installed gdal version: `gdalinfo --version`

3. Create a python virtual environment: `virtualenv env`

4. Installing python dependencies in virtual environment:
    
        source env/bin/activate
        pip install numpy flask
        pip install pygdal

Finally, we have installed the necessary libraries to build our service. On the next post, we will be covering the API development of our service. 
