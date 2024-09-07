# Geo Photo Radar

This project was done as part of the GLAMHack24, the Swiss Open Cultural Data Hackathon. See the [project description](https://hack.glam.opendata.ch/project/211).

## Goal

With the [photos accessible on the Zentralgut website](https://zentralgut.ch/glasplatten_zug/),
the Bibliothek Zug aims to bring the collection to a broader audience through the development of a mobile app. This app will notify users when they are near a location where one of the georeferenced photos from the "Glasplattensammlung Zug" was taken, offering a unique and immersive way to explore the region's history. This app provides a look into the past, allowing users to compare historical life and architecture with the present-day, offering a distinctive perspective on Zug's evolution over time.

## Demo

The demo installation can be accessed under https://photos.histify.app/

## Solution

This project provides a mobile web app (PWA), which allows to expierence the photos while walking through the city of Zug.
The app is built in a way that it can be reused for other dataset and hosted by anywone.

It consists of these components:

- `frontend` - the web application
- `api` - a small api for retrieving the data and uploading the data
- `elasticsearch` - an elasticsearch installation hosting the data

## Try it out

The `compose-prod.yaml` provides a setup with which you can try out the application.
In order for trying it out in a local machine, you need `git` and `docker` installed.
Follow these steps:

- clone the git repository
- run `docker compose -f compose-prod.yml up -d`
- visit http://localhost:8000/api/docs and upload a dataset
  - you need to prepare your dataset in a CSV similar to `data/bibzug_glasplatten_adapted.csv`
  - you need to authenticate with a bearer token, which is `dataimporttoken` in this setup
  - you can also do it with curl; see below
- visit http://localhost:8000 for testing the app

## Load data with curl

Sample data is in the `data` folder

To load it, you can use https://photo.histify.app/api/docs or with curl in the `data` folder
```
curl -X 'POST' \
  'https://photo.histify.app/api/import' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer XXXXXXXXXXXXXXX' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@bibzug_glasplatten_adapted.csv;type=text/csv'
```

In order to do that, you need an api key.


## Development environment

You can start the development environment within docker containers:

- clone the git repository
- run `docker compose build`
- run `docker compose up -d`
- visit http://localhost:8000
