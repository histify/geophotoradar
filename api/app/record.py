class Record:
    def __init__(
            self,
            id: str,
            title: str,
            image_url: str,
            lat: float,
            lon: float,
            iiif_url: str,
            source_system_url: str,
    ):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.lat = lat
        self.lon = lon
        self.iiif_url = iiif_url
        self.source_system_url = source_system_url
