from shapely import wkt
from shapely.geometry import Point
import math

class InternalAngle:
    def __init__(self,linestring1:str,linestring2:str):
        # 1. Converts lines WKT format to Shapely Geometry Objects
        self.line1 = wkt.loads(linestring1)
        self.line2 = wkt.loads(linestring2)

     # Identify the intersection point
    def get_intersection_point(self):
        # 2. Find the intersection Point
        intersection = self.line1.intersection(self.line2)
        
        return intersection
    
    # calculate internal angle between 2 linestrings
    def angle_between_lines(self):        
        # Identify the intersection point
        intersection = self.get_intersection_point()
        
        # Evaluates
        if intersection.is_empty or not intersection.geom_type == "Point":
            return None
        
        x0,y0 = intersection.x, intersection.y
        
        # Getting neighbor points
        p1 = self.get_neighbor(self.line1,intersection)
        p2 = self.get_neighbor(self.line2,intersection)
        
        
        # Vectors
        v1 = (p1.x - x0, p1.y - y0)
        v2 = (p2.x - x0, p2.y -y0)
        
        # producto punto
        dot = (v1[0] * v2[0]) + (v1[1] * v2[1])
        norm1 = math.sqrt(v1[0]**2 + v1[1]**2)
        norm2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
        cos_theta = dot / (norm1 * norm2)
        cos_theta = max(-1, min(1, cos_theta))  # 
    
        return math.degrees(math.acos(cos_theta))
    
    # Identify the neighbor point of the intersection point
    def get_neighbor(self,line, intersection_point):# line in geometry format
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