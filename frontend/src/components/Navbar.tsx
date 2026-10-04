import React from 'react';
import { Shield, AlertTriangle, Globe, Activity } from 'lucide-react';

interface NavbarProps {
  language: 'en' | 'hi' | 'hinglish';
  setLanguage: (lang: 'en' | 'hi' | 'hinglish') => void;
  onOpenRecovery: () => void;
  onSelectTab: (tab: 'investigate' | 'demo' | 'dashboard') => void;
  activeTab: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  language,
  setLanguage,
  onOpenRecovery,
  onSelectTab,
  activeTab
}) => {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo & Tagline */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => onSelectTab('investigate')}>
          <div className="bg-sky-600 p-2 rounded-lg text-white shadow-lg shadow-sky-600/20">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-xl tracking-tight text-white">RAKSHA</span>
              <span className="text-xs bg-sky-950 text-sky-400 border border-sky-800 px-2 py-0.5 rounded font-mono">
                SAFETY INFRASTRUCTURE
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">Before You Pay. Verify.</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="hidden md:flex items-center space-x-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => onSelectTab('investigate')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'investigate' ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            Investigate
          </button>
          <button
            onClick={() => onSelectTab('demo')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'demo' ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            Live Demo Suite
          </button>
          <button
            onClick={() => onSelectTab('dashboard')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'dashboard' ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            Database Intelligence
          </button>
        </div>

        {/* Controls: Language, Recovery Mode, Live DB Badge */}
        <div className="flex items-center space-x-3">
          {/* Language Selector */}
          <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
            <Globe className="w-3.5 h-3.5 text-slate-400 mr-1.5" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as any)}
              className="bg-transparent text-xs font-medium text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="en" className="bg-slate-900">English</option>
              <option value="hi" className="bg-slate-900">हिन्दी (Hindi)</option>
              <option value="hinglish" className="bg-slate-900">Hinglish</option>
            </select>
          </div>

          {/* Emergency Recovery Button */}
          <button
            onClick={onOpenRecovery}
            className="flex items-center space-x-1.5 bg-rose-950/60 hover:bg-rose-900/80 border border-rose-800/80 text-rose-300 px-3 py-1.5 rounded-lg text-xs font-semibold transition"
          >
            <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
            <span>Already Transferred Money?</span>
          </button>
        </div>

      </div>
    </header>
  );
};
