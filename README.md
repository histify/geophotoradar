# Geo Photo Radar

This project was done as part of the GLAMHack24, the Swiss Open Cultural Data Hackathon. See the [project description](https://hack.glam.opendata.ch/project/211).

## Load csv data with curl

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



## Set up local directories for docker-compose and elastic kiban

Do this in app root folder :
```
mkdir esdata01
mkdir esdata02
mkdir kibanadata
chmod g+rwx esdata01
chmod g+rwx esdata02
chmod g+rwx kibanadata
sudo chgrp 0 esdata01
sudo chgrp 0 esdata02
sudo chgrp 0 kibanadata
```