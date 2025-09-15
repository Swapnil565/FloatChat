import React, { useState, useEffect, useRef } from 'react';

const FloatChat = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const inputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Enhanced function to generate bot response with hardcoded outputs
  const generateResponse = (userMessage) => {
    const messageLower = userMessage.toLowerCase();
    
    // PRIORITY 1: Specific hardcoded responses (check these FIRST)
    
    // Indian Ocean Temperature Trends - EXACT MATCH FIRST
    if ((messageLower.includes('indian ocean') && (messageLower.includes('temperature') || messageLower.includes('warming') || messageLower.includes('trend'))) ||
        (messageLower.includes('ocean') && messageLower.includes('temperature') && messageLower.includes('trend')) ||
        messageLower.includes('indian ocean temperature') ||
        messageLower.includes('temperature trends') ||
        messageLower.includes('ocean warming')) {
      return {
        text: "**Floaty (Bot):** Hey there, ocean explorer! I'm Floaty, your friendly AI guide to the seas. Let's dive into those trends: The Indian Ocean has shown an **average warming** of +0.5°C over the past 12 months, with a notable **anomaly detection** in the Bay of Bengal reaching +1.5°C—possibly linked to climate patterns like El Niño. This data's been rigorously **validated against baselines** to ensure accuracy. **Confidence: 95%**. What else can I uncover for you?",
        image: "/images/temperature_trends.svg",
        imageAlt: "Indian Ocean Temperature Trends Over Last 12 Months"
      };
    }
    
    // Mumbai Warm Water - EXACT MATCH FIRST
    else if ((messageLower.includes('mumbai') && (messageLower.includes('warm') || messageLower.includes('hot') || messageLower.includes('temperature'))) ||
             messageLower.includes('warm water mumbai') ||
             messageLower.includes('hot water mumbai') ||
             messageLower.includes('temperature mumbai')) {
      return {
        text: "Ahoy from Mumbai! Floaty here, your guide to the Arabian Sea. You've noticed the **warm water patches**! My analysis shows a significant **temperature anomaly** of +2.1°C about 20km off the coast. This is likely due to a **weakened coastal current**. While unusual, it's currently stable. **Confidence: 92%**. Would you like to explore the ecological impact of this?",
        image: "/images/warm_water_mumbai.svg",
        imageAlt: "Warm Water Anomaly Near Mumbai Coast"
      };
    }
    
    // Kerala Fishing Zones - EXACT MATCH FIRST
    else if ((messageLower.includes('kerala') || messageLower.includes('kochi')) && (messageLower.includes('fish') || messageLower.includes('pomfret')) ||
             messageLower.includes('fishing kerala') ||
             messageLower.includes('pomfret kerala') ||
             messageLower.includes('fish kerala')) {
      return {
        text: "Greetings, sea adventurer! It's Floaty, your trusty ocean companion. Based on current data, I **recommend the zone** 50km off Kochi with ideal **water temperature 26°C** and calm seas—perfect for pomfret. **Avoid anomalies** in northern areas due to detected anomalies that could affect safety and catch. **Safety advisory**: Always check local conditions! **Confidence: 85%**. Need more details or alternatives?",
        image: "/images/fishing_zones_kerala.svg",
        imageAlt: "Pomfret Fishing Advice Near Kerala"
      };
    }
    
    // PRIORITY 2: General responses (only if above don't match)
    
    // Ocean temperature keywords (general) - ONLY if not already matched above
    else if (['temperature', 'warming', 'heat', 'thermal', 'climate'].some(word => messageLower.includes(word))) {
      return "🌡️ Ocean temperatures have been rising globally. The average sea surface temperature has increased by approximately 0.6°C since 1969. This warming affects marine ecosystems, fish migration patterns, and coral reef health. Would you like specific data for a particular region?";
    }
    
    // Fishing and marine life keywords
    else if (['fish', 'fishing', 'marine life', 'species', 'catch', 'stock'].some(word => messageLower.includes(word))) {
      return "🐟 Marine fisheries data shows significant changes in fish populations and distribution. Climate change is causing many species to migrate toward the poles. Sustainable fishing practices are crucial for maintaining healthy ocean ecosystems. Which specific species or region interests you?";
    }
    
    // Pollution keywords
    else if (['pollution', 'plastic', 'waste', 'contamination', 'debris'].some(word => messageLower.includes(word))) {
      return "🏭 Ocean pollution is a critical issue. Approximately 8 million tons of plastic waste enter our oceans annually. This affects marine life through ingestion, entanglement, and habitat disruption. Microplastics are now found throughout the marine food chain.";
    }
    
    // Sea level keywords
    else if (['sea level', 'rising', 'coastal', 'flooding', 'erosion'].some(word => messageLower.includes(word))) {
      return " Global sea levels have risen approximately 20cm since 1900, with the rate of increase accelerating in recent decades. This poses significant risks to coastal communities and ecosystems worldwide. Current projections suggest continued rise throughout this century.";
    }
    
    // Ocean acidification keywords
    else if (['acid', 'ph', 'acidification', 'carbonic', 'co2'].some(word => messageLower.includes(word))) {
      return " Ocean acidification, caused by increased CO2 absorption, has lowered ocean pH by 0.1 units since the industrial revolution. This 'other CO2 problem' threatens shell-forming organisms and coral reefs, with cascading effects throughout marine food webs.";
    }
    
    // Coral reef keywords
    else if (['coral', 'reef', 'bleaching', 'ecosystem'].some(word => messageLower.includes(word))) {
      return " Coral reefs are among the most biodiverse ecosystems on Earth, but they're facing unprecedented threats. Rising temperatures cause coral bleaching, while acidification weakens their calcium carbonate structures. About 50% of shallow-water corals have been lost in the past 30 years.";
    }
    
    // Ocean currents keywords
    else if (['current', 'circulation', 'gulf stream', 'conveyor'].some(word => messageLower.includes(word))) {
      return " Ocean currents play a crucial role in global climate regulation, distributing heat around the planet. The Atlantic Meridional Overturning Circulation (AMOC) has been weakening, which could significantly impact weather patterns in Europe and North America.";
    }
    
    // Data or research keywords
    else if (['data', 'research', 'study', 'analysis', 'monitoring'].some(word => messageLower.includes(word))) {
      return " Ocean monitoring involves satellites, buoys, autonomous underwater vehicles, and research vessels. Key datasets include temperature profiles, salinity measurements, current speeds, and biological surveys. This data helps scientists understand ocean health and predict changes.";
    }
    
    // Sustainability keywords
    else if (['sustainable', 'conservation', 'protection', 'preserve'].some(word => messageLower.includes(word))) {
      return "♻️ Ocean sustainability requires integrated approaches including marine protected areas, sustainable fishing quotas, pollution reduction, and climate action. International cooperation through agreements like the UN Ocean Treaty is essential for protecting our blue planet.";
    }
    
    // Greeting or general keywords
    else if (['hello', 'hi', 'help', 'what', 'how'].some(word => messageLower.includes(word))) {
      return "👋 Welcome to FloatChat! I'm here to help you explore ocean data and marine science topics. I can discuss ocean temperatures, marine ecosystems, fishing data, pollution impacts, sea level rise, and much more. What would you like to learn about?";
    }
    
    // Default response
    else {
      return "🌊 That's an interesting question about our oceans! While I don't have specific data on that topic right now, I can help you with information about ocean temperatures, marine ecosystems, fishing zones, pollution, sea level changes, and ocean conservation. What specific aspect interests you most?";
    }
  };

  // Handle sending message
  const handleSendMessage = () => {
    if (userInput.trim()) {
      const newUserMessage = { role: "user", content: userInput.trim() };
      const botResponse = generateResponse(userInput.trim());
      
      // Handle response format (string or object with text and image)
      let newBotMessage;
      if (typeof botResponse === 'object' && botResponse.text) {
        newBotMessage = { 
          role: "bot", 
          content: botResponse.text,
          image: botResponse.image,
          imageAlt: botResponse.imageAlt
        };
      } else {
        newBotMessage = { role: "bot", content: botResponse };
      }
      
      setMessages(prev => [...prev, newUserMessage, newBotMessage]);
      setUserInput('');
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Auto focus on input and scroll to bottom
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Function to render message with markdown-like formatting
  const renderMessage = (content) => {
    // Replace **text** with bold formatting
    const parts = content.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <>
      <style>{`
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        body {
          font-family: 'Inter', sans-serif;
          margin: 0;
          padding: 0;
        }
        
        /* Style the main app */
        .app {
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
          min-height: 100vh;
          overflow-x: hidden;
        }
        
        .main-container {
          padding: 0;
          max-width: none;
        }
        
        /* Header */
        .chat-header {
          text-align: center;
          margin-bottom: 0.5rem;
          padding: 0.5rem 0;
          height: 10vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        
        .chat-title {
          font-size: 2.1rem;
          font-weight: 700;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 0.4rem;
          letter-spacing: -0.02em;
        }
        
        .chat-subtitle {
          font-size: 1.1rem;
          color: #64748b;
          font-weight: 400;
          margin-top: 0.2rem;
        }
        
        /* Chat container */
        .chat-container {
          max-width: 900px;
          margin: 0 auto;
          padding: 2rem 2.5rem;
          background: rgba(255,255,255,0.95);
          border-radius: 24px;
          box-shadow: 0 25px 50px rgba(0,0,0,0.15);
          backdrop-filter: blur(10px);
          margin-bottom: 1.5rem;
          height: 75vh;
          overflow-y: auto;
        }
        
        /* Message styling */
        .message-container {
          margin: 1rem 0;
          display: flex;
          align-items: flex-start;
          gap: 1rem;
        }
        
        .user-message-container {
          justify-content: flex-end;
        }
        
        .bot-message-container {
          justify-content: flex-start;
        }
        
        .message-bubble {
          max-width: 75%;
          padding: 1rem 1.3rem;
          border-radius: 18px;
          font-family: 'Inter', sans-serif;
          line-height: 1.4;
          font-size: 0.87rem;
          box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .user-bubble {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 6px;
        }
        
        .bot-bubble {
          background: #f8fafc;
          color: #334155;
          border: 1px solid #e2e8f0;
          border-bottom-left-radius: 6px;
        }
        
        .avatar {
          width: 30px;
          height: 30px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.85rem;
          font-weight: 600;
          flex-shrink: 0;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .user-avatar {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }
        
        .bot-avatar {
          background: #f1f5f9;
          color: #475569;
          border: 1px solid #e2e8f0;
        }
        
        /* Input styling */
        .chat-input-container {
          position: fixed;
          bottom: 2rem;
          left: 50%;
          transform: translateX(-50%);
          width: 90%;
          max-width: 800px;
          z-index: 1000;
          display: flex;
          gap: 1rem;
          height: 15vh;
          align-items: center;
        }
        
        .input-field {
          flex: 1;
          background: white;
          border-radius: 25px;
          border: 2px solid #e2e8f0;
          padding: 0.85rem 1.3rem;
          font-size: 0.95rem;
          font-family: 'Inter', sans-serif;
          box-shadow: 0 10px 25px rgba(0,0,0,0.1);
          transition: all 0.3s ease;
          outline: none;
        }
        
        .input-field:focus {
          border-color: #667eea;
          box-shadow: 0 10px 35px rgba(102, 126, 234, 0.3);
        }
        
        .input-field::placeholder {
          color: #94a3b8;
        }
        
        .send-button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 25px;
          border: none;
          padding: 0.7rem 1.7rem;
          font-weight: 600;
          font-size: 0.95rem;
          font-family: 'Inter', sans-serif;
          box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
          transition: all 0.3s ease;
          cursor: pointer;
        }
        
        .send-button:hover {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
          transform: translateY(-2px);
          box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        }
        
        .send-button:active {
          transform: translateY(0px);
        }
        
        /* Welcome message styling */
        .welcome-container {
          text-align: center;
          padding: 2rem;
          max-width: 800px;
          margin: 0 auto;
          height: 65vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        
        .welcome-message {
          background: rgba(255,255,255,0.9);
          border-radius: 20px;
          padding: 2rem;
          margin-bottom: 2rem;
          box-shadow: 0 15px 35px rgba(0,0,0,0.1);
          backdrop-filter: blur(10px);
        }
        
        .welcome-message h3 {
          color: #334155;
          margin-bottom: 1rem;
          font-size: 1.5rem;
        }
        
        .welcome-message p {
          color: #64748b;
          font-size: 1.1rem;
          line-height: 1.6;
        }
        
        .example-questions {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
          margin-top: 2rem;
        }
        
        .example-question {
          background: rgba(255,255,255,0.8);
          border-radius: 15px;
          padding: 1rem;
          font-size: 0.9rem;
          color: #475569;
          border: 1px solid #e2e8f0;
          transition: all 0.3s ease;
        }
        
        .example-question:hover {
          background: rgba(255,255,255,1);
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        
        .example-question strong {
          display: block;
          margin-bottom: 0.5rem;
        }
        
        /* Message image styling */
        .message-image-container {
          margin-top: 1rem;
          border-radius: 12px;
          overflow: hidden;
          border: 1px solid #e2e8f0;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .message-image {
          width: 100%;
          max-width: 100%;
          height: auto;
          display: block;
          border-radius: 12px;
        }
      `}</style>
      
      <div className="app">
        <div className="main-container">
          {/* Header */}
          <div className="chat-header">
            <h1 className="chat-title">🌊 FloatChat</h1>
            <p className="chat-subtitle">Waves of Innovation: AI-Driven Insights for Sustainable Oceans</p>
          </div>

          {/* Display welcome message or chat */}
          {messages.length === 0 ? (
            <div className="welcome-container">
              <div className="welcome-message">
                <h3>🌊 Welcome to FloatChat!</h3>
                <p>
                  Your AI companion for exploring ocean data, marine ecosystems, and sustainable ocean practices. 
                  Ask me anything about our blue planet!
                </p>
              </div>
              
              <div className="example-questions">
                <div className="example-question">
                  <strong>🌡️ Climate Impact:</strong>
                  "What are the temperature trends in the Indian Ocean?"
                </div>
                <div className="example-question">
                  <strong>🐟 Marine Life:</strong>
                  "Show me warm water near Mumbai"
                </div>
                <div className="example-question">
                  <strong>🎣 Fishing Zones:</strong>
                  "Where should I fish for pomfret near Kerala?"
                </div>
                <div className="example-question">
                  <strong>🪸 Ecosystems:</strong>
                  "How are coral reefs doing?"
                </div>
              </div>
            </div>
          ) : (
            // Display chat messages in a container
            <div className="chat-container" ref={chatContainerRef}>
              {messages.map((msg, index) => (
                <div key={index}>
                  {msg.role === "user" ? (
                    <div className="message-container user-message-container">
                      <div className="message-bubble user-bubble">{msg.content}</div>
                      <div className="avatar user-avatar">U</div>
                    </div>
                  ) : (
                    <div className="message-container bot-message-container">
                      <div className="avatar bot-avatar">🌊</div>
                      <div className="message-bubble bot-bubble">
                        {renderMessage(msg.content)}
                        {msg.image && (
                          <div className="message-image-container">
                            <img 
                              src={msg.image} 
                              alt={msg.imageAlt || "Chart visualization"} 
                              className="message-image"
                            />
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Input area at bottom */}
          <div className="chat-input-container">
            <input
              ref={inputRef}
              type="text"
              className="input-field"
              placeholder="Try: 'Indian Ocean temperature trends' or 'warm water Mumbai' or 'pomfret fishing Kerala'"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button 
              className="send-button"
              onClick={handleSendMessage}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default FloatChat;
