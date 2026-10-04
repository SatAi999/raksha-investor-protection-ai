import React, { useState } from 'react';
import { Upload, FileText, Link, Mic, Play, Loader2 } from 'lucide-react';

interface UploadSectionProps {
  onInvestigateText: (text: string) => void;
  onInvestigateImage: (file: File) => void;
  onInvestigateAudio: (file: File) => void;
  isLoading: boolean;
  language: 'en' | 'hi' | 'hinglish';
}

export const UploadSection: React.FC<UploadSectionProps> = ({
  onInvestigateText,
  onInvestigateImage,
  onInvestigateAudio,
  isLoading,
  language
}) => {
  const [activeTab, setActiveTab] = useState<'screenshot' | 'text' | 'url' | 'audio'>('screenshot');
  const [textInput, setTextInput] = useState('');
  const [urlInput, setUrlInput] = useState('');

  const labels = {
    en: {
      headline: "Intercept Financial Solicitations Before Money Changes Hands",
      sub: "Upload WhatsApp/Telegram screenshots, paste advisory messages, URL domains, or voice notes for authoritative evidence verification.",
      startBtn: "Start Investigation",
      dropScreenshot: "Click or Drop WhatsApp/Telegram Screenshot Here",
      dropSub: "Supports PNG, JPG, WEBP formats. Real OCR text extraction.",
      pasteTextPlaceholder: "Paste WhatsApp message, Telegram post, guaranteed return offer, or claimed SEBI registration number...",
      pasteUrlPlaceholder: "https://suspicious-trading-domain.top",
      uploadAudioLabel: "Upload Voice Message / Call Recording (WAV, MP3)",
    },
    hi: {
      headline: "पैसे भेजने से पहले निवेश प्रस्ताव की तुरंत जांच करें",
      sub: "व्हाट्सएप/टेलीग्राम का स्क्रीनशॉट अपलोड करें, संदेश या वेबसाइट लिंक पेस्ट करें।",
      startBtn: "जांच शुरू करें (Investigate)",
      dropScreenshot: "व्हाट्सएप या टेलीग्राम स्क्रीनशॉट यहां अपलोड करें",
      dropSub: "PNG, JPG, WEBP समर्थित। स्वचालित OCR निष्कर्षण।",
      pasteTextPlaceholder: "व्हाट्सएप संदेश, टेलीग्राम पोस्ट या दावा किया गया SEBI पंजीकरण नंबर पेस्ट करें...",
      pasteUrlPlaceholder: "https://suspicious-trading-domain.top",
      uploadAudioLabel: "वॉयस मैसेज रिकॉर्डिंग अपलोड करें",
    },
    hinglish: {
      headline: "Money Transfer karne se pehle Verify karein",
      sub: "WhatsApp screenshot, text message ya URL paste karke official SEBI verification aur scam check karein.",
      startBtn: "Start Investigation",
      dropScreenshot: "Upload WhatsApp/Telegram Screenshot",
      dropSub: "PNG, JPG, WEBP formats supported.",
      pasteTextPlaceholder: "Paste WhatsApp/Telegram message or promised return scheme text here...",
      pasteUrlPlaceholder: "https://suspicious-domain.xyz",
      uploadAudioLabel: "Upload Voice Note (WAV, MP3)",
    }
  }[language];

  const handleImageFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onInvestigateImage(e.target.files[0]);
    }
  };

  const handleAudioFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onInvestigateAudio(e.target.files[0]);
    }
  };

  const handleTextSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (activeTab === 'url' && urlInput.trim()) {
      onInvestigateText(`Investigate URL: ${urlInput.trim()}`);
    } else if (textInput.trim()) {
      onInvestigateText(textInput.trim());
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl">
      <div className="text-center max-w-2xl mx-auto mb-8">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {labels.headline}
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          {labels.sub}
        </p>
      </div>

      {/* Input Selection Tabs */}
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        <button
          onClick={() => setActiveTab('screenshot')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'screenshot' ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/30' : 'bg-slate-800 text-slate-400 hover:text-white'
          }`}
        >
          <Upload className="w-4 h-4" />
          <span>Upload Screenshot</span>
        </button>

        <button
          onClick={() => setActiveTab('text')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'text' ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/30' : 'bg-slate-800 text-slate-400 hover:text-white'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Paste Message</span>
        </button>

        <button
          onClick={() => setActiveTab('url')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'url' ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/30' : 'bg-slate-800 text-slate-400 hover:text-white'
          }`}
        >
          <Link className="w-4 h-4" />
          <span>Paste URL Domain</span>
        </button>

        <button
          onClick={() => setActiveTab('audio')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'audio' ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/30' : 'bg-slate-800 text-slate-400 hover:text-white'
          }`}
        >
          <Mic className="w-4 h-4" />
          <span>Voice Note</span>
        </button>
      </div>

      {/* Tab Panels */}
      <div className="max-w-xl mx-auto">
        {activeTab === 'screenshot' && (
          <label className="border-2 border-dashed border-slate-700 hover:border-sky-500 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer transition bg-slate-950/40 group">
            <Upload className="w-10 h-10 text-slate-500 group-hover:text-sky-400 mb-3 transition" />
            <span className="text-sm font-semibold text-slate-200 group-hover:text-white">{labels.dropScreenshot}</span>
            <span className="text-xs text-slate-500 mt-1">{labels.dropSub}</span>
            <input type="file" accept="image/*" onChange={handleImageFile} className="hidden" disabled={isLoading} />
          </label>
        )}

        {activeTab === 'text' && (
          <form onSubmit={handleTextSubmit} className="space-y-4">
            <textarea
              rows={5}
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder={labels.pasteTextPlaceholder}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 resize-none font-mono"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !textInput.trim()}
              className="w-full bg-sky-600 hover:bg-sky-500 text-white font-semibold py-3 rounded-xl text-sm transition flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              <span>{labels.startBtn}</span>
            </button>
          </form>
        )}

        {activeTab === 'url' && (
          <form onSubmit={handleTextSubmit} className="space-y-4">
            <input
              type="text"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              placeholder={labels.pasteUrlPlaceholder}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 font-mono"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !urlInput.trim()}
              className="w-full bg-sky-600 hover:bg-sky-500 text-white font-semibold py-3 rounded-xl text-sm transition flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              <span>{labels.startBtn}</span>
            </button>
          </form>
        )}

        {activeTab === 'audio' && (
          <label className="border-2 border-dashed border-slate-700 hover:border-sky-500 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer transition bg-slate-950/40 group">
            <Mic className="w-10 h-10 text-slate-500 group-hover:text-sky-400 mb-3 transition" />
            <span className="text-sm font-semibold text-slate-200 group-hover:text-white">{labels.uploadAudioLabel}</span>
            <span className="text-xs text-slate-500 mt-1">Transcribes voice via Whisper ASR pipeline</span>
            <input type="file" accept="audio/*" onChange={handleAudioFile} className="hidden" disabled={isLoading} />
          </label>
        )}
      </div>

    </div>
  );
};
