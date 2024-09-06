from elasticsearch import Elasticsearch, helpers
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

es.info()


# {
#       "note_source note": "Der Überschwemmte Rathausquai der Stadt Luzern mit dem Hotel de la Tour und dem  Federal sowie der Kappelbr\u00fccke im Hintergrund. Die \u00dcberschwemmung ereignete sich beim Jahrhundert Hochwasser von 1910.",
#       "title": "Der Überschwemmte Rathausquai der Stadt Luzern",
#       "identifier_PPNanalog": "TF_GP_01990",
#       "recordIdentifier": "BibZug_TD_23_01990",
#       "classification": "Bibliothek Zug#Glasplatten",
#       "dateIssued": "1910",
#       "accessCondition_use and reproduction": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
#       "accessCondition_restriction on access": "OPENACCESS",
#       "form_material": "Glasplatte",
#       "form_form": "Geschichte",
#       "extent": "9x12",
#       "coordinates": "47.0519806883, 8.30707289986",
#       "identifier_ark": "ark:/63274/bz1rb4r",
#       "roleTerm_code": "pht",
#       "namePart_family": "Weber-Strebel",
#       "namePart_given": "Joseph Maria",
#       "displayForm_personal": "Weber-Strebel, Joseph Maria",
#       "subject": "Unfall/Katastrophe",
#       "canton": "Luzern",
#       "documentType": "Photograph",
#       "fileUrl": [
#         {
#           "FILE_0001_DEFAULT": "https://zentralgut.ch/content/BibZug_TD_23_01990/800/0/TD_23_01990.jpg"
#         }
#       ],
#       "iiifUrl": [
#         {
#           "FILE_0001_IIIF": "https://zentralgut.ch/api/v1/records/BibZug_TD_23_01990/files/images/TD_23_01990.jpg"
#         }
#       ]
#     }
#  }




es.index(
 index='geophotoradar',
 document={
  {
      "title": "Der Überschwemmte Rathausquai der Stadt Luzern",
      "image_url": "https://zentralgut.ch/content/BibZug_TD_23_01990/800/0/TD_23_01990.jpg",
      "id": "BibZug_TD_23_01990",
      "coordinates": "47.0519806883, 8.30707289986",
      "zentralgut_url": "https://n2t.net/ark:/63274/bz1rb4r",
      "iiif_url": "https://zentralgut.ch/api/v1/records/BibZug_TD_23_01990/files/images/TD_23_01990.jpg"
    }
 })