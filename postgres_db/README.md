## To setup the postgres database
- You first need to create env file in this directory which will hold environmental variables for the postgres image [To read more about postgres image variables](https://hub.docker.com/_/postgres)

Environment variables that are needed for this project:
``` 
    POSTGRES_USER:
    POSTGRES_PASSWORD:
    POSTGRES_DB=traffic_stream_record
    
```

- To start the postgres container:

``` 
    docker-compose up -d 
```


This will create postgres_data in this folder which will contain all the data stored in your database, to modify this you can go to the docker-compose file.
