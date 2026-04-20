"use client";
import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import axios from "axios";
import {
  Sparkles,
  AlertTriangle,
  Clock,
  MapPin,
  ArrowRight,
  Loader2,
  Utensils,
  Camera,
} from "lucide-react";

interface TripData {
  status: string;
  destination: string;
  reality_report: string;
  itinerary?: Record<string, string | string[]>; // Support for both string and arrays
}

export default function TripResult() {
  const { id } = useParams();
  const [data, setData] = useState<TripData | null>(null);
  const [loading, setLoading] = useState(true);
  const [approving, setApproving] = useState(false);

  const fetchReport = useCallback(async () => {
    try {
      const res = await axios.get(`http://localhost:8000/trip-status/${id}`);
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (id) fetchReport();
  }, [id, fetchReport]);

  const handleApprove = async () => {
    setApproving(true);
    try {
      const res = await axios.post(`http://localhost:8000/approve-trip/${id}`);
      setData(res.data);
    } catch (err) {
      alert("Planning failed!");
    } finally {
      setApproving(false);
    }
  };

  if (loading)
    return (
      <div className="min-h-screen bg-[#0F172A] flex items-center justify-center text-white">
        <Loader2 className="animate-spin mr-2" /> Researching...
      </div>
    );

  return (
    <main className="min-h-screen bg-[#0F172A] text-slate-200 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header - Simple & Clean */}
        <div className="flex justify-between items-center border-b border-slate-700 pb-6">
          <div>
            <h1 className="text-4xl font-extrabold text-white">
              Intelligence Report
            </h1>
            <p className="text-slate-400 mt-2 flex items-center gap-2">
              <MapPin size={16} className="text-indigo-400" />{" "}
              {data?.destination}
            </p>
          </div>
          <div
            className={`px-4 py-2 rounded-full text-xs font-bold uppercase tracking-widest border ${
              data?.status === "COMPLETED"
                ? "bg-emerald-500/10 text-emerald-400 border-emerald-400/20"
                : "bg-indigo-500/10 text-indigo-400 border-indigo-400/20"
            }`}
          >
            {data?.status}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {/* LEFT: Content Area */}
          <div className="lg:col-span-2 space-y-10">
            {/* 1. Research Report */}
            <div className="bg-slate-800/30 border border-slate-700/50 p-8 rounded-3xl backdrop-blur-sm">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <Sparkles className="text-indigo-400" /> Ground Reality Analysis
              </h2>
              <div className="text-slate-300 leading-relaxed whitespace-pre-wrap text-lg">
                {data?.reality_report}
              </div>
            </div>

            {/* 2. SMART ITINERARY (Phase-wise Segments) */}
            {data?.status === "COMPLETED" && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2 mb-8">
                  <Clock className="text-indigo-400" /> Optimized Time-Phase
                  Plan
                </h2>

                <div className="space-y-4">
                  {data.itinerary &&
                    Object.entries(data.itinerary).map(([phase, content]) => (
                      <div
                        key={phase}
                        className="bg-slate-800/50 border border-slate-700/50 rounded-3xl overflow-hidden shadow-xl"
                      >
                        {/* Phase Header */}
                        <div className="bg-slate-700/30 px-6 py-4 border-b border-slate-700/50 flex justify-between items-center">
                          <span className="text-indigo-400 font-black uppercase text-sm tracking-tighter italic">
                            {phase}
                          </span>
                        </div>

                        {/* Phase Points */}
                        <div className="p-6">
                          <ul className="space-y-4">
                            {/* Yahan hum bullet points render kar rahe hain */}
                            {(typeof content === "string"
                              ? content.split("\n")
                              : content
                            ).map((point, idx) => {
                              if (!point.trim()) return null;
                              return (
                                <li
                                  key={idx}
                                  className="flex gap-4 items-start group"
                                >
                                  <div className="mt-1.5 w-2 h-2 rounded-full bg-indigo-500 group-hover:scale-125 transition-transform shadow-[0_0_8px_rgba(99,102,241,0.6)]" />
                                  <span className="text-slate-300 text-lg leading-snug">
                                    {point.replace(/^\*|\-/, "").trim()}
                                  </span>
                                </li>
                              );
                            })}
                          </ul>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>

          {/* RIGHT: Sidebar Actions */}
          <div className="space-y-6">
            <div className="bg-slate-800/80 border border-slate-700 p-8 rounded-3xl sticky top-8 backdrop-blur-xl">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-3 text-white">
                <AlertTriangle className="text-amber-400" size={24} /> Safety
                Check
              </h3>
              <p className="text-slate-400 mb-8 leading-relaxed">
                Review the practical constraints above. Once approved, I'll
                generate the phase-wise execution plan.
              </p>

              {data?.status !== "COMPLETED" ? (
                <button
                  onClick={handleApprove}
                  disabled={approving}
                  className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-500/40"
                >
                  {approving ? (
                    <Loader2 className="animate-spin" />
                  ) : (
                    <>
                      Approve & Build Segments <ArrowRight size={18} />
                    </>
                  )}
                </button>
              ) : (
                <div className="space-y-4">
                  <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl text-emerald-400 font-bold flex flex-col items-center gap-1">
                    <span className="text-lg">✅ Logistics Verified</span>
                    <span className="text-[10px] opacity-70 uppercase tracking-widest text-center">
                      Itinerary includes Transit & Entry Points
                    </span>
                  </div>
                  <button className="w-full py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-xl font-medium text-sm">
                    Modify Phase Settings
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
