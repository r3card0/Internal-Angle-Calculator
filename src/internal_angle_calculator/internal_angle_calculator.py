from shapely import wkt
from shapely.geometry import Point, LineString
from pyproj import CRS, Geod
import math

class InternalAngle:
    """
    Computes the internal angle between two LineStrings (in WKT format), 
    automatically selecting the most accurate method:
      - If the coordinates are in degrees (lat/lon), it uses geodesic calculation (pyproj.Geod)
      - If the coordinates are projected (meters), it uses planar trigonometry
    """
    def __init__(self,linestring1:str,linestring2:str, crs: str = "EPSG:4326"):
        # 1. Convert the lines from WKT format to geometry objects (shapely)
        self.line1 = wkt.loads(linestring1)
        self.line2 = wkt.loads(linestring2)
        
        # Set the geographic system and the ellipsoid
        self.crs = CRS.from_user_input(crs) # interprets a coordinate reference system (CRS) description
        self.geod = Geod(ellps="WGS84") # creates a geodetic object that works on an ellipsoid, not a plane.
        
        # If the CRS is geographic, mark to use the geodesic method
        self.is_geographic = self.crs.is_geographic
        
       
    
    # Class Methods
    # Identify the intersection point
    def get_intersection_point(self):
        """Returns the intersection point between lines."""
        # 2. Get the intersection point
        intersection = self.line1.intersection(self.line2)
        
        return intersection if intersection.geom_type == "Point" else None
        
    # calculate internal angle between 2 linestrings
    def angle_between_lines(self):        
        """
        Internal angle computation between two lines.
        Returns the angle in dgrees (0°-180°).
        """
        intersection = self.get_intersection_point()
        if not intersection:
            return None

        # Neighboring points on each line
        p1 = self.get_neighbor(self.line1, intersection)
        p2 = self.get_neighbor(self.line2, intersection)

        # -------------------------------------------------------------
        # GEODESIC MODE (geographic coordinates)
        # -------------------------------------------------------------
        if self.is_geographic:
            lon0, lat0 = intersection.x, intersection.y
            lon1, lat1 = p1.x, p1.y
            lon2, lat2 = p2.x, p2.y

            # Calculate azimuths from the intersection point toward each line
            az1, _, _ = self.geod.inv(lon0, lat0, lon1, lat1)
            az2, _, _ = self.geod.inv(lon0, lat0, lon2, lat2)

            # Absolute angular difference
            diff = abs(az2 - az1)
            if diff > 180:
                diff = 360 - diff

            return diff

        # -------------------------------------------------------------
        # PLANAR TRYGONOMETRY MODE (projected coordinates)
        # -------------------------------------------------------------
        else:
            x0, y0 = intersection.x, intersection.y
            v1 = (p1.x - x0, p1.y - y0)
            v2 = (p2.x - x0, p2.y - y0)

            dot = v1[0] * v2[0] + v1[1] * v2[1]
            norm1 = math.sqrt(v1[0]**2 + v1[1]**2)
            norm2 = math.sqrt(v2[0]**2 + v2[1]**2)

            cos_theta = max(-1, min(1, dot / (norm1 * norm2)))
            return math.degrees(math.acos(cos_theta))
    
    # Identify the neighbor point of the intersection point
    def get_neighbor(self,line: LineString, intersection_point: Point):# line in geometry format
        """
        Returns the neihboring point to the intersection point, along a line.
        It is used to define the direction of each line.
        """
        
        
        coords = list(line.coords)
        
        # Get the index of the vertex
        nearest_idx = min(range(len(coords)),key=lambda i: intersection_point.distance(Point(coords[i])))
        
        # Select the neighbor point
        if nearest_idx == 0:
            neighbor_point = coords[1]
        elif nearest_idx == len(coords) -1:
            neighbor_point = coords[-2]
        else:
            # TTake the closest one between the previous and the next
            previous_point = Point(coords[nearest_idx -1])
            next_point = Point(coords[nearest_idx + 1])
            neighbor_point = previous_point if intersection_point.distance(previous_point) < intersection_point.distance(next_point) else next_point
            
        return Point(neighbor_point)