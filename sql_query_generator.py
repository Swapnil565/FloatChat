"""
FloatChat SQL Query Generator
Uses LLM to convert natural language queries into PostgreSQL SQL for ocean data retrieval
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

load_dotenv()

class SQLQueryGenerator:
    def __init__(self):
        self.client = Cerebras(api_key=os.getenv('CEREBRAS_API_KEY'))
        self.database_schema = self._get_database_schema()
        
    def _get_database_schema(self) -> str:
        """Return the database schema information for the LLM"""
        return """
        DATABASE SCHEMA:
        
        Table: argo_floats
        Columns:
        - float_id (INTEGER): Unique identifier for each Argo float
        - latitude (FLOAT): Latitude coordinate (-90 to 90)
        - longitude (FLOAT): Longitude coordinate (-180 to 180)
        - pressure_dbar (FLOAT): Water pressure in decibars (depth indicator)
        - temperature_celsius (FLOAT): Water temperature in Celsius
        - salinity_psu (FLOAT): Salinity in Practical Salinity Units
        - date_time (TIMESTAMP): Date and time of measurement
        - geometry (GEOMETRY): PostGIS geometry point (latitude, longitude)
        
        SPATIAL FUNCTIONS AVAILABLE:
        - ST_DWithin(geometry, ST_Point(lon, lat), distance_km * 1000): Find points within distance
        - ST_Distance(geometry, ST_Point(lon, lat)): Calculate distance in meters
        - ST_Point(longitude, latitude): Create a point geometry
        
        COMMON LOCATIONS (for reference):
        - Mumbai: (19.07, 72.88)
        - Chennai: (13.08, 80.27)
        - Kolkata: (22.57, 88.36)
        - Arabian Sea: (15-25°N, 60-75°E)
        - Bay of Bengal: (5-22°N, 80-100°E)
        - Indian Ocean: (0-30°S, 60-100°E)
        """
    
    def generate_sql_query(self, user_query: str) -> Tuple[str, Dict]:
        """
        Generate SQL query from natural language using LLM
        Returns: (sql_query, metadata)
        """
        
        system_prompt = f"""You are an expert SQL query generator for oceanographic data.
        
        {self.database_schema}
        
        INSTRUCTIONS:
        1. Convert the user's natural language query into a PostgreSQL SQL query
        2. Use appropriate WHERE clauses for filtering
        3. Include spatial queries when locations are mentioned
        4. Limit results to reasonable numbers (max 5000 rows for performance)
        5. Order results logically (by date_time, pressure_dbar, etc.)
        6. Return ONLY the SQL query, no explanations
        
        QUERY PATTERNS:
        - Temperature/Salinity near location: Use ST_DWithin with ~100km radius
        - Profile data: ORDER BY pressure_dbar ASC
        - Time series: ORDER BY date_time ASC
        - Surface data: WHERE pressure_dbar < 50
        - Deep data: WHERE pressure_dbar > 1000
        
        EXAMPLE QUERIES:
        User: "Temperature data near Mumbai"
        SQL: SELECT * FROM argo_floats WHERE ST_DWithin(geometry, ST_SetSRID(ST_Point(72.88, 19.07), 4326), 100000) ORDER BY date_time DESC LIMIT 1000;
        
        User: "Temperature profile for float 5905529"
        SQL: SELECT * FROM argo_floats WHERE float_id = '5905529' ORDER BY pressure_dbar ASC;
        
        User: "Surface temperature in Arabian Sea"
        SQL: SELECT * FROM argo_floats WHERE pressure_dbar < 50 AND latitude BETWEEN 15 AND 25 AND longitude BETWEEN 60 AND 75 ORDER BY date_time DESC LIMIT 2000;
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama3.1-8b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the SQL query
            sql_query = self._clean_sql_query(sql_query)
            
            # Extract metadata from the query
            metadata = self._extract_query_metadata(sql_query, user_query)
            
            return sql_query, metadata
            
        except Exception as e:
            # Fallback to a basic query
            fallback_query = "SELECT * FROM argo_floats ORDER BY date_time DESC LIMIT 1000;"
            metadata = {
                "query_type": "fallback",
                "location": None,
                "parameters": ["temperature", "salinity"],
                "error": str(e)
            }
            return fallback_query, metadata
    
    def _clean_sql_query(self, sql_query: str) -> str:
        """Clean and validate the SQL query"""
        # Remove any markdown formatting
        sql_query = re.sub(r'```sql\n?', '', sql_query)
        sql_query = re.sub(r'```\n?', '', sql_query)
        
        # Fix ST_Point SRID issues - replace ST_Point with ST_SetSRID(ST_Point(...), 4326)
        st_point_pattern = r'ST_Point\(([^)]+)\)'
        
        def replace_st_point(match):
            coords = match.group(1)
            return f'ST_SetSRID(ST_Point({coords}), 4326)'
        
        sql_query = re.sub(st_point_pattern, replace_st_point, sql_query)
        print(f"🔧 Fixed ST_Point SRID in query")
        
        # Ensure it ends with semicolon
        sql_query = sql_query.strip()
        if not sql_query.endswith(';'):
            sql_query += ';'
            
        # Basic security check - prevent dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'TRUNCATE']
        sql_upper = sql_query.upper()
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return "SELECT * FROM argo_floats ORDER BY date_time DESC LIMIT 1000;"
        
        return sql_query
    
    def _extract_query_metadata(self, sql_query: str, user_query: str) -> Dict:
        """Extract metadata from the generated SQL query"""
        metadata = {
            "query_type": "unknown",
            "location": None,
            "parameters": [],
            "depth_range": None,
            "time_constraint": False,
            "spatial_query": False
        }
        
        sql_lower = sql_query.lower()
        user_lower = user_query.lower()
        
        # Detect query type
        if "order by pressure_dbar" in sql_lower:
            metadata["query_type"] = "profile"
        elif "order by date_time" in sql_lower:
            metadata["query_type"] = "time_series"
        elif "st_dwithin" in sql_lower or "st_distance" in sql_lower:
            metadata["query_type"] = "spatial"
            metadata["spatial_query"] = True
        elif "float_id" in sql_lower:
            metadata["query_type"] = "float_specific"
        else:
            metadata["query_type"] = "general"
        
        # Detect parameters
        if "temperature" in user_lower:
            metadata["parameters"].append("temperature")
        if "salinity" in user_lower:
            metadata["parameters"].append("salinity")
        if "pressure" in user_lower or "depth" in user_lower:
            metadata["parameters"].append("pressure")
        
        # Default to temperature if no parameters detected
        if not metadata["parameters"]:
            metadata["parameters"] = ["temperature"]
        
        # Detect location mentions
        locations = ["mumbai", "chennai", "kolkata", "delhi", "bangalore", "goa", "kerala"]
        for location in locations:
            if location in user_lower:
                metadata["location"] = location.title()
                break
        
        # Detect ocean regions
        regions = ["arabian sea", "bay of bengal", "indian ocean"]
        for region in regions:
            if region in user_lower:
                metadata["location"] = region.title()
                break
        
        # Detect depth constraints
        if "surface" in user_lower:
            metadata["depth_range"] = "surface"
        elif "deep" in user_lower:
            metadata["depth_range"] = "deep"
        elif "profile" in user_lower:
            metadata["depth_range"] = "profile"
        
        return metadata

    def get_sample_queries(self) -> List[Dict]:
        """Return sample queries for testing"""
        return [
            {
                "user_query": "Show temperature data near Mumbai",
                "expected_type": "spatial"
            },
            {
                "user_query": "Temperature profile for float 5905529",
                "expected_type": "profile"
            },
            {
                "user_query": "Surface temperature in Arabian Sea",
                "expected_type": "spatial"
            },
            {
                "user_query": "Salinity trends over time near Chennai",
                "expected_type": "time_series"
            },
            {
                "user_query": "Deep water temperature data",
                "expected_type": "general"
            }
        ]

# Test function
def test_sql_generator():
    """Test the SQL query generator"""
    generator = SQLQueryGenerator()
    
    sample_queries = generator.get_sample_queries()
    
    print("🧪 Testing SQL Query Generator\n")
    
    for i, sample in enumerate(sample_queries, 1):
        print(f"Test {i}: {sample['user_query']}")
        sql_query, metadata = generator.generate_sql_query(sample['user_query'])
        print(f"SQL: {sql_query}")
        print(f"Metadata: {metadata}")
        print("-" * 50)

if __name__ == "__main__":
    test_sql_generator()