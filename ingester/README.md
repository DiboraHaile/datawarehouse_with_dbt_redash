# To run the postgres database
You first need to create env file in this directory
which will hold environmental variables for the postgres image
[To read more about postgres image variables](https://hub.docker.com/_/postgres)

Environment variables that are needed for this project:
``` 
    POSTGRES_USER:
    POSTGRES_PASSWORD:
    POSTGRES_DB=traffic_stream_record
    
```

Then you run:

``` docker-compose build ```


which will build an image based on your specification
