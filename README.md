# Childcare MongoDB Database 

## Purpose of Repo

The purpose of this repo is to show how to model and create data in a MongoDB database.

We will walk through how someone coming from a relational database would model data in MongoDB using a relational schema.

We will then go over how we create database indexes to optimize our queries but there maybe a couple of suprises along the way.

Finally we will walk through how we could model this data using embeded data and a relational or lookup aggregation to store less frequently accessed data.

Are you excited? Let's get started.

## Getting Required Software

We are going to be using a few tools through this repo that we will need to install.
- [Docker](https://www.docker.com/)
- [MongoDB](https://www.mongodb.com/)
- [MongoDB Compass](https://www.mongodb.com/products/compass)
- [Python](https://www.python.org/)
- [UV](https://docs.astral.sh/uv/)
  
I will walk through the instructions for each of these tools below for a Mac. If you are on a different platform you will need to adjust the instructions.

### Docker

The Docker instructions can be found [here](https://docs.docker.com/desktop/setup/install/mac-install/) . Choose the correct installation for a Apple Silicon or Intel Mac.

This rarely happens but I prefer to install Docker this way as there are always updates for Docker and it makes it easier to keep up with the latest version. If you want you can install Docker with Homebrew. 

`brew install --cask docker`

### MongoDB

Once you have Docker Desktop installed and runningyou can run MongoDB using the docker-compose.yml file located in the root of this repo. Simply run:

`docker compose up -d`

If you happen to have an older version of Docker where the command used to be `docker-compose` you can still run it with the following command:

`docker-compose up -d`

### MongoDB Compass

MongoDB Compass is a amazing GUI for MongoDB. It's a free tool that is available for Mac and Windows. You can download it [here](https://www.mongodb.com/products/tools/compass) or install it with Homebrew: `brew install --cask mongodb-compass`

To connect to your database running in docker open Compass and create a new connection with the following connection string: `mongodb://root:password@localhost:27017/`

### MongoDB Shell

Of course you will probably want to interact with MongoDB from the command line. You can install it from [here](https://www.mongodb.com/try/download/shell)with Homebrew: `brew install mongosh`

To connect to your database running in docker you can use the following command:
`mongosh -u "root" -p` then enter the password which is `password` when prompted.

### Python

We are going to be using Python and the [Pymongo](https://pymongo.readthedocs.io/en/stable/) library to connect to MongoDB. Along with that we will be managing our dependencies using [UV](https://docs.astral.sh/uv/). To install UV run the following command: `brew install uv`

