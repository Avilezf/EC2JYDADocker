﻿# EC2JYDADocker
 Introduction:
 
 This is a project in based on create a technologic solution for Data Analytics for the following Containers:
 
  1. Container Jupyter Notebook 
  2. Container Postgres Database
  3. Container Dash Server

Following the instructions:

  1. Populate the database with a data source (any data source, in our case, we use a dvd's rental database)
  2. From a jupyter notebook connect to the database and make at least 3 visualizations from the data
  3. Show those same visualizations they use on the Dash server
 
# Play with Docker

1. The first thing is to Clone the github repository into the instance:
```
git clone https://github.com/Avilezf/EC2JYDADocker.git
```
2. Change the directory to the repository
```
cd EC2JYDADocker
```

3. Start the docker compose
```
docker-compose up
```

# Important!
The Jupyter Notebook have a password or token necessary to visualize the information:
```
pydata
```
# Authors
Luis Fernando Llanos Avilez,
Andrés Felipe Tovar Sandoval
Sebastian Combita
Gabriel Castillo

