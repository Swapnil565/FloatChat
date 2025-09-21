#!/usr/bin/env python3
"""
FloatChat Docker System Test
Quick verification that the dockerized system is working correctly
"""

import subprocess
import time
import psycopg2
import requests
from pathlib import Path

def test_docker_containers():
    """Test if Docker containers are running"""
    print("🐳 Testing Docker containers...")
    
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if 'floatchat-postgres' in result.stdout:
            print("✅ PostgreSQL container is running")
            return True
        else:
            print("❌ PostgreSQL container not found")
            return False
    except Exception as e:
        print(f"❌ Docker test failed: {e}")
        return False

def test_database_connection():
    """Test database connectivity and data"""
    print("🗄️ Testing database connection...")
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='floatchat_ocean_data',
            user='floatchat_user',
            password='floatchat_secure_password_2024',
            port=5432
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM argo_floats;")
        count = cursor.fetchone()[0]
        
        print(f"✅ Database connected: {count:,} records available")
        
        # Test spatial query
        cursor.execute("""
            SELECT COUNT(*) FROM argo_floats 
            WHERE ST_DWithin(geometry, ST_SetSRID(ST_Point(72.88, 19.07), 4326), 100000)
        """)
        mumbai_count = cursor.fetchone()[0]
        print(f"✅ Spatial queries working: {mumbai_count} records near Mumbai")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_floatchat_pipeline():
    """Test the lightweight FloatChat pipeline"""
    print("🤖 Testing FloatChat pipeline...")
    
    try:
        from lightweight_pipeline import LightweightFloatChatPipeline
        
        # Initialize pipeline
        pipeline = LightweightFloatChatPipeline()
        print("✅ Pipeline initialized successfully")
        
        # Test a simple query
        response = pipeline.process_user_query("mumbai water")
        
        if response and response.get('success'):
            print("✅ Pipeline test successful")
            print(f"📊 Retrieved {response.get('total_records', 0)} records")
            return True
        else:
            print("❌ Pipeline test failed")
            return False
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False

def main():
    """Run all system tests"""
    print("🚀 FloatChat Docker System Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Docker containers
    if test_docker_containers():
        tests_passed += 1
    
    print()
    
    # Test 2: Database
    if test_database_connection():
        tests_passed += 1
        
    print()
    
    # Test 3: FloatChat pipeline
    if test_floatchat_pipeline():
        tests_passed += 1
    
    print()
    print("=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Your FloatChat system is ready!")
        print("\n🌊 Try running: python lightweight_pipeline.py")
        print("💬 Ask questions like: 'show me water profile of mumbai'")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        
        if tests_passed == 0:
            print("\n🔧 Quick fixes:")
            print("1. Start Docker: docker-compose up -d")
            print("2. Wait 30 seconds for database initialization")
            print("3. Run this test again: python test_docker_system.py")

if __name__ == "__main__":
    main()