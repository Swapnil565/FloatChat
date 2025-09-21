"""
FloatChat Friendly Chatbot System
Provides detailed, concise, and friendly responses for ocean data queries
"""

import os
from typing import Dict, List, Optional
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

load_dotenv()

class FloatChatBot:
    def __init__(self):
        self.client = Cerebras(api_key=os.getenv('CEREBRAS_API_KEY'))
        self.conversation_history = []
        
    def get_system_prompt(self) -> str:
        """
        Return system prompt for direct ocean data analysis
        """
        return """You are an oceanographic data analyst. Provide direct, scientific analysis of ocean data without unnecessary formatting or repetition.

ANALYSIS FOCUS:
- Interpret temperature, salinity, and depth patterns
- Explain ocean science behind the observations
- Identify significant oceanographic features
- Provide regional context for the measurements

RESPONSE STYLE:
- Direct and analytical
- Plain text only
- No emojis or fancy formatting
- Don't repeat user questions
- Focus on data insights, not visualizations
- Scientific but accessible language

AVOID:
- Mentioning user queries
- Talking about plots or visualizations
- Overly enthusiastic language
- Repeating information unnecessarily
- Technical difficulties or system status"""

    def generate_response(self, user_query: str, sql_metadata: Optional[Dict] = None, 
                         data_summary: Optional[Dict] = None) -> str:
        """
        Generate a direct, analytical response based on actual ocean data
        """
        
        # Prepare data context
        data_context = ""
        if data_summary and data_summary.get('data_shape'):
            rows, cols = data_summary['data_shape']
            data_context += f"Analysis of {rows:,} ocean measurements. "
            
            if data_summary.get('location_info'):
                data_context += f"Location: {data_summary['location_info']}. "
            
            if data_summary.get('depth_range'):
                depth_range = data_summary['depth_range']
                if isinstance(depth_range, dict):
                    data_context += f"Depth range: {depth_range.get('surface', 0)}m to {depth_range.get('bottom', 2000)}m. "
                
            if data_summary.get('temp_range'):
                temp_range = data_summary['temp_range']
                if isinstance(temp_range, dict):
                    data_context += f"Temperature range: {temp_range.get('min', 0)}°C to {temp_range.get('max', 30)}°C. "
                
            if data_summary.get('salinity_range'):
                sal_range = data_summary['salinity_range']
                if isinstance(sal_range, dict):
                    data_context += f"Salinity range: {sal_range.get('min', 33)} to {sal_range.get('max', 37)} PSU."
        
        # Create analysis prompt
        conversation_prompt = f"""Analyze this ocean data and provide insights:

{data_context}

Provide a direct analysis focusing on:
1. What the ocean conditions show
2. Notable patterns in temperature and salinity
3. Ocean science interpretation of the data
4. Regional oceanographic context

Give a concise, scientific analysis without repeating the user's question. Focus on what the data reveals about ocean conditions."""

        try:
            response = self.client.chat.completions.create(
                model="llama3.1-8b",
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": conversation_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            chat_response = response.choices[0].message.content.strip()
            
            # Add to conversation history
            self.conversation_history.append({
                "user": user_query,
                "assistant": chat_response,
                "metadata": sql_metadata
            })
            
            return chat_response
            
        except Exception as e:
            return self._get_fallback_response(user_query, str(e))
    
    def _get_fallback_response(self, user_query: str, error: str) -> str:
        """
        Provide a simple fallback response when API fails
        """
        return f"Ocean data analysis temporarily unavailable. Please check your API configuration. Error: {error}"
    
    def get_plot_explanation(self, plot_type: str, data_info: Dict) -> str:
        """
        Generate specific explanations for different plot types
        """
        explanations = {
            "profile": "This profile chart shows how ocean properties change with depth - like taking a vertical slice through the ocean! 📊 You'll notice how temperature typically decreases as you go deeper, creating distinct ocean layers.",
            
            "3d_scatter": "This interactive 3D visualization lets you explore the ocean data in three dimensions! 🌐 You can rotate, zoom, and pan to see how temperature and salinity vary across location and depth. It's like having a virtual submarine tour!",
            
            "map": "This geographic map shows the spatial distribution of ocean measurements! 🗺️ Each point represents data from an Argo float, and the colors indicate different values. You can see how ocean properties vary across different regions.",
            
            "time_series": "This time series chart reveals how ocean conditions change over time! 📈 It's fascinating to see seasonal patterns, long-term trends, and sometimes even the effects of major climate events.",
            
            "ts_diagram": "This Temperature-Salinity diagram is like a 'fingerprint' of water masses! 🌡️ Different ocean regions and depths create characteristic T-S signatures that oceanographers use to track water movement."
        }
        
        base_explanation = explanations.get(plot_type, "This visualization shows your ocean data in an informative way!")
        
        # Add data-specific context
        if data_info.get('data_shape'):
            rows, cols = data_info['data_shape']
            base_explanation += f" I'm showing you {rows:,} measurements from our ocean database."
        
        return base_explanation
    
    def suggest_follow_up_questions(self, user_query: str, plot_metadata: Dict) -> List[str]:
        """
        Suggest relevant follow-up questions based on the current query
        """
        suggestions = []
        
        query_lower = user_query.lower()
        
        # Location-based suggestions
        if any(location in query_lower for location in ['mumbai', 'chennai', 'kolkata']):
            suggestions.extend([
                "How does this compare to other coastal regions?",
                "Can you show me the seasonal patterns here?",
                "What's the water quality like at different depths?"
            ])
        
        # Parameter-specific suggestions
        if 'temperature' in query_lower:
            suggestions.extend([
                "How does salinity vary in the same region?",
                "Can you show me the temperature profile?",
                "What causes these temperature patterns?"
            ])
        
        if 'salinity' in query_lower:
            suggestions.extend([
                "How does this affect marine life?",
                "Show me the T-S diagram for this region",
                "What are the freshwater influences here?"
            ])
        
        # Plot-specific suggestions
        plot_type = plot_metadata.get('query_type', '')
        if plot_type == 'spatial':
            suggestions.extend([
                "Can you show me a 3D view of this data?",
                "How does this vary with depth?",
                "Show me the time evolution of this pattern"
            ])
        
        # General ocean science suggestions
        suggestions.extend([
            "What ocean currents affect this region?",
            "How does this data compare to global averages?",
            "Can you explain the ocean science behind this pattern?"
        ])
        
        # Return a random selection to keep it fresh
        import random
        return random.sample(suggestions, min(3, len(suggestions)))
    
    def get_conversation_summary(self) -> Dict:
        """
        Get a summary of the current conversation
        """
        return {
            "total_interactions": len(self.conversation_history),
            "topics_discussed": [interaction["metadata"].get("query_type") if interaction.get("metadata") else "general" 
                               for interaction in self.conversation_history],
            "recent_queries": [interaction["user"] for interaction in self.conversation_history[-3:]]
        }

# Test function
def test_floatchat_bot():
    """Test the FloatChat bot with sample scenarios"""
    bot = FloatChatBot()
    
    test_scenarios = [
        {
            "query": "What's the water temperature like near Mumbai?",
            "plot_metadata": {"query_type": "spatial", "location": "Mumbai", "parameters": ["temperature"]},
            "data_summary": {"data_shape": (1250, 7), "total_records": 1250}
        },
        {
            "query": "Show me temperature profile for float 5905529",
            "plot_metadata": {"query_type": "profile", "parameters": ["temperature"]},
            "data_summary": {"data_shape": (45, 7), "total_records": 45}
        },
        {
            "query": "Can you create a 3D visualization of ocean data?",
            "plot_metadata": {"query_type": "spatial", "parameters": ["temperature", "salinity"]},
            "data_summary": {"data_shape": (3000, 7), "total_records": 3000}
        }
    ]
    
    print("🧪 Testing FloatChat Bot\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"Test {i}: {scenario['query']}")
        response = bot.generate_response(
            scenario['query'], 
            scenario['plot_metadata'], 
            scenario['data_summary']
        )
        print(f"FloatChat: {response}")
        print("-" * 80)

if __name__ == "__main__":
    test_floatchat_bot()