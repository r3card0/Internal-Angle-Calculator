from shapely import wkt
from shapely.geometry import Point
from pyproj import CRS, Geod
import math

class InternalAngle:
    def __init__(self,linestring1:str,linestring2:str, crs: str="EPSG:4326"):
        # 1. Converts lines WKT format to Shapely Geometry Objects
        self.line1 = wkt.loads(linestring1)
        self.line2 = wkt.loads(linestring2)
        # 2. Set a Geographic System and an Ellipsoid
        self.crs = CRS.from_user_input(crs)
        self.geod = Geod(ellps="WGS84") # Creates a geodetic object, focused in an ellipsoide, not a planar
        # If CRS geographic
        self.is_geographic = self.crs.is_geographic

     # Identify the intersection point
    def get_intersection_point(self):
        # 2. Find the intersection Point
        intersection = self.line1.intersection(self.line2)
        
        return intersection if intersection.geom_type == "Point" else None
    
    # calculate internal angle between 2 linestrings
    def angle_between_lines(self): 
        """
        Calculates the internal angle between two LineStrings
        Returns values of angle degrees (0°-180°)
        """       
        # Identify the intersection point
        intersection = self.get_intersection_point()
        if not intersection:
            return None
        
              
        # Getting neighbor points
        p1 = self.get_neighbor(self.line1,intersection)
        p2 = self.get_neighbor(self.line2,intersection)

        # --------------------------------------------
        # Geodesic Mode (geographic coordinates)
        # --------------------------------------------
        if self.is_geographic:
            lon0, lat0 = intersection.x, intersection.y
            lon1, lat1 = p1.x, p1.y
            lon2, lat2 = p2.x, p2.y

            # Calculates Azimuth from intersection point to each line
            az1, _, _ = self.geod.inv(lon0,lat0,lon1,lat1)
            az2, _, _ = self.geod.inv(lon0,lat0,lon2,lat2)

            # Absolute angular difference
            diff = abs(az2 - az1)
            if diff > 180:
                diff = 360 - diff

            return diff
        
        # --------------------------------------------
        # Planar Mode (geographic coordinates)
        # --------------------------------------------
        else:
            x0, y0 = intersection.x, intersection.y
            # vectors
            v1 = (p1.x - x0, p1.y - y0)
            v2 = (p2.x - x0, p2.y - y0)
        
            # product dot
            dot = (v1[0] * v2[0]) + (v1[1] * v2[1])
            norm1 = math.sqrt(v1[0]**2 + v1[1]**2)
            norm2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
            cos_theta = max(-1, min(1, dot / (norm1 * norm2)))
            return math.degrees(math.acos(cos_theta))
    
    # Identify the neighbor point of the intersection point
    def get_neighbor(self,line, intersection_point):# line in geometry format
        """
        Return the neighbor point of the intersection point from a LineString
        Used to define the direction of the LineString
        """
        coords = list(line.coords)
        
        # Find the vertice index 
        nearest_idx = min(range(len(coords)),key=lambda i: intersection_point.distance(Point(coords[i])))
        
        # Select the neighbor point
        if nearest_idx == 0:
            neighbor_point = coords[1]
        elif nearest_idx == len(coords) -1:
            neighbor_point = coords[-2]
        else:
            
            previous_point = Point(coords[nearest_idx -1])
            next_point = Point(coords[nearest_idx + 1])
            neighbor_point = previous_point if intersection_point.distance(previous_point) < intersection_point.distance(next_point) else next_point
            
        return Point(neighbor_point)