class StoreLayout:

    def __init__(self):
        self.zones = {
            "DISPLAY_TOP": {
                "polygon": [
                    (0, 0), (1000, 0),
                    (1000, 180), (0, 180)
                ]
            },
            "FOH": {
                "polygon": [
                    (0, 180), (1000, 180),
                    (1000, 650), (0, 650)
                ]
            },
            "BILLING": {
                "polygon": [
                    (800, 200), (1000, 200),
                    (1000, 650), (800, 650)
                ]
            },
            "AISLE_BOTTOM": {
                "polygon": [
                    (0, 650), (1000, 650),
                    (1000, 1000), (0, 1000)
                ]
            }
        }

    def _point_in_polygon(self, x, y, poly):
        inside = False
        n = len(poly)
        p1x, p1y = poly[0]

        for i in range(n + 1):
            p2x, p2y = poly[i % n]

            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                        if p1x == p2x or x <= xinters:
                            inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    def get_zone(self, x, y):
        for zone_name, zone_data in self.zones.items():
            if self._point_in_polygon(x, y, zone_data["polygon"]):
                return zone_name
        return "UNKNOWN"