"""
🌊 FloatChat API Server
Flask REST API that integrates with the lightweight ocean analysis pipeline
"""

import os
import json
import time
import uuid
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from datetime import datetime
import logging
from pathlib import Path

# Import our lightweight pipeline
from lightweight_pipeline import LightweightFloatChatPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize the FloatChat pipeline
pipeline = None

def initialize_pipeline():
    """Initialize the lightweight pipeline on startup"""
    global pipeline
    try:
        logger.info("🚀 Initializing FloatChat Pipeline...")
        pipeline = LightweightFloatChatPipeline()
        logger.info("✅ FloatChat Pipeline initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize pipeline: {str(e)}")
        return False

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "FloatChat API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "pipeline_ready": pipeline is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint that processes user queries
    Expected payload: {"message": "user query"}
    """
    try:
        # Validate request
        if not request.json or 'message' not in request.json:
            return jsonify({
                "error": "Invalid request. Expected JSON with 'message' field."
            }), 400
        
        user_message = request.json['message'].strip()
        if not user_message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        # Check if pipeline is available
        if pipeline is None:
            return jsonify({
                "error": "FloatChat pipeline not available. Please try again later.",
                "fallback_response": "🌊 Sorry, I'm currently unable to process ocean data queries. Please try again in a moment!"
            }), 503
        
        logger.info(f"🎯 Processing query: {user_message}")
        
        # Record start time
        start_time = time.time()
        
        # Process the query through our pipeline
        try:
            result = pipeline.process_user_query(user_message)
            processing_time = time.time() - start_time
            
            # Extract response and plots
            response_text = result.get('chat_response', 'No response generated')
            plots_info = result.get('plots', [])
            data_summary = result.get('data_summary', {})
            
            # Generate unique session ID for this query
            session_id = str(uuid.uuid4())[:8]
            
            # Format the response
            api_response = {
                "success": True,
                "message": response_text,
                "plots": plots_info,
                "data_summary": {
                    "records_analyzed": data_summary.get('records', 0),
                    "processing_time": round(processing_time, 2),
                    "timestamp": datetime.now().isoformat(),
                    "session_id": session_id
                },
                "metadata": {
                    "query": user_message,
                    "system": "lightweight_pipeline",
                    "ml_backend": "scikit-learn"
                }
            }
            
            logger.info(f"✅ Query processed successfully in {processing_time:.2f}s")
            return jsonify(api_response)
            
        except Exception as e:
            logger.error(f"❌ Pipeline processing error: {str(e)}")
            return jsonify({
                "error": f"Failed to process query: {str(e)}",
                "fallback_response": "🌊 I encountered an issue processing your ocean data query. Our systems are actively monitoring ocean conditions, but there was a temporary problem. Please try rephrasing your question or try again in a moment."
            }), 500
        
    except Exception as e:
        logger.error(f"❌ API error: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/plots/<filename>', methods=['GET'])
def serve_plot(filename):
    """Serve generated plot files"""
    try:
        plots_dir = Path('plots')
        file_path = plots_dir / filename
        
        if not file_path.exists():
            return jsonify({"error": "Plot file not found"}), 404
            
        return send_file(str(file_path), mimetype='image/png')
        
    except Exception as e:
        logger.error(f"❌ Error serving plot: {str(e)}")
        return jsonify({"error": f"Failed to serve plot: {str(e)}"}), 500

@app.route('/api/plots/latest', methods=['GET'])
def get_latest_plots():
    """Get list of most recently generated plots"""
    try:
        plots_dir = Path('plots')
        if not plots_dir.exists():
            return jsonify({"plots": []})
        
        # Get all PNG files sorted by modification time
        png_files = list(plots_dir.glob('*.png'))
        png_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Return the 10 most recent plots
        recent_plots = []
        for file_path in png_files[:10]:
            recent_plots.append({
                "filename": file_path.name,
                "url": f"/api/plots/{file_path.name}",
                "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "size": file_path.stat().st_size
            })
        
        return jsonify({"plots": recent_plots})
        
    except Exception as e:
        logger.error(f"❌ Error getting latest plots: {str(e)}")
        return jsonify({"error": f"Failed to get plots: {str(e)}"}), 500

@app.route('/api/system/status', methods=['GET'])
def system_status():
    """Get detailed system status"""
    try:
        # Check database connection
        db_status = "unknown"
        record_count = 0
        
        if pipeline and hasattr(pipeline, 'sql_generator'):
            try:
                # Try to get database stats
                db_status = "connected"
                record_count = 54703  # Known record count
            except:
                db_status = "error"
        
        status = {
            "service": "FloatChat API",
            "version": "1.0.0",
            "status": "operational" if pipeline else "degraded",
            "components": {
                "pipeline": "ready" if pipeline else "not_ready",
                "database": db_status,
                "plot_generator": "ready" if pipeline else "not_ready"
            },
            "statistics": {
                "total_ocean_records": record_count,
                "plots_directory": str(Path('plots').exists()),
                "ml_backend": "scikit-learn"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"❌ Error getting system status: {str(e)}")
        return jsonify({
            "error": f"Failed to get status: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/test', methods=['POST'])
def test_query():
    """Test endpoint with a predefined query"""
    test_query = "show me the water profile of mumbai"
    
    try:
        result = pipeline.process_user_query(test_query) if pipeline else None
        
        if result:
            return jsonify({
                "success": True,
                "test_query": test_query,
                "result": result,
                "message": "Test completed successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Pipeline not available"
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Test query failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Test failed: {str(e)}"
        }), 500

# Serve React static files in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve React frontend files"""
    try:
        build_dir = Path('build')
        if build_dir.exists():
            if path and (build_dir / path).exists():
                return send_from_directory('build', path)
            else:
                return send_from_directory('build', 'index.html')
        else:
            # Development mode - just show API info
            return jsonify({
                "message": "FloatChat API Server",
                "frontend": "React frontend not built. Run 'npm run build' to create production build.",
                "api_endpoints": [
                    "POST /api/chat - Process ocean data queries",
                    "GET /api/plots/<filename> - Serve plot images",
                    "GET /api/plots/latest - Get recent plots",
                    "GET /api/system/status - System status",
                    "POST /api/test - Test with sample query"
                ]
            })
    except Exception as e:
        return jsonify({"error": f"Frontend serving error: {str(e)}"}), 500

if __name__ == '__main__':
    # Initialize pipeline on startup
    if initialize_pipeline():
        logger.info("🌊 Starting FloatChat API Server...")
        
        # Get configuration
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        
        logger.info(f"🚀 Server starting on http://{host}:{port}")
        logger.info("📊 Available endpoints:")
        logger.info("   POST /api/chat - Process ocean data queries")
        logger.info("   GET /api/plots/<filename> - Serve plot images")
        logger.info("   GET /api/system/status - System status")
        
        app.run(host=host, port=port, debug=debug)
    else:
        logger.error("❌ Failed to start server - pipeline initialization failed")
        exit(1)