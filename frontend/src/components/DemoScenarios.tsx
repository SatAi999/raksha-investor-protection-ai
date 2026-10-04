import React from 'react';
import { Play, ShieldAlert, CheckCircle2, FileText } from 'lucide-react';

interface DemoScenariosProps {
  onSelectScenario: (text: string) => void;
  isLoading: boolean;
}

export const DemoScenarios: React.FC<DemoScenariosProps> = ({ onSelectScenario, isLoading }) => {
  const scenarios = [
    {
      id: 'demo1',
      title: 'Fake SEBI Approved Guaranteed Investment Scam',
      badge: 'HIGH RISK DEMO',
      badgeStyle: 'bg-rose-950 text-rose-400 border-rose-800',
      description: 'Promises guaranteed 18% monthly return, urgent 5 seat limit, deposit request on Telegram app, unverified SEBI reg INZ000293847.',
      sampleText: 'SEBI APPROVED INVESTMENT OPPORTUNITY! Guaranteed 18% monthly return. Only 5 seats remaining. Deposit ₹25,000 today. Our expert will guide you on Telegram. Download trading app: http://sebi-pro-trader.top/app.apk SEBI Reg: INZ000293847'
    },
    {
      id: 'demo2',
      title: 'Legitimate SEBI & Broker Educational Notice',
      badge: 'LOW RISK DEMO',
      badgeStyle: 'bg-emerald-950 text-emerald-400 border-emerald-800',
      description: 'Official Zerodha and SEBI investor warning reminding investors that registered brokers never promise guaranteed returns.',
      sampleText: 'Zerodha Safety Alert: We do not operate any Telegram groups offering guaranteed stock tips or fund management services. Beware of unregistered advisors. Official SEBI website www.sebi.gov.in.'
    },
    {
      id: 'demo3',
      title: 'Hindi Guaranteed Stock Tips Telegram Group',
      badge: 'MULTILINGUAL DEMO',
      badgeStyle: 'bg-amber-950 text-amber-400 border-amber-800',
      description: 'Hindi investment solicitation promising 15% fixed daily profit with minimum deposit of ₹10,000 via Telegram group link.',
      sampleText: 'नमस्ते निवेशक! SEBI द्वारा पंजीकृत हमारी टीम आपको प्रतिदिन 15% का निश्चित लाभ देगी। न्यूनतम निवेश ₹10,000। अभी टेलीग्राम ग्रुप ज्वाइन करें: https://sebi-trade-group.app'
    },
    {
      id: 'demo4',
      title: 'Direct Pre-IPO Escrow Allotment Guarantee',
      badge: 'HIGH RISK DEMO',
      badgeStyle: 'bg-rose-950 text-rose-400 border-rose-800',
      description: 'Fake IPO share allotment claim requiring upfront escrow UPI payment to personal handle with claimed merchant banker registration.',
      sampleText: 'Direct IPO Allotment Guarantee! Get 1000 shares of Tata Capital before listing. Transfer funds to Escrow UPI ID: sebi.escrow@ybl. Registration number: INM000012345.'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <h2 className="text-xl font-bold text-white mb-2 flex items-center space-x-2">
          <FileText className="w-5 h-5 text-sky-400" />
          <span>RAKSHA Hackathon Live Demonstration Suite</span>
        </h2>
        <p className="text-xs text-slate-400">
          Select any real-world demonstration scenario to trigger the complete end-to-end OCR/NLP/URL/SEBI verification pipeline.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {scenarios.map((sc) => (
          <div key={sc.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between space-y-4 hover:border-slate-700 transition">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${sc.badgeStyle}`}>
                  {sc.badge}
                </span>
              </div>
              <h3 className="font-bold text-slate-100 text-sm">{sc.title}</h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">{sc.description}</p>
              
              <div className="mt-3 bg-slate-950 p-3 rounded border border-slate-800 text-[11px] font-mono text-slate-300 line-clamp-3">
                "{sc.sampleText}"
              </div>
            </div>

            <button
              onClick={() => onSelectScenario(sc.sampleText)}
              disabled={isLoading}
              className="w-full bg-sky-600 hover:bg-sky-500 text-white font-semibold py-2.5 rounded-lg text-xs transition flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5" />
              <span>Run Live Investigation</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
