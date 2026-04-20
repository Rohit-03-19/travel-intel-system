"use client";
import React, { useState } from "react";
import { Search, MapPin, Sparkles, AlertCircle } from "lucide-react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function Home() {
  const [destination, setDestination] = useState("");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter(); // 2. Router initialize karo
  // ... baaki states

  const handlePlanTrip = async () => {
    if (!destination || !query)
      return alert("Bhai, destination aur vibe toh dalo!");

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/plan-trip", {
        user_query: query,
        destination: destination,
      });
      const threadId = res.data.thread_id;
      router.push(`/trip/${threadId}`); // User ko result page par le jao
    } catch (err) {
      alert("Error: Backend se data nahi mila!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0F172A] text-slate-200 selection:bg-indigo-500/30">
      {/* Background Decor */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-indigo-500/10 blur-[120px] pointer-events-none" />

      <div className="max-w-4xl mx-auto px-6 pt-32 pb-20 relative z-10">
        {/* Header Section */}
        <div className="text-center mb-16 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium mb-4">
            <Sparkles size={14} />
            <span>Next-Gen Travel Intelligence</span>
          </div>
          <h1 className="text-6xl font-bold tracking-tight text-white">
            Travel with <span className="text-indigo-500">Certainty.</span>
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            Deep-dive research into spiritual auras and ground realities,
            powered by Agentic AI.
          </p>
        </div>

        {/* Search Command Center */}
        <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 p-8 rounded-3xl shadow-2xl">
          <div className="grid gap-6">
            {/* Destination Input */}
            <div className="relative">
              <MapPin
                className="absolute left-4 top-4 text-slate-500"
                size={20}
              />
              <input
                type="text"
                placeholder="Where do you want to go?"
                className="w-full bg-slate-900/50 border border-slate-700 rounded-2xl py-4 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all text-white placeholder:text-slate-600"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
              />
            </div>

            {/* Vibe/Query Input */}
            <div className="relative">
              <Search
                className="absolute left-4 top-4 text-slate-500"
                size={20}
              />
              <textarea
                placeholder="Describe your vibe... (e.g. 'I want a soulful 1-day trip to Vrindavan, avoid crowds but include Banke Bihari temple')"
                className="w-full bg-slate-900/50 border border-slate-700 rounded-2xl py-4 pl-12 pr-4 h-32 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all text-white placeholder:text-slate-600 resize-none"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>

            {/* CTA Button */}
            <button
              onClick={handlePlanTrip}
              disabled={loading}
              className={`w-full py-4 rounded-2xl font-bold text-lg transition-all flex items-center justify-center gap-2
                ${
                  loading
                    ? "bg-slate-700 text-slate-400 cursor-not-allowed"
                    : "bg-indigo-600 hover:bg-indigo-50 hover:shadow-[0_0_20px_rgba(79,70,229,0.4)] text-white"
                }`}
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
                  Analyzing Ground Reality...
                </>
              ) : (
                "Generate Intelligence Report"
              )}
            </button>
          </div>
        </div>

        {/* Trust Indicators */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 opacity-60">
          <div className="flex items-center gap-3 text-sm">
            <Sparkles size={18} className="text-indigo-400" />
            <span>Spiritual Aura Analysis</span>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <AlertCircle size={18} className="text-amber-400" />
            <span>Real-time Safety Checks</span>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <MapPin size={18} className="text-emerald-400" />
            <span>Smart Route Planning</span>
          </div>
        </div>
      </div>
    </main>
  );
}
