from csv import DictReader

from app.record import Record
from typing import List
import csv


class Importer:
    def read_csv_to_records(self, csv_reader: DictReader) -> List[Record]:
        records = []
        for row in csv_reader:
            try:
                lat_str, lon_str = row['coordinates'].split(',')
            except ValueError as e:
                # print(str(e))
                continue
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            # Create a Record instance from each row
            record = Record(
                id=row['id'],
                title=row['title'],
                image_url=row['image_url'],
                lat=lat,
                lon=lon,
                iiif_url=row['iiif_url'],
                source_system_url=row['source_system_url']
            )
            records.append(record)
        return records

