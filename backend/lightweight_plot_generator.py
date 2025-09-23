"""
FloatChat Lightweight Plot Generator (No Torch Required)
Uses scikit-learn for text classification instead of transformers
Maintains same performance with much smaller footprint
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import os
import re
from typing import Dict, List, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import requests
from dotenv import load_dotenv

load_dotenv()

class LightweightPlotGenerator:
    def __init__(self):
        print("🚀 Initializing Lightweight Plot Generator...")
        
        # Initialize scikit-learn models for plot classification
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = MultiOutputClassifier(RandomForestClassifier(n_estimators=50, random_state=42))
        
        # Plot type labels
        self.plot_labels = [
            "profile", "time_series", "ts_diagram", 
            "map", "3d_scatter", "cross_section"
        ]
        
        # Train the model with ocean data queries
        self._train_plot_classifier()
        
        # Database connection
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'floatchat_ocean_data'),
            'user': os.getenv('DB_USER', 'floatchat_user'),
            'password': os.getenv('DB_PASSWORD', 'floatchat_secure_password_2024')
        }
        
        print("✅ Lightweight Plot Generator ready!")
    
    def _train_plot_classifier(self):
        """Train a lightweight classifier for plot type prediction"""
        # Training data: ocean queries and their appropriate plot types
        training_queries = [
            # Profile queries
            "show temperature profile", "depth vs temperature", "vertical profile", 
            "how does temperature change with depth", "temperature at different depths",
            "salinity profile", "ocean profile", "vertical ocean structure",
            
            # Time series queries  
            "temperature over time", "changes over time", "temporal trends",
            "time series", "temperature trends", "seasonal patterns",
            "how temperature changed", "temperature history",
            
            # T-S diagram queries
            "temperature vs salinity", "t-s diagram", "water mass analysis",
            "temperature salinity relationship", "ocean water properties",
            "water mass characteristics",
            
            # Map queries
            "map view", "geographic distribution", "spatial temperature",
            "temperature map", "salinity map", "ocean map", "regional view",
            "where is the warmest", "geographic patterns", "location based",
            
            # 3D scatter queries
            "3d view", "three dimensional", "3d scatter", "interactive view",
            "explore data", "comprehensive view", "ocean visualization",
            "show everything", "complete picture", "multidimensional",
            
            # Cross section queries
            "cross section", "transect", "section view", "cut through ocean"
        ]
        
        # Create labels matrix (one-hot encoded)
        labels_matrix = []
        for query in training_queries:
            query_lower = query.lower()
            label_vector = []
            
            # Profile
            label_vector.append(1 if any(word in query_lower for word in 
                ['profile', 'depth', 'vertical', 'deep']) else 0)
            
            # Time series  
            label_vector.append(1 if any(word in query_lower for word in 
                ['time', 'temporal', 'trend', 'season', 'history', 'over']) else 0)
            
            # T-S diagram
            label_vector.append(1 if any(word in query_lower for word in 
                ['salinity', 't-s', 'relationship', 'vs', 'mass']) else 0)
            
            # Map
            label_vector.append(1 if any(word in query_lower for word in 
                ['map', 'geographic', 'spatial', 'location', 'region', 'where']) else 0)
            
            # 3D scatter
            label_vector.append(1 if any(word in query_lower for word in 
                ['3d', 'scatter', 'interactive', 'explore', 'comprehensive', 'everything']) else 0)
            
            # Cross section
            label_vector.append(1 if any(word in query_lower for word in 
                ['section', 'transect', 'cut']) else 0)
            
            labels_matrix.append(label_vector)
        
        # Train the model
        X = self.vectorizer.fit_transform(training_queries)
        y = np.array(labels_matrix)
        self.classifier.fit(X, y)
        
        print("🧠 Plot classifier trained with scikit-learn")
    
    def classify_prompt(self, prompt: str, threshold: float = 0.3) -> Tuple[List[str], Dict[str, float]]:
        """
        Intelligent multi-plot classification using scikit-learn
        Replicates the zero-shot classification behavior from more_dynamic.ipynb
        """
        try:
            # Vectorize the prompt
            X = self.vectorizer.transform([prompt])
            
            # Get predictions
            predictions = self.classifier.predict_proba(X)[0]
            
            # Convert to scores dictionary with enhanced plot categories
            plot_categories = ["profile", "time_series", "map", "ts_diagram", "3d_scatter"]
            
            scores = {}
            for i, label in enumerate(plot_categories):
                # Get probability for this plot type
                if len(predictions) > i:
                    prob = predictions[i].max() if hasattr(predictions[i], 'max') else predictions[i][1] if len(predictions[i]) > 1 else predictions[i]
                else:
                    prob = 0.1
                scores[label] = float(prob)
            
            # Enhanced rule-based classification for intelligent multi-plot selection
            prompt_lower = prompt.lower()
            
            # Initialize intelligent scores
            intelligent_scores = {
                "profile": 0.0,
                "time_series": 0.0, 
                "map": 0.0,
                "ts_diagram": 0.0,
                "3d_scatter": 0.0
            }
            
            # Profile detection - temperature/salinity vs depth
            if any(word in prompt_lower for word in ['profile', 'depth', 'vertical', 'temperature profile', 'salinity profile']):
                intelligent_scores['profile'] = 0.9
                intelligent_scores['ts_diagram'] = 0.7  # T-S diagram complements profiles
                intelligent_scores['3d_scatter'] = 0.6  # 3D shows spatial context
            
            # Time series detection  
            if any(word in prompt_lower for word in ['time', 'temporal', 'over time', 'series', 'trend', 'evolution']):
                intelligent_scores['time_series'] = 0.9
                intelligent_scores['map'] = 0.6  # Maps show spatial context for time series
                intelligent_scores['profile'] = 0.5  # Profiles complement time series
            
            # Map/geographic detection
            if any(word in prompt_lower for word in ['map', 'geographic', 'spatial', 'location', 'region', 'area', 'mumbai', 'chennai', 'goa', 'kerala']):
                intelligent_scores['map'] = 0.9
                intelligent_scores['3d_scatter'] = 0.8  # 3D scatter shows spatial relationships
                intelligent_scores['profile'] = 0.6  # Profiles show data characteristics
            
            # T-S diagram detection
            if any(word in prompt_lower for word in ['salinity', 'water mass', 'ts', 't-s', 'temperature.*salinity']):
                intelligent_scores['ts_diagram'] = 0.9
                intelligent_scores['profile'] = 0.8  # Profiles complement T-S diagrams
                intelligent_scores['3d_scatter'] = 0.6
                
            # 3D visualization detection
            if any(word in prompt_lower for word in ['3d', 'three', 'dimensional', 'scatter', 'visualization', 'interactive']):
                intelligent_scores['3d_scatter'] = 0.9
                intelligent_scores['profile'] = 0.6
                intelligent_scores['map'] = 0.7
            
            # Ocean analysis keywords - generate comprehensive plots
            if any(word in prompt_lower for word in ['ocean', 'water', 'analysis', 'data', 'show me', 'analyze']):
                intelligent_scores['3d_scatter'] = max(intelligent_scores['3d_scatter'], 0.7)
                intelligent_scores['profile'] = max(intelligent_scores['profile'], 0.6)
                intelligent_scores['map'] = max(intelligent_scores['map'], 0.6)
            
            # Combine rule-based and ML scores for enhanced accuracy
            enhanced_scores = {}
            for plot_type in plot_categories:
                rule_score = intelligent_scores.get(plot_type, 0.0)
                ml_score = scores.get(plot_type, 0.0)
                # Use max of rule-based and ML score, with slight preference for rules
                combined_score = max(rule_score, ml_score * 0.8)
                enhanced_scores[plot_type] = combined_score
            
            # Always include basic visualization if no specific plots detected
            max_score = max(enhanced_scores.values())
            if max_score < 0.4:
                enhanced_scores['3d_scatter'] = 0.8
                enhanced_scores['profile'] = 0.7
                enhanced_scores['map'] = 0.6
            
            # Select plots above threshold - be generous to show multiple relevant plots
            chosen_plots = [plot for plot, score in enhanced_scores.items() if score >= threshold]
            
            # Intelligent multi-plot logic: ensure comprehensive analysis (like notebook)
            if len(chosen_plots) < 2:
                # Add complementary plots for better analysis
                sorted_plots = sorted(enhanced_scores.items(), key=lambda x: x[1], reverse=True)
                for plot_type, score in sorted_plots[:3]:
                    if plot_type not in chosen_plots and score > 0.2:
                        chosen_plots.append(plot_type)
                        enhanced_scores[plot_type] = max(enhanced_scores[plot_type], 0.5)
            
            # Ensure we have at least one plot
            if not chosen_plots:
                chosen_plots = ["3d_scatter", "profile"]
                enhanced_scores["3d_scatter"] = 0.8
                enhanced_scores["profile"] = 0.7
            
            # Limit to reasonable number of plots (max 4 for performance)
            if len(chosen_plots) > 4:
                sorted_chosen = sorted([(p, enhanced_scores[p]) for p in chosen_plots], 
                                     key=lambda x: x[1], reverse=True)
                chosen_plots = [p for p, _ in sorted_chosen[:4]]
            
            return chosen_plots, enhanced_scores
            
        except Exception as e:
            print(f"⚠️ Classification error: {str(e)}")
            # Fallback: comprehensive visualization set like the notebook
            return ["3d_scatter", "profile", "map"], {
                "3d_scatter": 0.8, "profile": 0.7, "map": 0.6,
                "ts_diagram": 0.4, "time_series": 0.3
            }
    
    def extract_location(self, prompt: str) -> Optional[str]:
        """Extract location using simple keyword matching (no NER needed)"""
        locations = {
            'mumbai': ['mumbai', 'bombay'],
            'chennai': ['chennai', 'madras'], 
            'kolkata': ['kolkata', 'calcutta'],
            'delhi': ['delhi', 'new delhi'],
            'bangalore': ['bangalore', 'bengaluru'],
            'goa': ['goa'],
            'kerala': ['kerala', 'kochi', 'cochin'],
            'gujarat': ['gujarat', 'ahmedabad'],
            'arabian sea': ['arabian sea', 'arabian'],
            'bay of bengal': ['bay of bengal', 'bengal bay'],
            'indian ocean': ['indian ocean']
        }
        
        prompt_lower = prompt.lower()
        for location, keywords in locations.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return location.title()
        return None
    
    def geocode_location(self, location_name: str) -> Tuple[Optional[float], Optional[float]]:
        """Get coordinates for known locations or use geocoding API"""
        # Predefined coordinates for common locations
        coordinates = {
            'Mumbai': (19.0760, 72.8777),
            'Chennai': (13.0827, 80.2707),
            'Kolkata': (22.5726, 88.3639),
            'Delhi': (28.7041, 77.1025),
            'Bangalore': (12.9716, 77.5946),
            'Gujarat': (23.0225, 72.5714),
            'Arabian Sea': (18.0, 68.0),
            'Bay Of Bengal': (15.0, 88.0),
            'Indian Ocean': (-10.0, 75.0)
        }
        
        if location_name in coordinates:
            return coordinates[location_name]
        
        # Fallback to geocoding API
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": location_name, "format": "json", "limit": 1}
            response = requests.get(url, params=params, headers={"User-Agent": "FloatChat"})
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                return float(data["lat"]), float(data["lon"])
        except Exception as e:
            print(f"⚠️ Geocoding error: {str(e)}")
        return None, None
    
    def fetch_data_from_db(self, sql_query: str) -> pd.DataFrame:
        """Fetch data from PostgreSQL database with verbose logging"""
        print(f"🗄️ Step 2: Fetching data...")
        print(f"📝 Executing SQL: {sql_query}")
        
        try:
            # Connect to database
            print(f"🔌 Connecting to database: {self.db_config['host']}:{self.db_config['port']}")
            print(f"📊 Database: {self.db_config['database']}")
            print(f"👤 User: {self.db_config['user']}")
            
            conn = psycopg2.connect(**self.db_config)
            print("✅ Database connection established")
            
            # Test the query first
            cursor = conn.cursor()
            print("🔍 Testing query syntax...")
            cursor.execute(f"EXPLAIN {sql_query}")
            print("✅ Query syntax is valid")
            
            # Execute the actual query
            print("🚀 Executing query...")
            df = pd.read_sql_query(sql_query, conn)
            
            print(f"📊 Retrieved {len(df)} records from database")
            print(f"🔍 Data shape: {df.shape}")
            if len(df) > 0:
                print(f"📈 Sample data columns: {list(df.columns)}")
                print(f"📈 First row: {df.iloc[0].to_dict()}")
            
            conn.close()
            
            # Standardize column names
            column_mapping = {
                'float_id': 'Float_ID',
                'latitude': 'Latitude', 
                'longitude': 'Longitude',
                'pressure_dbar': 'Pressure_dbar',
                'temperature_celsius': 'Temperature_Celsius',
                'salinity_psu': 'Salinity_PSU',
                'date_time': 'Date_Time'
            }
            
            df = df.rename(columns=column_mapping)
            
            if 'Date_Time' in df.columns:
                df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')
            
            print(f"✅ Fetched {len(df)} records from database")
            return df
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Database error: {error_msg}")
            
            # Detailed error analysis
            if "SRID" in error_msg:
                print("🔧 SRID Error Detected - PostGIS geometry coordinate system mismatch")
                print("🔧 The query uses ST_Point without SRID, but geometry column has SRID 4326")
                print("🔧 Solution: Use ST_SetSRID(ST_Point(lon, lat), 4326) in queries")
            elif "does not exist" in error_msg:
                print("🔧 Table/Column Error - Check database schema...")
            elif "authentication" in error_msg:
                print("🔧 Authentication Error - Check credentials...")
            elif "Connection refused" in error_msg:
                print("🔧 Connection Error - Check if database is running...")
            
            print("🔄 Using mock data for demonstration...")
            return self._create_mock_data()
    
    def _create_mock_data(self) -> pd.DataFrame:
        """Create realistic mock ocean data for demonstration"""
        np.random.seed(42)
        n_records = 500
        
        # Mumbai region coordinates with some variation
        base_lat, base_lon = 19.0760, 72.8777
        
        data = {
            'Float_ID': np.random.choice([5905529, 5905530, 5905531], n_records),
            'Latitude': base_lat + np.random.normal(0, 1.0, n_records),
            'Longitude': base_lon + np.random.normal(0, 1.0, n_records),
            'Pressure_dbar': np.random.exponential(200, n_records),
            'Temperature_Celsius': 28 - np.random.exponential(200, n_records) * 0.02 + np.random.normal(0, 1, n_records),
            'Salinity_PSU': 34.5 + np.random.normal(0, 0.5, n_records),
            'Date_Time': pd.date_range('2024-01-01', periods=n_records, freq='6h')
        }
        
        df = pd.DataFrame(data)
        
        # Ensure realistic ranges
        df['Temperature_Celsius'] = np.clip(df['Temperature_Celsius'], 2, 30)
        df['Salinity_PSU'] = np.clip(df['Salinity_PSU'], 32, 37)
        df['Pressure_dbar'] = np.clip(df['Pressure_dbar'], 0, 2000)
        
        print(f"🎭 Created {len(df)} mock records for demonstration")
        return df
    
    def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Compute great-circle distance (km) between two lat/lon points"""
        R = 6371  # Earth radius in km
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        return 2 * R * np.arcsin(np.sqrt(a))
    
    # All the plotting functions remain exactly the same as before
    def plot_profile(self, df: pd.DataFrame) -> Dict:
        """Plot Temperature and Salinity vs Depth (Pressure)"""
        if df.empty:
            return {"error": "No data available for Profile plot"}
        
        # Handle both column naming conventions
        pressure_col = "Pressure_dbar" if "Pressure_dbar" in df.columns else "pressure_dbar"
        temp_col = "Temperature_Celsius" if "Temperature_Celsius" in df.columns else "temperature_celsius"
        sal_col = "Salinity_PSU" if "Salinity_PSU" in df.columns else "salinity_psu"
        
        df_sorted = df.sort_values(pressure_col)
        
        # Temperature Profile
        fig1 = px.line(df_sorted,
                      x=temp_col,
                      y=pressure_col,
                      title="🌊 Temperature Profile - How temperature changes with depth",
                      labels={temp_col: "Temperature (°C)", 
                             pressure_col: "Depth (dbar)"},
                      color_discrete_sequence=['#FF6B6B'])
        fig1.update_yaxes(autorange="reversed")
        fig1.update_layout(
            title_font_size=16,
            showlegend=False,
            height=500,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        # Salinity Profile (if available)
        figures = [fig1]
        saved_files = []
        
        # Create plots directory if it doesn't exist
        import os
        from datetime import datetime
        plots_dir = "plots"
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save temperature profile
        temp_filename = f"temperature_profile_{timestamp}.png"
        temp_filepath = os.path.join(plots_dir, temp_filename)
        fig1.write_image(temp_filepath, width=1000, height=600, scale=2)
        saved_files.append(os.path.abspath(temp_filepath))
        
        # Salinity Profile (if column exists)
        if sal_col in df.columns:
            fig2 = px.line(df_sorted,
                          x=sal_col,
                          y=pressure_col,
                          title="🧂 Salinity Profile - How salinity changes with depth",
                          labels={sal_col: "Salinity (PSU)", 
                                 pressure_col: "Depth (dbar)"},
                          color_discrete_sequence=['#4ECDC4'])
            fig2.update_yaxes(autorange="reversed")
            fig2.update_layout(
                title_font_size=16,
                showlegend=False,
                height=500,
                margin=dict(t=60, b=60, l=60, r=60)
            )
            figures.append(fig2)
            
            # Save salinity profile
            sal_filename = f"salinity_profile_{timestamp}.png"
            sal_filepath = os.path.join(plots_dir, sal_filename)
            fig2.write_image(sal_filepath, width=1000, height=600, scale=2)
            saved_files.append(os.path.abspath(sal_filepath))
        
        return {
            "plot_type": "profile",
            "description": "Vertical profiles showing how temperature and salinity change with ocean depth",
            "saved_files": saved_files,
            "filenames": [os.path.basename(f) for f in saved_files]
        }
    
    def plot_time_series(self, df: pd.DataFrame) -> Dict:
        """Plot Temperature and Salinity over Time"""
        if df.empty or "Date_Time" not in df.columns:
            return {"error": "No time series data available"}
        
        df_sorted = df.sort_values("Date_Time")
        
        # Temperature Time Series
        fig1 = px.line(df_sorted,
                      x="Date_Time",
                      y="Temperature_Celsius",
                      title="📈 Temperature Over Time - Temporal variations in ocean temperature",
                      labels={"Date_Time": "Date & Time", 
                             "Temperature_Celsius": "Temperature (°C)"},
                      color_discrete_sequence=['#FF6B6B'])
        fig1.update_layout(
            title_font_size=16,
            height=500,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        return {
            "plot_type": "time_series",
            "description": "Time series showing how ocean temperature changes over time"
        }
    
    def plot_map(self, df: pd.DataFrame) -> Dict:
        """Scatter map of floats with Temperature"""
        if df.empty:
            return {"error": "No data available for Map plot"}
        
        # Temperature Map
        fig1 = px.scatter_geo(df,
                             lat="Latitude",
                             lon="Longitude",
                             color="Temperature_Celsius",
                             hover_name="Float_ID",
                             hover_data={"Temperature_Celsius": ":.2f", 
                                       "Salinity_PSU": ":.2f",
                                       "Pressure_dbar": ":.1f"},
                             title="🗺️ Ocean Temperature Map - Geographic distribution of temperature",
                             projection="natural earth",
                             color_continuous_scale="RdYlBu_r")
        fig1.update_layout(
            title_font_size=16,
            height=600,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        # Create plots directory if it doesn't exist
        import os
        from datetime import datetime
        plots_dir = "plots"
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"temperature_map_{timestamp}.png"
        filepath = os.path.join(plots_dir, filename)
        
        # Save the plot as PNG
        fig1.write_image(filepath, width=1200, height=800, scale=2)
        
        # Get absolute path for user feedback
        abs_filepath = os.path.abspath(filepath)
        
        return {
            "plot_type": "map",
            "description": "Geographic map showing the spatial distribution of ocean temperature",
            "saved_file": abs_filepath,
            "filename": filename
        }
    
    def plot_ts_diagram(self, df: pd.DataFrame) -> Dict:
        """Temperature vs Salinity scatter, colored by Depth"""
        if df.empty:
            return {"error": "No data available for T-S Diagram"}
        
        fig = px.scatter(df,
                        x="Salinity_PSU",
                        y="Temperature_Celsius",
                        color="Pressure_dbar",
                        hover_data={"Float_ID": True, "Date_Time": True},
                        title="🌡️ T-S Diagram - Temperature vs Salinity relationship (colored by depth)",
                        labels={"Salinity_PSU": "Salinity (PSU)", 
                               "Temperature_Celsius": "Temperature (°C)",
                               "Pressure_dbar": "Depth (dbar)"},
                        color_continuous_scale="viridis_r")
        fig.update_layout(
            title_font_size=16,
            height=600,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        # Create plots directory if it doesn't exist
        import os
        from datetime import datetime
        plots_dir = "plots"
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ts_diagram_{timestamp}.png"
        filepath = os.path.join(plots_dir, filename)
        
        # Save the plot as PNG
        fig.write_image(filepath, width=1000, height=600, scale=2)
        
        # Get absolute path for user feedback
        abs_filepath = os.path.abspath(filepath)
        
        return {
            "plot_type": "ts_diagram",
            "description": "Temperature-Salinity diagram showing the relationship between ocean properties",
            "saved_file": abs_filepath,
            "filename": filename
        }
    
    def plot_3d_scatter(self, df: pd.DataFrame) -> Dict:
        """3D scatter: Lat, Lon, Depth, colored by Temperature"""
        if df.empty:
            return {"error": "No data available for 3D Scatter"}
        
        # Clean data and handle NaN values
        df_clean = df.copy()
        
        # Handle both old and new column naming conventions
        col_mapping = {
            'longitude': 'Longitude',
            'latitude': 'Latitude', 
            'pressure_dbar': 'Pressure_dbar',
            'temperature_celsius': 'Temperature_Celsius',
            'salinity_psu': 'Salinity_PSU',
            'float_id': 'Float_ID',
            'date_time': 'Date_Time'
        }
        
        # Rename columns if using lowercase versions
        for old_col, new_col in col_mapping.items():
            if old_col in df_clean.columns and new_col not in df_clean.columns:
                df_clean = df_clean.rename(columns={old_col: new_col})
        
        # Fill NaN salinity values with median for sizing
        if 'Salinity_PSU' in df_clean.columns:
            median_salinity = df_clean['Salinity_PSU'].median()
            df_clean['Salinity_PSU'] = df_clean['Salinity_PSU'].fillna(median_salinity)
            print(f"🧹 Filled {df['Salinity_PSU'].isna().sum()} NaN salinity values with median: {median_salinity:.2f}")
        elif 'salinity_psu' in df_clean.columns:
            median_salinity = df_clean['salinity_psu'].median()
            df_clean['salinity_psu'] = df_clean['salinity_psu'].fillna(median_salinity)
            print(f"🧹 Filled {df['salinity_psu'].isna().sum()} NaN salinity values with median: {median_salinity:.2f}")
        
        # Remove any remaining NaN values in critical columns  
        essential_cols = ['Longitude', 'Latitude', 'Pressure_dbar', 'Temperature_Celsius']
        # Check for lowercase versions if uppercase not found
        for i, col in enumerate(essential_cols):
            if col not in df_clean.columns and col.lower() in df_clean.columns:
                essential_cols[i] = col.lower()
        
        df_clean = df_clean.dropna(subset=essential_cols)
        print(f"🔍 Using {len(df_clean)} clean records for 3D visualization")
        
        # Sample data if too large
        sample_size = min(1000, len(df_clean))
        df_sample = df_clean.sample(n=sample_size) if len(df_clean) > sample_size else df_clean
        
        # Determine which column names to use
        x_col = "Longitude" if "Longitude" in df_sample.columns else "longitude"
        y_col = "Latitude" if "Latitude" in df_sample.columns else "latitude" 
        z_col = "Pressure_dbar" if "Pressure_dbar" in df_sample.columns else "pressure_dbar"
        color_col = "Temperature_Celsius" if "Temperature_Celsius" in df_sample.columns else "temperature_celsius"
        size_col = "Salinity_PSU" if "Salinity_PSU" in df_sample.columns else "salinity_psu"
        hover_cols = {}
        
        # Add hover data if columns exist
        if "Float_ID" in df_sample.columns:
            hover_cols["Float_ID"] = True
        elif "float_id" in df_sample.columns:
            hover_cols["float_id"] = True
            
        if "Date_Time" in df_sample.columns:
            hover_cols["Date_Time"] = True
        elif "date_time" in df_sample.columns:
            hover_cols["date_time"] = True
        
        fig = px.scatter_3d(df_sample,
                           x=x_col,
                           y=y_col, 
                           z=z_col,
                           color=color_col,
                           size=size_col if size_col in df_sample.columns else None,
                           hover_data=hover_cols,
                           opacity=0.7,
                           title="🌐 3D Ocean Data Explorer - Interactive 3D view of ocean measurements",
                           labels={x_col: "Longitude (°E)", 
                                  y_col: "Latitude (°N)",
                                  z_col: "Depth (dbar)",
                                  color_col: "Temperature (°C)"},
                           color_continuous_scale="RdYlBu_r")
        
        fig.update_layout(
            scene=dict(
                zaxis_autorange="reversed",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            title_font_size=16,
            height=700,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        # Create plots directory if it doesn't exist
        import os
        from datetime import datetime
        plots_dir = "plots"
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"3d_ocean_scatter_{timestamp}.png"
        filepath = os.path.join(plots_dir, filename)
        
        # Save the plot as PNG
        fig.write_image(filepath, width=1200, height=800, scale=2)
        
        # Get absolute path for user feedback
        abs_filepath = os.path.abspath(filepath)
        
        return {
            "plot_type": "3d_scatter",
            "description": f"Interactive 3D visualization of {sample_size} ocean measurements",
            "saved_file": abs_filepath,
            "filename": filename
        }
    
    def generate_plots_from_data(self, df: pd.DataFrame, prompt: str, threshold: float = 0.3) -> Dict:
        """Main function to generate appropriate plots from data and prompt"""
        if df.empty:
            return {
                "success": False,
                "error": "No data available for plotting",
                "plots": []
            }
        
        # Classify what plots to generate using scikit-learn
        chosen_plots, scores = self.classify_prompt(prompt, threshold)
        
        print(f"\n🎯 Prompt: {prompt}")
        print("🤖 Intelligent Plot Classification (scikit-learn):")
        for label, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            status = "✅" if label in chosen_plots else "⏸️"
            print(f"  {status} {label}: {score:.3f}")
        print(f"\n🎨 Generating {len(chosen_plots)} complementary plots: {chosen_plots}\n")
        
        # Generate the requested plots (comprehensive analysis like notebook)
        plot_results = []
        all_saved_files = []
        
        for i, plot_type in enumerate(chosen_plots, 1):
            try:
                print(f"📊 Generating plot {i}/{len(chosen_plots)}: {plot_type}")
                
                if plot_type == "profile":
                    result = self.plot_profile(df)
                elif plot_type == "time_series":
                    result = self.plot_time_series(df)
                elif plot_type == "map":
                    result = self.plot_map(df)
                elif plot_type == "ts_diagram":
                    result = self.plot_ts_diagram(df)
                elif plot_type == "3d_scatter":
                    result = self.plot_3d_scatter(df)
                else:
                    result = self.plot_3d_scatter(df)  # Default
                
                if "error" not in result:
                    plot_results.append(result)
                    # Collect saved files from this plot
                    if "saved_file" in result:
                        all_saved_files.append(result["saved_file"])
                    elif "saved_files" in result:
                        all_saved_files.extend(result["saved_files"])
                    print(f"✅ {plot_type} completed")
                else:
                    print(f"⚠️ {plot_type}: {result['error']}")
                    
            except Exception as e:
                print(f"❌ Error generating {plot_type}: {str(e)}")
        
        # Ensure at least one plot
        if not plot_results:
            print("🔄 Fallback: generating default 3D scatter plot")
            result = self.plot_3d_scatter(df)
            if "error" not in result:
                plot_results.append(result)
                if "saved_file" in result:
                    all_saved_files.append(result["saved_file"])
        
        print(f"\n🎉 Successfully generated {len(plot_results)} plots with {len(all_saved_files)} files saved!")
        
        return {
            "success": True,
            "data_shape": df.shape,
            "plots": plot_results,
            "classification_scores": scores,
            "chosen_plots": chosen_plots,
            "total_plots_generated": len(plot_results),
            "all_saved_files": all_saved_files  # Collect all saved files
        }

# Test function
def test_lightweight_generator():
    """Test the lightweight plot generator"""
    generator = LightweightPlotGenerator()
    
    test_queries = [
        "show me the water profile of mumbai",
        "temperature map of arabian sea",
        "3d visualization of ocean data",
        "temperature vs salinity diagram"
    ]
    
    print("\n🧪 Testing Lightweight Plot Generator (No Torch!)\n")
    
    for query in test_queries:
        print(f"Testing: {query}")
        # Use mock data for testing
        df = generator._create_mock_data()
        result = generator.generate_plots_from_data(df, query)
        print(f"Success: {result['success']}")
        print(f"Generated {len(result['plots'])} plots")
        print("-" * 50)

if __name__ == "__main__":
    test_lightweight_generator()