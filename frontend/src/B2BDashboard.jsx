import React, { useEffect, useState } from 'react';

export default function B2BDashboard() {
  const [notices, setNotices] = useState([]);
  const [selectedNotice, setSelectedNotice] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [riskLoading, setRiskLoading] = useState(false);

  useEffect(() => {
    fetch('https://nyaya-voice-backend.onrender.com/api/b2b/notices')
      .then(r => r.json())
      .then(d => setNotices(d));
  }, []);

  const handleViewRisk = (sessionId) => {
    setSelectedNotice(sessionId);
    setRiskLoading(true);
    fetch(`https://nyaya-voice-backend.onrender.com/api/b2b/risk/${sessionId}`)
      .then(r => r.json())
      .then(d => {
        setRiskData(d);
        setRiskLoading(false);
      });
  };

  const closeRiskModal = () => {
    setSelectedNotice(null);
    setRiskData(null);
  };

  return (
    <div className="min-h-screen bg-stone-50 p-8 text-charcoal flex flex-col items-center">
      <div className="w-full max-w-7xl">
          <header className="mb-8 md:mb-12 border-b border-stone-300 pb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-serif font-bold text-gray-900 tracking-tight mb-2">Corporate Defense Portal</h1>
              <p className="text-gray-500 text-base md:text-lg">Manage incoming pre-litigation notices and AI risk probabilities.</p>
            </div>
            <div className="bg-charcoal text-white px-4 py-2 rounded-lg font-mono text-sm whitespace-nowrap">
              Active Alerts: {notices.length}
            </div>
          </header>

          <div className="w-full bg-white rounded-2xl shadow-sm border border-stone-200 overflow-x-auto">
            <table className="w-full text-left border-collapse min-w-[800px]">
              <thead>
                <tr className="bg-stone-100 border-b border-stone-300">
                  <th className="p-5 font-semibold text-gray-600">Notice UUID</th>
                  <th className="p-5 font-semibold text-gray-600">Company (Opponent)</th>
                  <th className="p-5 font-semibold text-gray-600">Dispute Value</th>
                  <th className="p-5 font-semibold text-gray-600 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {notices.map(notice => (
                  <tr key={notice.session_id} className="border-b border-stone-100 hover:bg-stone-50 transition">
                    <td className="p-5 font-mono text-sm text-gray-500 truncate max-w-[150px]">{notice.session_id}</td>
                    <td className="p-5 font-medium max-w-[200px] truncate">{notice.facts.opponent_name}</td>
                    <td className="p-5">Rs. {notice.facts.dispute_amount}</td>
                    <td className="p-5 text-right flex justify-end gap-2">
                      <a href={`/verify/${notice.session_id}`} target="_blank" className="font-semibold text-charcoal outline p-2 border border-gray rounded-md hover:bg-gray-100 transition mr-2">Open QR Verify</a>
                      <button 
                        onClick={() => handleViewRisk(notice.session_id)}
                        className="bg-red-50 text-red-600 hover:bg-red-100 border border-red-200 px-4 py-2 rounded-lg font-medium transition text-sm whitespace-nowrap"
                      >
                        View AI Risk Score
                      </button>
                    </td>
                  </tr>
                ))}
                {notices.length === 0 && (
                  <tr>
                    <td colSpan="4" className="p-10 text-center text-gray-400 italic">No incoming notices detected.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
      </div>

      {/* Risk Modal */}
      {selectedNotice && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-8 max-w-2xl w-full relative shadow-2xl">
            <button onClick={closeRiskModal} className="absolute top-6 right-6 text-gray-400 hover:text-black text-2xl font-bold">&times;</button>
            <h2 className="text-2xl font-serif font-bold mb-6">Automated Risk Analysis</h2>
            
            {riskLoading ? (
              <div className="py-20 text-center">
                 <div className="w-12 h-12 border-4 border-stone-200 border-t-red-500 rounded-full animate-spin mx-auto mb-4"></div>
                 <p className="text-gray-500 font-medium">Gemini Defense Subagent calculating odds...</p>
                 <p className="text-gray-400 text-sm mt-2 font-mono truncate">ID: {selectedNotice}</p>
              </div>
            ) : riskData && (
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row gap-6">
                  {/* Gauge Simulator */}
                  <div className="w-full sm:w-1/3 bg-stone-50 rounded-2xl p-6 flex flex-col items-center justify-center border border-stone-200">
                    <div className={`text-5xl sm:text-6xl font-black ${riskData.risk_score > 70 ? 'text-red-500' : 'text-orange-500'}`}>
                      {riskData.risk_score}%
                    </div>
                    <div className="text-xs uppercase font-bold text-gray-400 mt-2 tracking-wider text-center">Litigation Risk</div>
                  </div>
                  
                  <div className="w-full sm:w-2/3 space-y-4">
                    <div className="bg-red-50 border border-red-100 rounded-xl p-4">
                      <h4 className="font-bold text-red-800 mb-1 flex items-center gap-2">Legal Vulnerability</h4>
                      <p className="text-red-900 text-sm leading-relaxed">{riskData.legal_vulnerability}</p>
                    </div>
                    <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
                      <h4 className="font-bold text-blue-800 mb-1 flex items-center gap-2">Est. Court Cost</h4>
                      <p className="text-blue-900 text-md font-bold leading-relaxed">{riskData.estimated_cost}</p>
                    </div>
                  </div>
                </div>
                
                <div className="bg-stone-900 text-white rounded-2xl p-6 mt-4">
                  <h4 className="font-bold mb-2 uppercase text-xs tracking-widest text-stone-400">Action Plan (AI Recommendation)</h4>
                  <p className="text-lg font-serif tracking-wide">{riskData.recommendation}</p>
                </div>
                
                <button 
                  onClick={closeRiskModal}
                  className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-xl shadow-lg transition tracking-wider"
                >
                  Settle Case and Archive Notice ✓
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
