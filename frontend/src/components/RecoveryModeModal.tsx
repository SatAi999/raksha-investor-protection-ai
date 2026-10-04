import React from 'react';
import { ShieldAlert, X, PhoneCall, Building2, FileCheck, ExternalLink } from 'lucide-react';

interface RecoveryModeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const RecoveryModeModal: React.FC<RecoveryModeModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 sm:p-8 shadow-2xl relative space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-rose-950 text-rose-400 border border-rose-800">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">RECOVERY & HARM REDUCTION MODE</h3>
              <p className="text-xs text-rose-400 font-medium">Immediate official steps if money was transferred</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step 1: Immediate Bank Stop Payment */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-xs font-bold text-sky-400 uppercase tracking-wider">
            <Building2 className="w-4 h-4" />
            <span>Step 1: Contact Bank Immediately</span>
          </div>
          <p className="text-xs text-slate-300">
            Call your bank's fraud reporting helpline or freeze your debit/credit card and NetBanking immediately to prevent secondary debits. Request a transaction freeze / chargeback request.
          </p>
        </div>

        {/* Step 2: National Cyber Crime Portal 1930 */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-xs font-bold text-rose-400 uppercase tracking-wider">
            <PhoneCall className="w-4 h-4" />
            <span>Step 2: Dial 1930 / File Cybercrime Incident</span>
          </div>
          <p className="text-xs text-slate-300">
            Report financial fraud immediately on India's National Cyber Crime Helpline <strong>1930</strong> or register an official complaint online at <a href="https://cybercrime.gov.in" target="_blank" rel="noreferrer" className="text-sky-400 underline inline-flex items-center">cybercrime.gov.in <ExternalLink className="w-3 h-3 ml-0.5" /></a> within the golden hour.
          </p>
        </div>

        {/* Step 3: Preserve Evidence */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
            <FileCheck className="w-4 h-4" />
            <span>Step 3: Preserve All Evidence</span>
          </div>
          <ul className="text-xs text-slate-400 space-y-1 list-disc list-inside">
            <li>Save transaction UTR numbers and payment receipts.</li>
            <li>Take full screenshots of WhatsApp / Telegram chats.</li>
            <li>Note down phone numbers, handles, and URLs.</li>
            <li>Do NOT delete chat history or block accounts until police report is filed.</li>
          </ul>
        </div>

        {/* Close button */}
        <button
          onClick={onClose}
          className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-2.5 rounded-xl text-xs transition"
        >
          Close Harm Reduction Guidance
        </button>

      </div>
    </div>
  );
};
