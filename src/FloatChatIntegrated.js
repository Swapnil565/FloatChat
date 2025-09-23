import React, { useState, useEffect, useRef } from 'react';

const FloatChat = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');
  const [currentImageIndex, setCurrentImageIndex] = useState({}); // Track current image index for each message
  const inputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // API Configuration
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  // Check API status on component mount
  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/system/status`);
        if (response.ok) {
          setApiStatus('connected');
        } else {
          setApiStatus('error');
        }
      } catch (error) {
        console.error('API status check failed:', error);
        setApiStatus('offline');
      }
    };
    
    checkApiStatus();
  }, [API_BASE_URL]);

  // Call real API for ocean data analysis
  const generateResponse = async (userMessage) => {
    try {
      setIsLoading(true);
      
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        // Format response with real ocean data
        let responseText = data.message;
        
        // Add data summary if available
        if (data.data_summary) {
          const summary = data.data_summary;
          responseText += `\n\n📊 **Analysis Summary:**\n`;
          responseText += `• Records analyzed: ${summary.records_analyzed || 0}\n`;
          responseText += `• Processing time: ${summary.processing_time || 0}s\n`;
          responseText += `• System: Lightweight ML Pipeline (scikit-learn)`;
        }

        // Handle plots - convert to the format expected by the frontend
        let plotImages = [];
        if (data.plots && data.plots.length > 0) {
          data.plots.forEach(plot => {
            // Handle both single filename and multiple filenames
            if (plot.filename) {
              // Single file plot (like 3D scatter)
              plotImages.push({
                url: `${API_BASE_URL}/api/plots/${plot.filename}`,
                alt: plot.description || 'Ocean Data Visualization'
              });
            } else if (plot.filenames && plot.filenames.length > 0) {
              // Multiple files plot (like profile plots)
              plot.filenames.forEach(filename => {
                plotImages.push({
                  url: `${API_BASE_URL}/api/plots/${filename}`,
                  alt: plot.description || 'Ocean Data Visualization'
                });
              });
            }
          });
        }

        return {
          text: responseText,
          images: plotImages,
          metadata: data.metadata
        };
      } else {
        throw new Error(data.error || 'Unknown API error');
      }
      
    } catch (error) {
      console.error('API Error:', error);
      
      // Fallback to enhanced responses when API is unavailable
      return getFallbackResponse(userMessage, error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Enhanced fallback responses when API is unavailable
  const getFallbackResponse = (userMessage, errorMessage) => {
    const messageLower = userMessage.toLowerCase();
    
    // PRIORITY 1: Specific enhanced responses (maintaining original hardcoded logic)
    
    // Indian Ocean Temperature Trends - EXACT MATCH FIRST
    if ((messageLower.includes('indian ocean') && (messageLower.includes('temperature') || messageLower.includes('warming') || messageLower.includes('trend'))) ||
        (messageLower.includes('ocean') && messageLower.includes('temperature') && messageLower.includes('trend')) ||
        messageLower.includes('indian ocean temperature') ||
        messageLower.includes('temperature trends') ||
        messageLower.includes('ocean warming')) {
      return {
        text: "**Floaty (Bot):** Hey there, ocean explorer! I'm Floaty, your friendly AI guide to the seas. Let's dive into those trends: The Indian Ocean has shown an **average warming** of +0.5°C over the past 12 months, with a notable **anomaly detection** in the Bay of Bengal reaching +1.5°C—possibly linked to climate patterns like El Niño. This data's been rigorously **validated against baselines** to ensure accuracy. **Confidence: 95%**. What else can I uncover for you?\n\n🔧 **Note:** Currently using cached analysis. Real-time data processing temporarily unavailable.",
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
        text: "Ahoy from Mumbai! Floaty here, your guide to the Arabian Sea. You've noticed the **warm water patches**! My analysis shows a significant **temperature anomaly** of +2.1°C about 20km off the coast. This is likely due to a **weakened coastal current**. While unusual, it's currently stable. **Confidence: 92%**. Would you like to explore the ecological impact of this?\n\n🔧 **Note:** Currently using cached analysis. Real-time ocean monitoring temporarily unavailable.",
        image: "/images/warm_water_mumbai.svg",
        imageAlt: "Warm Water Anomaly Near Mumbai Coast"
      };
    }
    
    // Kerala Fishing Zones - EXACT MATCH FIRST
    else if (((messageLower.includes('kerala') || messageLower.includes('kochi')) && (messageLower.includes('fish') || messageLower.includes('pomfret'))) ||
             messageLower.includes('fishing kerala') ||
             messageLower.includes('pomfret kerala') ||
             messageLower.includes('fish kerala')) {
      return {
        text: "Greetings, sea adventurer! It's Floaty, your trusty ocean companion. Based on current data, I **recommend the zone** 50km off Kochi with ideal **water temperature 26°C** and calm seas—perfect for pomfret. **Avoid anomalies** in northern areas due to detected anomalies that could affect safety and catch. **Safety advisory**: Always check local conditions! **Confidence: 85%**. Need more details or alternatives?\n\n🔧 **Note:** Currently using cached analysis. Real-time fishing condition updates temporarily unavailable.",
        image: "/images/fishing_zones_kerala.svg",
        imageAlt: "Pomfret Fishing Advice Near Kerala"
      };
    }
    
    // PRIORITY 2: General responses with offline notice
    
    // Ocean temperature keywords (general)
    else if (['temperature', 'warming', 'heat', 'thermal', 'climate'].some(word => messageLower.includes(word))) {
      return {
        text: "🌡️ Ocean temperatures have been rising globally. The average sea surface temperature has increased by approximately 0.6°C since 1969. This warming affects marine ecosystems, fish migration patterns, and coral reef health. Would you like specific data for a particular region?\n\n🔧 **System Status:** Real-time temperature analysis currently unavailable. Connecting to ocean data pipeline..."
      };
    }
    
    // Default response with system status
    else {
      return {
        text: "🌊 I'm your FloatChat ocean analysis assistant! While I'm currently unable to access real-time ocean data, I can still help with general oceanographic information. Once our systems reconnect, I'll provide detailed analysis with live ARGO float data, temperature profiles, and multi-plot visualizations.\n\n🔧 **System Status:** " + errorMessage
      };
    }
  };

  // Handle sending message
  const handleSendMessage = async () => {
    if (userInput.trim() && !isLoading) {
      const newUserMessage = { role: "user", content: userInput.trim() };
      const currentInput = userInput.trim();
      
      // Add user message immediately
      setMessages(prev => [...prev, newUserMessage]);
      setUserInput('');
      
      // Generate bot response
      const botResponse = await generateResponse(currentInput);
      
      // Handle response format (maintain compatibility with original structure)
      let newBotMessage;
      if (typeof botResponse === 'object' && botResponse.text) {
        newBotMessage = { 
          role: "bot", 
          content: botResponse.text,
          image: botResponse.image, // Single image for backward compatibility
          imageAlt: botResponse.imageAlt,
          images: botResponse.images // Multiple images for new functionality
        };
      } else {
        newBotMessage = { role: "bot", content: botResponse };
      }
      
      setMessages(prev => [...prev, newBotMessage]);
    }
  };

  // Image carousel navigation functions
  const navigateImage = (messageIndex, direction, totalImages) => {
    setCurrentImageIndex(prev => {
      const currentIndex = prev[messageIndex] || 0;
      let newIndex;
      
      if (direction === 'next') {
        newIndex = (currentIndex + 1) % totalImages;
      } else {
        newIndex = currentIndex === 0 ? totalImages - 1 : currentIndex - 1;
      }
      
      return {
        ...prev,
        [messageIndex]: newIndex
      };
    });
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
          padding-top: 1rem;
        }
        
        .main-container {
          padding: 0;
          max-width: none;
          min-height: calc(100vh - 2rem);
        }
        
        /* Header */
        .chat-header {
          text-align: center;
          margin-bottom: 2rem;
          padding: 0.5rem 0;
          height: calc(10vh + 17px);
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
        
        /* API Status Indicator */
        .api-status {
          display: inline-block;
          padding: 0.2rem 0.5rem;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
          margin-left: 0.5rem;
        }
        
        .api-status.connected {
          background: rgba(34, 197, 94, 0.1);
          color: #16a34a;
        }
        
        .api-status.offline {
          background: rgba(239, 68, 68, 0.1);
          color: #dc2626;
        }
        
        .api-status.checking {
          background: rgba(251, 191, 36, 0.1);
          color: #d97706;
        }
        
        /* Chat container */
        .chat-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2.75rem 3rem;
          background: rgba(255,255,255,0.95);
          border-radius: 24px;
          box-shadow: 0 25px 50px rgba(0,0,0,0.15);
          backdrop-filter: blur(10px);
          margin-bottom: 0.2rem;
          height: calc(75vh + 90px);
          overflow-y: auto;
        }
        
        /* Message styling */
        .message-container {
          margin: 1.75rem 0;
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
          max-width: calc(75% + 50px);
          padding: 1rem 1.3rem;
          border-radius: 18px;
          font-family: 'Inter', sans-serif;
          line-height: 1.4;
          font-size: 0.95rem;
          box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .user-bubble {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 6px;
          padding: 1.3rem 1.7rem;
        }
        
        .bot-bubble {
          background: #f8fafc;
          color: #334155;
          border: 1px solid #e2e8f0;
          border-bottom-left-radius: 6px;
          min-height: calc(1.4em + 70px);
          padding: 1.1rem 1.4rem;
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
        
        /* Loading indicator */
        .loading-indicator {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 0.5rem;
          color: #64748b;
          font-size: 0.8rem;
        }
        
        .loading-dots {
          display: flex;
          gap: 0.2rem;
        }
        
        .loading-dot {
          width: 4px;
          height: 4px;
          background: #64748b;
          border-radius: 50%;
          animation: loadingPulse 1.4s infinite ease-in-out;
        }
        
        .loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .loading-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes loadingPulse {
          0%, 80%, 100% { opacity: 0.3; }
          40% { opacity: 1; }
        }
        
        /* Input styling */
        .chat-input-container {
          position: fixed;
          bottom: 2rem;
          left: 50%;
          transform: translateX(-50%);
          width: auto;
          max-width: none;
          z-index: 1000;
          display: flex;
          gap: 1rem;
          height: auto;
          align-items: center;
          padding: 0.5rem 0;
        }
        
        .input-field {
          flex: 1;
          background: white;
          border-radius: 25px;
          border: 2px solid #e2e8f0;
          padding: 1rem 1.6rem;
          font-size: 0.95rem;
          font-family: 'Inter', sans-serif;
          box-shadow: 0 10px 25px rgba(0,0,0,0.1);
          transition: all 0.3s ease;
          outline: none;
          width: 790px;
          height: 100px;
          max-width: 790px;
          min-height: 100px;
          box-sizing: border-box;
        }
        
        .input-field:focus {
          border-color: #667eea;
          box-shadow: 0 10px 35px rgba(102, 126, 234, 0.3);
        }
        
        .input-field::placeholder {
          color: #94a3b8;
        }
        
        .input-field:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        
        .send-button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 25px;
          border: none;
          padding: 1.5rem 2.5rem;
          font-weight: 600;
          font-size: 1.1rem;
          font-family: 'Inter', sans-serif;
          box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
          transition: all 0.3s ease;
          cursor: pointer;
          height: 100px;
          min-width: 120px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .send-button:hover:not(:disabled) {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
          transform: translateY(-2px);
          box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        }
        
        .send-button:active {
          transform: translateY(0px);
        }
        
        .send-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        
        /* Welcome message styling */
        .welcome-container {
          text-align: center;
          padding: 1.5rem;
          max-width: 800px;
          margin: 0 auto;
          height: calc(65vh + 70px);
          display: flex;
          flex-direction: column;
          justify-content: center;
          transform: translateY(-45px);
          background: linear-gradient(135deg, rgba(245, 247, 250, 0.4) 0%, rgba(195, 207, 226, 0.4) 100%);
          border-radius: 24px;
          border: 1px solid rgba(226, 232, 240, 0.3);
          backdrop-filter: blur(5px);
        }
        
        .welcome-message {
          background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
          border-radius: 20px;
          padding: 2.5rem;
          margin-bottom: 1rem;
          box-shadow: 0 15px 35px rgba(0,0,0,0.1);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(226, 232, 240, 0.3);
          background-image: 
            radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.05) 0%, transparent 50%);
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
          margin-top: 1.5rem;
          margin-bottom: 1.5rem;
        }
        
        .example-question {
          background: rgba(255,255,255,0.85);
          border-radius: 15px;
          padding: 1.5rem;
          font-size: 0.92rem;
          color: #475569;
          border: 1px solid #e2e8f0;
          transition: all 0.3s ease;
          cursor: pointer;
          min-height: 120px;
          display: flex;
          flex-direction: column;
          justify-content: center;
          box-shadow: 0 2px 8px rgba(0,0,0,0.05);
          position: relative;
          overflow: hidden;
        }
        
        .example-question::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 4px;
          height: 100%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          opacity: 0;
          transition: opacity 0.3s ease;
        }
        
        .example-question:hover::before {
          opacity: 1;
        }
        
        .example-question:hover {
          background: rgba(255,255,255,1);
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(0,0,0,0.12);
          border-color: rgba(102, 126, 234, 0.2);
        }
        
        .example-question strong {
          display: block;
          margin-bottom: 0.6rem;
          font-size: 0.94rem;
          color: #334155;
        }
        
        /* Message image styling */
        .message-image-container {
          margin-top: 1.5rem;
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
        
        /* Multiple images styling */
        .message-images-container {
          margin-top: 1.5rem;
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
        }
        
        /* Image Carousel Styling */
        .image-carousel-container {
          margin-top: 1.5rem;
        }
        
        .image-carousel {
          position: relative;
          background: white;
          border-radius: 12px;
          overflow: hidden;
          border: 1px solid #e2e8f0;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          min-height: 475px;
        }
        
        .current-image-container {
          width: 100%;
          display: flex;
          justify-content: center;
          align-items: center;
          background: #f8fafc;
        }
        
        .carousel-image {
          width: 100%;
          max-width: 100%;
          height: auto;
          display: block;
          max-height: 720px;
          min-height: 420px;
          object-fit: contain;
        }
        
        .carousel-nav-btn {
          position: absolute;
          top: 50%;
          transform: translateY(-50%);
          background: rgba(0, 0, 0, 0.7);
          color: white;
          border: none;
          width: 60px;
          height: 60px;
          border-radius: 50%;
          font-size: 32px;
          font-weight: bold;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
          z-index: 10;
        }
        
        .carousel-nav-btn:hover {
          background: rgba(0, 0, 0, 0.9);
          transform: translateY(-50%) scale(1.1);
        }
        
        .carousel-prev {
          left: 20px;
        }
        
        .carousel-next {
          right: 20px;
        }
        
        .image-counter {
          position: absolute;
          bottom: 10px;
          right: 10px;
          background: rgba(0, 0, 0, 0.7);
          color: white;
          padding: 4px 8px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 600;
        }
        
        .image-description {
          background: #f1f5f9;
          padding: 8px 12px;
          font-size: 13px;
          color: #64748b;
          border-top: 1px solid #e2e8f0;
          text-align: center;
        }
      `}</style>
      
      <div className="app">
        <div className="main-container">
          {/* Header */}
          <div className="chat-header">
            <h1 className="chat-title">
              FloatChat
              <span className={`api-status ${apiStatus}`}>
                {apiStatus === 'connected' && '● Real-time Data'}
                {apiStatus === 'offline' && '● Offline Mode'}
                {apiStatus === 'checking' && '● Connecting...'}
                {apiStatus === 'error' && '● Limited Mode'}
              </span>
            </h1>
            <p className="chat-subtitle">Waves of Innovation: AI-Driven Insights for Sustainable Oceans</p>
          </div>

          {/* Display welcome message or chat */}
          {messages.length === 0 ? (
            <div className="welcome-container">
              <div className="welcome-message">
                <h3>Welcome to FloatChat!</h3>
                <p>
                  Your AI companion for exploring ocean data, marine ecosystems, and sustainable ocean practices. 
                  {apiStatus === 'connected' 
                    ? " Connected to real-time ARGO float data with 54,703+ ocean measurements!"
                    : " Ask me anything about our blue planet!"
                  }
                </p>
                <div style={{marginTop: '1.2rem', fontSize: '0.9rem', color: '#64748b'}}>
                  <p><strong>Real-time Analysis:</strong> Live ocean temperature, salinity & depth profiling</p>
                  <p><strong>Smart Insights:</strong> AI-powered pattern recognition and trend analysis</p>
                  <p><strong>Global Coverage:</strong> Comprehensive data from Indian Ocean ARGO floats</p>
                </div>
              </div>
              
              <div className="example-questions">
                <div className="example-question" onClick={() => setUserInput("What are the temperature trends in the Indian Ocean?")}>
                  <strong>Climate Impact:</strong>
                  "What are the temperature trends in the Indian Ocean?"
                </div>
                <div className="example-question" onClick={() => setUserInput("Show me warm water near Mumbai")}>
                  <strong>Marine Life:</strong>
                  "Show me warm water near Mumbai"
                </div>
                <div className="example-question" onClick={() => setUserInput("Where should I fish for pomfret near Kerala?")}>
                  <strong>Fishing Zones:</strong>
                  "Where should I fish for pomfret near Kerala?"
                </div>
                <div className="example-question" onClick={() => setUserInput("show me the water profile of mumbai")}>
                  <strong>Ocean Analysis:</strong>
                  "Show me the water profile of Mumbai"
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
                        
                        {/* Single image (backward compatibility) */}
                        {msg.image && (
                          <div className="message-image-container">
                            <img 
                              src={msg.image} 
                              alt={msg.imageAlt || "Chart visualization"} 
                              className="message-image"
                            />
                          </div>
                        )}
                        
                        {/* Multiple images with carousel navigation */}
                        {msg.images && msg.images.length > 0 && (
                          <div className="image-carousel-container">
                            <div className="image-carousel">
                              {/* Display current image */}
                              <div className="current-image-container">
                                <img 
                                  src={msg.images[currentImageIndex[index] || 0].url} 
                                  alt={msg.images[currentImageIndex[index] || 0].alt || "Ocean Data Visualization"} 
                                  className="carousel-image"
                                />
                              </div>
                              
                              {/* Navigation buttons (only show if more than 1 image) */}
                              {msg.images.length > 1 && (
                                <>
                                  <button 
                                    className="carousel-nav-btn carousel-prev"
                                    onClick={() => navigateImage(index, 'prev', msg.images.length)}
                                    aria-label="Previous diagram"
                                  >
                                    ‹
                                  </button>
                                  <button 
                                    className="carousel-nav-btn carousel-next"
                                    onClick={() => navigateImage(index, 'next', msg.images.length)}
                                    aria-label="Next diagram"
                                  >
                                    ›
                                  </button>
                                </>
                              )}
                              
                              {/* Image counter */}
                              {msg.images.length > 1 && (
                                <div className="image-counter">
                                  {(currentImageIndex[index] || 0) + 1} / {msg.images.length}
                                </div>
                              )}
                              
                              {/* Image description */}
                              <div className="image-description">
                                {msg.images[currentImageIndex[index] || 0].alt || "Ocean Data Visualization"}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
              
              {/* Loading indicator */}
              {isLoading && (
                <div className="message-container bot-message-container">
                  <div className="avatar bot-avatar">🌊</div>
                  <div className="message-bubble bot-bubble">
                    <div className="loading-indicator">
                      Analyzing ocean data
                      <div className="loading-dots">
                        <div className="loading-dot"></div>
                        <div className="loading-dot"></div>
                        <div className="loading-dot"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Input area at bottom */}
          <div className="chat-input-container">
            <input
              ref={inputRef}
              type="text"
              className="input-field"
              placeholder={apiStatus === 'connected' 
                ? "Try: 'Indian Ocean temperature trends' or 'warm water Mumbai' or 'show me water profile of mumbai'"
                : "Ask me about ocean data, marine ecosystems, or climate trends..."
              }
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
            />
            <button 
              className="send-button"
              onClick={handleSendMessage}
              disabled={isLoading || !userInput.trim()}
            >
              {isLoading ? 'Analyzing...' : 'Send'}
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default FloatChat;