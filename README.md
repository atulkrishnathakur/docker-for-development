# How to docker for FastAPI development

## Create `Dockerfile` to use for development
```
# Use the official Python image
FROM python:3.12.8

# Set the working directory
WORKDIR /docker-for-development

# This command put requirements.txt in container in specific directory
COPY ./requirements.txt /docker-for-development/requirements.txt


# This command will install dependancies in docker container
RUN pip install --no-cache-dir --upgrade -r /docker-for-development/requirements.txt

# copy source code files and directory in docker container
COPY ./app /docker-for-development/app

# this is default command. It will run after container start. It is used for development only
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]

```

- In this docker file we are using `CMD` command for fastapi development
```
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
```

- For the production use below `CMD` command
```
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

```

## Create the `docker-compose.yml` file for development
```
# version: '3.9' # Defines the version of Docker Compose being used. No need to write in newer version in docker compose file

services:
  fastapiapp: # Service for your FastAPI application
    build:
      context: . # Directory containing the Dockerfile
      dockerfile: Dockerfile # Path to the Dockerfile for building the image
    image: fastapiappimage:dev # Name and tag for the Docker image
    container_name: fastapiappcontainer # Custom name for the container
    ports:
      - "8000:8000" # Maps port 8000 on the host to port 8000 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - webstore:/docker-for-development/app/uploads # Persistent storage for application-specific data
      - webpdfstore:/docker-for-development/app/generated_pdf
      - .:/docker-for-development  # Bind-mounted local directory for live updates. It used only for development not for production
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - ENV=$ENV # Explicitly defines the ENV variable from the .env file
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before FastAPI app
    networks:
      - dockerfordevelopmentnetwork # Connects to your custom network
    restart: unless-stopped # better for development. better for debuging. If you want to stop container manually then it will not again start automatically. It will start automatically when system reboot
    
  nginx: # Service for the Nginx web server
    image: nginx:stable # Uses the stable version of the official Nginx image
    container_name: nginxcontainer # Custom name for the container
    ports:
      - "80:80" # Maps port 80 on the host to port 80 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro # Mounts the custom Nginx configuration file in read-only mode. It is bind mount. It is not persistent valume
    depends_on:
      - fastapiapp # Ensures FastAPI app starts before Nginx
    networks:
      - dockerfordevelopmentnetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  postgresdb: # Service for the PostgreSQL database
    image: postgres:17 # Uses the official PostgreSQL image for version 17
    container_name: postgrescontainer # Custom name for the container
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - POSTGRES_USER=$POSTGRES_USER # Explicitly defines the POSTGRES_USER and $POSTGRES_USER from the .env file
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD # Explicitly defines the POSTGRES_PASSWORD and $POSTGRES_PASSWORD from the .env file
      - POSTGRES_DB=$POSTGRES_DB # Explicitly defines the POSTGRES_DB and $POSTGRES_DB from the .env file
      - POSTGRES_SERVER=$POSTGRES_SERVER # Explicitly defines the POSTGRES_SERVER and $POSTGRES_SERVER from the .env file
      - POSTGRES_PORT=$POSTGRES_PORT # Explicitly defines the POSTGRES_PORT and $POSTGRES_PORT from the .env file
    volumes:
      - postgresdata:/var/lib/postgresql/data # Persistent storage for database data
    networks:
      - dockerfordevelopmentnetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  pgadmin4: # Service for pgAdmin4
    image: dpage/pgadmin4:9.1.0 # Uses pgAdmin4 version 9.1.0
    container_name: pgadmin4container # Custom name for the pgAdmin4 container
    ports:
      - "5050:80" # Maps port 5050 on the host to port 80 in the container
    environment:
      - PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL # Admin email for logging into pgAdmin4
      - PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD # Admin password for logging into pgAdmin4
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before pgAdmin4
    volumes:
      - pgadmin4data:/var/lib/pgadmin # Persistent storage for database data
    networks:
      - dockerfordevelopmentnetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

volumes:
  webstore: # Named volume for FastAPI app data
    driver: local # used to create valume in host machine
    name: docker-for-development_uploads # Explicitly set the volume name

  webpdfstore: # Named volume for FastAPI app data
    driver: local # used to create valume in host machine
    name: docker-for-development_generated_pdf # Explicitly set the volume name

  
  postgresdata: # Named volume for PostgreSQL data
    driver: local # used to create valume in host machine
    name: docker-for-development_postgresdata # Explicitly set the volume name

  pgadmin4data: # Named volume for PostgreSQL data
    driver: local # used to create valume in host machine
    name: docker-for-development_pgadmin4data # Explicitly set the volume name

networks:
  dockerfordevelopmentnetwork: # Use consistent naming for the custom network
    driver: bridge
    name: docker-for-development-network # Explicitly provide network name.
```

1. Bind mounted volume for source code. The `docker-for-development` is the project root dirctory. When you use bind mount volume for source code then your changes will be reflected automatically. Remove this volume if you deploy the source code for production.
```
    volumes:
      - .:/docker-for-development  # Bind-mounted local directory for live updates. It used only for development not for production
```

2. `restart: unless-stopped` command used for developement. It is better for development. It is better for debuging. If you want to stop container manually then it will not again start automatically. It will start automatically when system reboot. When you deploy for production then use `restart: always`


