import React, { useEffect, useState } from 'react';
import { fetchDashboardStats } from '../services/api';
import { Database, ShieldCheck, AlertOctagon, Link2, RefreshCw } from 'lucide-react';

export const DatabaseDashboard: React.FC = () => {
  const [stats, setStats] = useState<any>({
    total_investigations: 0,
    high_risk_interceptions: 0,
    urls_analyzed: 0,
    unverified_sebi_claims: 0
  });
  const [loading, setLoading] = useState(true);

  const loadStats = async () => {
    setLoading(true);
    try {
      const data = await fetchDashboardStats();
      setStats(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white mb-1 flex items-center space-x-2">
            <Database className="w-5 h-5 text-sky-400" />
            <span>RAKSHA Database Telemetry & Interception Statistics</span>
          </h2>
          <p className="text-xs text-slate-400">
            Real database audit records fetched dynamically from SQLite / PostgreSQL telemetry tables.
          </p>
        </div>
        <button
          onClick={loadStats}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          title="Refresh Stats"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-2">
          <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Total Investigations</div>
          <div className="text-3xl font-extrabold font-mono text-white">{stats.total_investigations}</div>
          <div className="text-[11px] text-slate-500">Live database audit log</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-2">
          <div className="text-xs text-rose-400 font-semibold uppercase tracking-wider">High Risk Interceptions</div>
          <div className="text-3xl font-extrabold font-mono text-rose-400">{stats.high_risk_interceptions}</div>
          <div className="text-[11px] text-slate-500">Intercepted pre-transaction</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-2">
          <div className="text-xs text-amber-400 font-semibold uppercase tracking-wider">URLs Analyzed</div>
          <div className="text-3xl font-extrabold font-mono text-amber-400">{stats.urls_analyzed}</div>
          <div className="text-[11px] text-slate-500">Domain lexical model checks</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-2">
          <div className="text-xs text-sky-400 font-semibold uppercase tracking-wider">SEBI Registry Checks</div>
          <div className="text-3xl font-extrabold font-mono text-sky-400">{stats.unverified_sebi_claims}</div>
          <div className="text-[11px] text-slate-500">Official registry lookups</div>
        </div>
      </div>
    </div>
  );
};
