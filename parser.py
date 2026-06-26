import json
import psycopg2 # or use `pip install supabase`

# Connection properties
DB_HOST = "sgfhjqfkbumsphevxlrc.supabase.co"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "YOUR_SUPABASE_DB_PASSWORD" 

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=5432)
cursor = conn.cursor()

# Load the file locally or download via requests
with open('(R) ORLAND 424 STATES.geojson', 'r') as f:
    geojson_data = json.load(f)

for feature in geojson_data['features']:
    properties = feature['properties']
    geometry = json.dumps(feature['geometry'])
    
    name = properties.get('name', 'Unknown District')
    category = properties.get('category', 'county')
    ref_num = properties.get('id', 'N/A')
    img_link = properties.get('image_link', None) # keeps link string only
    
    # Using ST_GeomFromGeoJSON to write spatial data natively to PostGIS
    query = """
    INSERT INTO orlegeo_map_objects (name, category, reference_number, image_url, geom)
    VALUES (%s, %s, %s, %s, ST_GeomFromGeoJSON(%s));
    """
    cursor.execute(query, (name, category, ref_num, img_link, geometry))

conn.commit()
cursor.close()
conn.close()
print("Orland structural matrix fully updated via Python Script.")
