# Safety site
## Web application for detecting safety violations

## Initialization
*add .env file to root folder*

File looks like:
* *SECRET_KEY*=**value**
* *POSTGRES_HOST*=**value**
* *POSTGRES_DB*=**value**
* *POSTGRES_USER*=**value**
* *POSTGRES_PASSWORD*=**value**
* *PGADMIN_DEFAULT_EMAIL*=**value**
* *PGADMIN_DEFAULT_PASSWORD*=**value**

## Building
*docker build -t [image_name] .*

## Running containers
*docker-compose up*

## Stopping containers
*docker-compose down*