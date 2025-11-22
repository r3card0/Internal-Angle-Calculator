# Internal Angle Calculator

A Python class for calculating the internal angle between two intersecting LineStrings with automatic method selection based on coordinate reference system (CRS)

# 📊 Overview

**Purpose**

The `InternalAngle` class calculates the internal angle formed by two intersecting linear geometries (roads, paths, lines) by automatically selecting the most appropiate calculation methods:

* Geodesic calculation for geographic coordinates (longitude/latitude)
* Planar trigonometry for projected coordinates (meters, feet, etc)

**Key Features**

* 🌎 Automatic detection of coordinate system type (geographic vs projected)
* 📐 Precise angle calculation using geodesic methods for lon/lat data
* 🎯 Handles Well-Known Text (WKT) format input
* 🔄 Neighbor point selection for direction determination
* ✅ Returns angles in degrees (0° to 180°)

**Uses Cases**
* Road intersection angle assessment
* Transportation network analysis
* Urban planning and design validation
* Geometric quality contro of spatial datasets
* Infraestructure engineering calculations

# 🚀 Getting Ready

**Prerequisites**

You can use this repository in two different ways:

1. Clone the repository

    Follows the steps below to clone and work directly with the source code

    Clone repository
    ```bash
    git clone https://github.com/r3card0/Internal-Angle-Calculator.git
    ```

2. Install as a dependency

    Alternatively, you can install this repository as a dependency within your own project:

    1. Create a Python virtual environment

        ```python
        python3 -m venv <virtual_env_name>
        ```

    2. Activate virtual environment
        
        ```python
        source <virtual_env_name>/bin/activate
        ```

    3. Install libraries `shapely and `pyproj`

        ```bash
        pip install shapely pyproj
        ```

        **Required Libraries**

         * `shapely` - Geometry handling
         * `pyproj` - Coordinate system transformations and geodesic calculations

        and install repository as a dependency:

        ```bash
        pip install git+https://github.com/r3card0/Internal-Angle-Calculator.git@v0.1.0
        ```

**Basic Usage**

### 1. Initialize the Class

```python
from internal_angle_calculator import InternalAngle

# WKT format LineString
line1_wkt = "LINESTRING(-99.5 27.5, -99.4 27.6)"
line2_wkt = "LINESTRING(-99.45 27.4, -99.45 27.7)"

# Create instance (default CRS is EPSG:4326 - WGS84)
angle_calculation = InternalAngle(line1_wkt, line2_wkt, crs="EPSG:4326")
```

### 2. Calculate the Internal Angle

```python
# Get the angle in degrees
angle = angle_calculation.angle_between_lines()
print(f"Internal angle: {angle:.2f}°")
```

### 3. Get Intersection Point

```python
# Retrieve the intersection point
intersection = angle_calculation.get_intersection_point()
if intersection:
    print(f"Intersection coordinates: {intersection.x}, {intersection.y}")
```

**Working with DataFrames**

if you have a dataset with multiple pairs of LineStrings:

```python
import pandas as pd
from internal_angle_calculator import InternalAngle

# Sample DataFrame
data = {
    'road_1': [
        "LINESTRING(-99.5 27.5, -99.4 27.6)",
        "LINESTRING(-100.0 28.0, -100.1 28.1)"
    ],
    'road_2': [
        "LINESTRING(-99.45 27.4, -99.45 27.7)",
        "LINESTRING(-100.05 27.9, -100.05 28.2)"
    ]
}

df = pd.DataFrame(data)

# Calculate angles for each row
def calculate_angle(row):
    calc = InternalAngle(row['road_1'], row['road_2'], crs="EPSG:4326")
    return calc.angle_between_lines()

df['internal_angle'] = df.apply(calculate_angle, axis=1)
print(df)
```

**Coordinate Reference Systems**

**Geographic Coordinates (Geodesic Method)**

```python
# Using WGS84 (lat/lon)
angle_calculation = InternalAngle(line1_wkt, line2_wkt, crs="EPSG:4326")
```

**Projectes Coordinates (Planar Method)**

```python
# Using UTM Zone 14N
angle_calculation = InternalAngle(line1_wkt, line2_wkt, crs="EPSG:32614")

# Using Web Mercator
angle_calculation = InternalAngle(line1_wkt, line2_wkt, crs="EPSG:3857")
```

### Class Methods
|Method|Description|Returns|
|-|-|-|
|`get_intersection_point()`|Finds the intersection point between the two lines|`Point` object or `None`|
|`angle_between_lines()`|Calculates the internal angle between lines|`float` (degrees) or `None`|
|`get_neighbor(line, intersection_point)`|Identifies the neighbor point to determine line direction|`Point` object|

**Technical Details**

**Geodesic Calculation (Geographic CRS)**

* Uses `pyproj.Geod` with WGS84 ellipsoid
* Calculates forward azimuth from intersection point to neighbor points
* Computes angular difference between azimuth bearings
* Handles wraparound for angles > 180°

**Planar Calculation (Projected CRS)**

* Uses vector dot product and norms
* Applies inverse cosine to calculate angle
* Clamps cosine values to [-1,1] to avoid numerical errors
* Efficient for large datasets with projected coordinates

Example output

```python
# Example with real data
line1 = "LINESTRING(-99.508 27.544, -99.489 27.558)"
line2 = "LINESTRING(-99.500 27.540, -99.500 27.560)"

calc = InternalAngle(line1, line2)
angle = calc.angle_between_lines()
intersection = calc.get_intersection_point()

print(f"Internal Angle: {angle:.2f}°")
print(f"Intersection: ({intersection.x:.4f}, {intersection.y:.4f})")
```

Output

```bash
Internal Angle: 67.38°
Intersection: (-99.5000, 27.5520)
```

Error Handling

The class returns `None` when:

* Lines do not intersect
* Intersection is not a single point (e.g. overlapping segments)
* Invalid WKT format is provided

```python
angle = angle_calc.angle_between_lines()
if angle is None:
    print("Lines do not intersect at a single point")
else:
    print(f"Angle: {angle:.2f}°")
```

## Contributing
For improvements or bug resports, please submit an issue or pull request to the repository

## Author
[r3car0](https://github.com/r3card0)

Last Update: Nov 2025