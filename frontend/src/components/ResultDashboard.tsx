import React from 'react';
import { InvestigationResult } from '../types';
import { AlertOctagon, CheckCircle2, ShieldAlert, FileSpreadsheet, Download, ExternalLink, Activity, ArrowRight, CornerDownRight } from 'lucide-react';

interface ResultDashboardProps {
  result: InvestigationResult;
  onReset: () => void;
}

export const ResultDashboard: React.FC<ResultDashboardProps> = ({ result, onReset }) => {
  const isHighRisk = result.risk_level === 'HIGH' || result.risk_level === 'CRITICAL';

  const handleDownloadReport = () => {
    window.open(`/api/investigations/${result.investigation_id}/report`, '_blank');
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Top Banner: Risk Assessment */}
      <div className={`rounded-2xl p-6 sm:p-8 border shadow-2xl transition ${
        isHighRisk ? 'bg-rose-950/40 border-rose-800/80 shadow-rose-950/50' : 'bg-amber-950/30 border-amber-800/60 shadow-amber-950/30'
      }`}>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <div className={`p-3.5 rounded-2xl ${isHighRisk ? 'bg-rose-600 text-white' : 'bg-amber-600 text-white'}`}>
              <AlertOctagon className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono tracking-wider uppercase text-slate-400">RAKSHA CALIBRATED RISK ASSESSMENT</span>
                <span className="text-xs text-slate-500">• ID: {result.investigation_id}</span>
              </div>
              <h2 className={`text-2xl sm:text-3xl font-extrabold tracking-tight ${isHighRisk ? 'text-rose-400' : 'text-amber-400'}`}>
                {result.risk_level} RISK SOLICITATION
              </h2>
            </div>
          </div>

          <div className="flex items-center space-x-4 bg-slate-950/60 p-3 rounded-xl border border-slate-800">
            <div>
              <div className="text-xs text-slate-400">Calibrated Scam Prob</div>
              <div className="text-xl font-bold font-mono text-slate-100">
                {Math.round(result.risk_probability * 100)}%
              </div>
            </div>
            <div className="h-8 w-px bg-slate-800" />
            <div>
              <div className="text-xs text-slate-400">Confidence Score</div>
              <div className="text-xl font-bold font-mono text-slate-100">
                {Math.round(result.confidence * 100)}%
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer banner separating ML model estimate from authoritative facts */}
        <div className="mt-4 p-3 bg-slate-900/80 rounded-lg border border-slate-800 text-xs text-slate-300 flex items-center justify-between">
          <span>
            <strong>IMPORTANT:</strong> ML risk score is a statistical model estimate. Regulatory verification is established separately by official SEBI database lookup.
          </span>
          <button
            onClick={handleDownloadReport}
            className="flex items-center space-x-1.5 bg-sky-600 hover:bg-sky-500 text-white px-3 py-1.5 rounded text-xs font-semibold transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Official PDF Report</span>
          </button>
        </div>
      </div>

      {/* WHY DID RAKSHA FLAG THIS? Grid */}
      <div>
        <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-sky-400" />
          <span>Why RAKSHA Flagged This Solicitaton</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          {/* Card 1: Authoritative SEBI Registry Verification */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider">Level 1 Authoritative Fact</span>
              <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                result.sebi_verification.status === 'VERIFIED' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-rose-950 text-rose-400 border border-rose-800'
              }`}>
                {result.sebi_verification.status}
              </span>
            </div>
            <h4 className="font-bold text-slate-100 text-sm">SEBI Intermediary Registry Check</h4>
            <p className="text-xs text-slate-400 leading-relaxed">{result.sebi_verification.reason}</p>
            {result.claims.registration_numbers.length > 0 && (
              <div className="text-xs font-mono bg-slate-950 p-2 rounded border border-slate-800 text-slate-300">
                Claimed Reg: {result.claims.registration_numbers.join(', ')}
              </div>
            )}
          </div>

          {/* Card 2: NCRP Cybercrime & Phishing Intelligence */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider">Level 2/3 Intelligence</span>
              <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                result.cybercrime_verification.status === 'MATCH' ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-slate-800 text-slate-300'
              }`}>
                {result.cybercrime_verification.status}
              </span>
            </div>
            <h4 className="font-bold text-slate-100 text-sm">National Cybercrime & Threat Intelligence</h4>
            <p className="text-xs text-slate-400 leading-relaxed">{result.cybercrime_verification.reason}</p>
          </div>

          {/* Card 3: NLP Text Model Analysis */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Level 4 ML Model Estimate</span>
              <span className="text-xs font-mono font-bold text-sky-400">
                {Math.round(result.nlp_analysis.scam_probability * 100)}% Scam Risk
              </span>
            </div>
            <h4 className="font-bold text-slate-100 text-sm">Multilingual NLP Text Classifier</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Analyzed social engineering language, return promises, and channel migration markers.
            </p>
          </div>

          {/* Card 4: URL Classifier */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Level 4 URL Model Estimate</span>
              <span className="text-xs font-mono font-bold text-amber-400">
                {result.url_analysis.phishing_probability ? `${Math.round(result.url_analysis.phishing_probability * 100)}% Phishing` : 'No URL'}
              </span>
            </div>
            <h4 className="font-bold text-slate-100 text-sm">Domain & Lexical URL Classifier</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              {result.url_analysis.url ? `Inspected domain host '${result.url_analysis.hostname}' for suspicious TLD, entropy, and IP structure.` : 'No external web domain detected in solicitation text.'}
            </p>
          </div>

        </div>
      </div>

      {/* Behavioral Red Flags List */}
      {result.behavioral_red_flags.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h4 className="text-sm font-bold text-slate-200 mb-3 uppercase tracking-wider flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-rose-500" />
            <span>Behavioral Red Flags Triggered ({result.behavioral_red_flags.length})</span>
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {result.behavioral_red_flags.map((flag) => (
              <div key={flag.id} className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs">
                <div className="font-bold text-rose-300">{flag.id}: {flag.name}</div>
                <div className="text-slate-400 mt-1">{flag.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Visual Evidence Graph */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h4 className="text-sm font-bold text-slate-200 mb-4 uppercase tracking-wider">
          Evidence Network Graph
        </h4>
        <div className="flex flex-wrap items-center gap-3 bg-slate-950 p-6 rounded-xl border border-slate-800">
          {result.evidence_graph.nodes.map((node) => (
            <div
              key={node.id}
              className={`px-3 py-2 rounded-lg text-xs font-mono font-semibold border ${
                node.risk === 'danger' ? 'bg-rose-950 text-rose-300 border-rose-800' :
                node.risk === 'warning' ? 'bg-amber-950 text-amber-300 border-amber-800' :
                'bg-slate-900 text-slate-300 border-slate-700'
              }`}
            >
              {node.label}
            </div>
          ))}
        </div>
      </div>

      {/* What You Should Do: Protective Directives */}
      <div className="bg-sky-950/40 border border-sky-800/80 rounded-2xl p-6 sm:p-8">
        <h3 className="text-lg font-extrabold text-sky-400 mb-2">
          PAUSE BEFORE YOU PAY: Protective Action Required
        </h3>
        <p className="text-xs text-slate-300 mb-4">
          {result.recommended_action}
        </p>

        <div className="space-y-2">
          {result.safety_do_not_list.map((item, idx) => (
            <div key={idx} className="flex items-start space-x-2 text-xs text-slate-200">
              <span className="text-rose-400 font-bold">✕</span>
              <span>{item}</span>
            </div>
          ))}
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={handleDownloadReport}
            className="bg-sky-600 hover:bg-sky-500 text-white font-semibold px-4 py-2 rounded-xl text-xs flex items-center space-x-2 transition"
          >
            <Download className="w-4 h-4" />
            <span>Download PDF Evidence Report</span>
          </button>
          
          <button
            onClick={onReset}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold px-4 py-2 rounded-xl text-xs transition"
          >
            Investigate Another Solicitaton
          </button>
        </div>
      </div>
    </div>
  );
};
