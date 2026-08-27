import React, { useState, useEffect, useRef } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Welcome to Nyaya-Voice. How may I assist you with your legal matter today?' }
  ]);
  const [input, setInput] = useState('');
  const [isComplete, setIsComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    let storedSession = sessionStorage.getItem('nyaya_session');
    if (!storedSession) {
      storedSession = crypto.randomUUID();
      sessionStorage.setItem('nyaya_session', storedSession);
    }
    setSessionId(storedSession);
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text, session_id: sessionId })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        setMessages(prev => [...prev, { role: 'ai', text: `⚠️ Backend Error ${response.status}: ${data.detail || 'Unknown Crash'}` }]);
      } else {
        setMessages(prev => [...prev, { role: 'ai', text: data.reply || 'No text received' }]);
        if (data.status === 'complete') setIsComplete(true);
      }
    } catch (e) {
      setMessages(prev => [...prev, { role: 'ai', text: `⚠️ Network Error: Could not reach the Legal Brain.` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await sendAudio(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Could not access the microphone. Please check your permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendAudio = async (audioBlob) => {
    setIsLoading(true);
    
    const formData = new FormData();
    formData.append("file", audioBlob, "voice_recording.webm");
    formData.append("session_id", sessionId);
    formData.append("mode", "translate");

    try {
      const response = await fetch(`${API_BASE_URL}/api/voice-chat`, {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        setMessages(prev => [...prev, { role: 'ai', text: `⚠️ Voice Error ${response.status}: ${data.detail || 'Unknown Crash'}` }]);
      } else {
        setMessages(prev => [
          ...prev, 
          { role: 'user', text: `🎙️ ${data.transcript || 'Audio received'}` },
          { role: 'ai', text: data.reply || 'No text received' }
        ]);
        if (data.status === 'complete' || data.is_complete) setIsComplete(true);
      }
    } catch (e) {
      setMessages(prev => [...prev, { role: 'ai', text: `⚠️ Network Error: Could not reach the Legal Brain.` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4">
      <header className="w-full max-w-6xl flex justify-between items-center py-6 mb-8 border-b border-stone">
        <div className="flex items-center space-x-3">
          <div className="text-3xl font-serif font-bold tracking-tight">Nyaya-Voice</div>
        </div>
        <button className="bg-gold px-6 py-2 rounded-full font-medium hover:bg-yellow-200 transition text-charcoal flex items-center gap-2">
          <span>➔</span> Get Free Consultation
        </button>
      </header>
      
      <main className="w-full max-w-6xl flex flex-col lg:flex-row gap-12 items-center">
        <div className="w-full lg:w-1/2 flex flex-col pt-10">
          <h1 className="text-6xl md:text-8xl font-serif leading-[1.1] mb-6 text-charcoal">
            Smart Law <br/>Support
          </h1>
          <p className="text-gray-600 mb-8 leading-relaxed max-w-md text-lg">
            When the stakes are high, you need more than just advice. Nyaya-Voice provides sharp legal insight and automated drafting to help you take action with confidence.
          </p>
          
          <div className="flex items-center gap-8 mt-4">
             <div>
                <div className="font-serif text-4xl mb-1">200K</div>
                <div className="text-sm text-gray-500">Notices Drafted</div>
             </div>
             <div className="w-px h-12 bg-stone"></div>
             <div>
                <div className="font-serif text-4xl mb-1">20+</div>
                <div className="text-sm text-gray-500">Legal Categories</div>
             </div>
          </div>
        </div>

        <div className="w-full lg:w-1/2 bg-white rounded-[2rem] shadow-sm border border-stone pt-6 pb-4 px-4 flex flex-col h-[600px] relative z-10">
          <div className="bg-cream py-4 px-6 rounded-2xl mb-4 flex items-center justify-between border border-stone">
            <h2 className="font-serif text-xl font-semibold">Live Legal Assistant</h2>
            <div className="text-xs font-semibold bg-white px-3 py-1 rounded-full text-green-600 border border-stone flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500"></div> Online
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-2xl px-5 py-3 text-[15px] leading-relaxed ${msg.role === 'user' ? 'bg-charcoal text-cream rounded-br-sm' : 'bg-[#f4f1ed] text-charcoal border border-stone rounded-bl-sm'}`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-[85%] rounded-2xl px-5 py-4 bg-[#f4f1ed] border border-stone rounded-bl-sm flex items-center gap-2 animate-pulse">
                  <span className="w-2 h-2 rounded-full bg-gray-400"></span>
                  <span className="w-2 h-2 rounded-full bg-gray-400"></span>
                  <span className="w-2 h-2 rounded-full bg-gray-400"></span>
                </div>
              </div>
            )}
          </div>

          <div className="px-2 pt-2 flex gap-2 overflow-x-auto">
            <button 
              onClick={() => setInput("I'm Priya Nair from Mumbai. I returned a kurta to Flipkart on Feb 28, but my Rs.4500 refund was never processed. I want an immediate refund.")}
              className="text-xs font-medium text-stone-500 bg-[#f4f1ed] border border-stone hover:bg-[#e6e2db] hover:text-charcoal px-3 py-1.5 rounded-full transition whitespace-nowrap"
            >
              Flipkart Refund
            </button>
            <button 
              onClick={() => setInput("I'm Arjun Das from Kolkata. My food order from Zomato Ltd was delivered cold and incomplete. Support denied my Rs.350 refund!")}
              className="text-xs font-medium text-stone-500 bg-[#f4f1ed] border border-stone hover:bg-[#e6e2db] hover:text-charcoal px-3 py-1.5 rounded-full transition whitespace-nowrap"
            >
              Zomato Dispute
            </button>
            <button 
              onClick={() => setInput("I'm Ramesh Kumar from Delhi. My OLED TV from LG Electronics developed dead pixels after 2 months. They refuse to replace my Rs.75000 unit.")}
              className="text-xs font-medium text-stone-500 bg-[#f4f1ed] border border-stone hover:bg-[#e6e2db] hover:text-charcoal px-3 py-1.5 rounded-full transition whitespace-nowrap"
            >
              LG Electronics
            </button>
            <button 
              onClick={() => setInput("I'm Fatima from Hyderabad. My Reliance Jio internet stopped working on March 5 and they refuse to refund my Rs.599 monthly plan.")}
              className="text-xs font-medium text-stone-500 bg-[#f4f1ed] border border-stone hover:bg-[#e6e2db] hover:text-charcoal px-3 py-1.5 rounded-full transition whitespace-nowrap"
            >
              Reliance Jio
            </button>
            <button 
              onClick={() => setInput("I'm Meena from Chennai. My boAt Lifestyle earphones stopped working after 10 days of use. I demand a replacement or full Rs.2999 refund.")}
              className="text-xs font-medium text-stone-500 bg-[#f4f1ed] border border-stone hover:bg-[#e6e2db] hover:text-charcoal px-3 py-1.5 rounded-full transition whitespace-nowrap"
            >
              boAt Earphones
            </button>
          </div>
          
          <div className="mt-2 bg-white rounded-full border border-stone p-1.5 flex items-center shadow-sm">
            <input
              type="file"
              id="receipt-upload"
              className="hidden"
              accept="image/*"
              onChange={async (e) => {
                 const file = e.target.files[0];
                 if (!file || !sessionId) return;
                 setMessages(prev => [...prev, { role: 'user', text: `📎 Uploading ${file.name}...` }]);
                 setIsLoading(true);
                 
                 const formData = new FormData();
                 formData.append("file", file);
                 
                 try {
                     const res = await fetch(`${API_BASE_URL}/api/upload_receipt?session_id=${sessionId}`, {
                         method: "POST",
                         body: formData
                     });
                     const data = await res.json();
                     if (!res.ok) throw new Error(data.detail || "Upload failed");
                     
                     setMessages(prev => [...prev, { role: 'ai', text: "✅ Bill scanned! I've updated your case with the Merchant, Date, and Amount. What happened exactly?" }]);
                 } catch (err) {
                     const errorMsg = err.message || err.detail || String(err);
                     setMessages(prev => [...prev, { role: 'ai', text: `Vision Error: ${errorMsg}` }]);
                 } finally {
                     setIsLoading(false);
                 }
              }}
            />
            <label htmlFor="receipt-upload" className="cursor-pointer bg-[#f4f1ed] text-charcoal rounded-full w-10 h-10 flex items-center justify-center hover:bg-stone transition ml-1 shrink-0">
               📎
            </label>
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder={isRecording ? "Recording... (Click mic to stop)" : "Explain your legal dispute..."}
              className="flex-1 px-5 py-2 focus:outline-none bg-transparent min-w-0"
              disabled={isRecording}
            />
            
            <button 
              onClick={isRecording ? stopRecording : startRecording}
              className={`mr-1 rounded-full w-10 h-10 flex items-center justify-center transition shrink-0 ${isRecording ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
            >
              🎤
            </button>

            <button 
              onClick={handleSend}
              className="bg-charcoal text-cream rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-800 transition shrink-0 disabled:opacity-50"
              disabled={isRecording}
            >
              ➔
            </button>
          </div>

          {isComplete && (
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 animate-bounce">
              <a 
                href={`${API_BASE_URL}/api/download_notice/${sessionId}`} 
                target="_blank" 
                rel="noreferrer" 
                className="bg-charcoal text-cream hover:bg-gold hover:text-charcoal px-8 py-5 rounded-full font-serif text-xl border-4 border-cream shadow-[0_20px_50px_rgba(0,0,0,0.3)] transition-all whitespace-nowrap flex items-center gap-3"
              >
                📄 Download Legal Notice (PDF)
              </a>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
