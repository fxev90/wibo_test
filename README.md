# Wibo Test Repository
# Francisco Escalante
This repository contains the code for the Wibo Test, which is divided into two main parts:

- A backend application built with Fastapi
- A frontend application built with Angular

The project also utilizes Docker for managing a Mongodb database and a container for the Fastapi app.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Clone the Repository](#clone-the-repository)
- [Environment Setup](#environment-setup)
- [Running the Angular Application](#running-the-angular-application)

## Prerequisites

- Node.js (v18.x or later)
- Docker (v24.0.6 or later)
- NPM package manager

## Getting Started

### Clone the Repository

```bash
git clone git@github.com:fxev90/wibo_test.git
cd wibo_test
```

### Environment Setup

Copy the `.env.example` file and rename it to `.env`. Update the `.env` file with your actual environment variables.

```bash
cp .env.example .env
```

### Run  Docker to build Fastapi app container

In the root directory of the repository, run the following command:
```bash
docker-compose build
```

```bash
docker-compose up
```

## Running the Angular Application

### Navigate to the Angular Folder
### This application run outside the container
Go to the root folder of the repo then 
```bash
cd ./client_angular
```
### Install Dependencies

```bash
npm install
```

```bash
npm install -g @angular/cli@latest
```



### Run the Application

```bash
ng serve
```

The application will start running on [http://localhost:4200/]

### DEMO Credentials
user=admin
Password=123456789


### Mongodb config
Is being setup in
```bash
vim ./db_confs/init-mongo.js
```
```bash
vim ./db_confs/mongod.conf
```