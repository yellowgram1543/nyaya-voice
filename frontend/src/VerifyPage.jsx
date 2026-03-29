import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function VerifyPage() {
  const { sessionId } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/api/verify/${sessionId}`)
      .then(res => {
        if (!res.ok) throw new Error("Verification Failed");
        return res.json();
      })
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, [sessionId]);

  if (loading) return <div className="min-h-screen flex items-center justify-center p-8 bg-[#fdfcfaf5] text-xl font-serif">Verifying Digital Signatures...</div>;

  if (error) return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#fdfcfaf5] text-charcoal">
      <div className="bg-red-50 text-red-600 p-8 rounded-2xl max-w-md text-center border border-red-200">
        <h1 className="text-3xl font-serif font-bold mb-4">⚠️ Verification Failed</h1>
        <p className="mb-6">This physical document does not match any official Nyaya-Voice records. It may be fraudulent or tampered with.</p>
        <Link to="/" className="underline text-red-800 font-semibold">Return to Home</Link>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col items-center py-20 bg-[#fdfcfaf5] text-charcoal p-4">
      <div className="w-full max-w-2xl bg-white p-10 rounded-[2rem] shadow-sm border border-green-200 relative overflow-hidden">
        <div className="absolute top-0 w-full h-2 left-0 bg-green-500"></div>
        <div className="flex items-center gap-4 mb-8">
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-2xl">✅</div>
            <div>
              <h1 className="text-3xl font-serif font-bold text-green-800">Verified Legal Notice</h1>
              <p className="text-sm font-mono text-gray-400">UUID: {data.session_id}</p>
            </div>
        </div>

        <p className="text-lg leading-relaxed mb-8 border-b border-stone pb-8">
          This digital tracking page confirms that a legal notice was officially drafted and stored by the Nyaya-Voice Legal Engine on behalf of the consumer below.
        </p>

        <div className="space-y-4">
          <div className="flex justify-between p-4 bg-cream rounded-xl border border-stone-200">
            <span className="font-semibold">Opponent</span>
            <span className="text-right max-w-[60%]">{data.facts.opponent_name}</span>
          </div>
          <div className="flex justify-between p-4 bg-cream rounded-xl border border-stone-200">
            <span className="font-semibold">Dispute Amount</span>
            <span>Rs. {data.facts.dispute_amount}</span>
          </div>
          <div className="flex justify-between p-4 bg-cream rounded-xl border border-stone-200">
            <span className="font-semibold">Incident Date</span>
            <span>{data.facts.incident_date}</span>
          </div>
          <div className="p-4 bg-stone-50 rounded-xl border border-stone-200 mt-4">
            <span className="font-semibold block mb-2">Core Grievance</span>
            <p className="text-gray-700 italic">"{data.facts.core_issue}"</p>
          </div>
        </div>

        <div className="mt-10 text-center text-sm text-gray-400 border-t border-stone pt-6">
          Powered by Nyaya-Voice Native Storage <br/>
          <Link to="/" className="text-charcoal underline mt-2 inline-block">Visit Client App</Link>
        </div>
      </div>
    </div>
  );
}
