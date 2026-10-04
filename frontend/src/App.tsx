import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { UploadSection } from './components/UploadSection';
import { ResultDashboard } from './components/ResultDashboard';
import { RecoveryModeModal } from './components/RecoveryModeModal';
import { DemoScenarios } from './components/DemoScenarios';
import { DatabaseDashboard } from './components/DatabaseDashboard';
import { investigateText, investigateImage, investigateAudio } from './services/api';
import { InvestigationResult } from './types';
import { Shield, AlertCircle } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<'investigate' | 'demo' | 'dashboard'>('investigate');
  const [language, setLanguage] = useState<'en' | 'hi' | 'hinglish'>('en');
  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isRecoveryOpen, setIsRecoveryOpen] = useState(false);

  const handleInvestigateText = async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await investigateText(text);
      setResult(res);
      setActiveTab('investigate');
    } catch (e: any) {
      setError(e.message || 'Investigation request failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInvestigateImage = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await investigateImage(file);
      setResult(res);
      setActiveTab('investigate');
    } catch (e: any) {
      setError(e.message || 'Screenshot OCR processing failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInvestigateAudio = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await investigateAudio(file);
      setResult(res);
      setActiveTab('investigate');
    } catch (e: any) {
      setError(e.message || 'Audio transcription processing failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        language={language}
        setLanguage={setLanguage}
        onOpenRecovery={() => setIsRecoveryOpen(true)}
        onSelectTab={setActiveTab}
        activeTab={activeTab}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Error Notification */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-300 text-xs flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 text-rose-400" />
              <span>{error}</span>
            </div>
            <button onClick={() => setError(null)} className="text-slate-400 hover:text-white">Dismiss</button>
          </div>
        )}

        {/* Tab 1: Primary Investigation & Result View */}
        {activeTab === 'investigate' && (
          <div className="space-y-8">
            {!result && (
              <UploadSection
                onInvestigateText={handleInvestigateText}
                onInvestigateImage={handleInvestigateImage}
                onInvestigateAudio={handleInvestigateAudio}
                isLoading={isLoading}
                language={language}
              />
            )}

            {result && (
              <ResultDashboard
                result={result}
                onReset={() => setResult(null)}
              />
            )}
          </div>
        )}

        {/* Tab 2: Live Demo Suite */}
        {activeTab === 'demo' && (
          <DemoScenarios
            onSelectScenario={handleInvestigateText}
            isLoading={isLoading}
          />
        )}

        {/* Tab 3: Database Dashboard */}
        {activeTab === 'dashboard' && (
          <DatabaseDashboard />
        )}

      </main>

      <RecoveryModeModal
        isOpen={isRecoveryOpen}
        onClose={() => setIsRecoveryOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-sky-500" />
            <span className="font-bold text-slate-300">RAKSHA Public-Good Safety Infrastructure</span>
          </div>
          <div>SANGYAN Investor Resilience Hackathon | Non-Commercial Public-Good Positioning</div>
        </div>
      </footer>
    </div>
  );
}
export default App;
