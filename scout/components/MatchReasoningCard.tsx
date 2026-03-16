import { GrantOpportunity } from '@/lib/types';
import SubmissionTimeline from './SubmissionTimeline';

export default function MatchReasoningCard({ grant }: { grant: GrantOpportunity }) {
  return (
    <div className="flex flex-col gap-6 text-sm text-neutral-300">
      <div>
        <h4 className="font-semibold text-white text-base mb-2">Summary</h4>
        <p className="leading-relaxed">{grant.summary}</p>
      </div>
      
      <div>
        <h4 className="font-semibold text-white text-base mb-2">Eligibility</h4>
        <p className="leading-relaxed">{grant.eligibility}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-emerald-500/5 border border-emerald-500/10 rounded-xl p-4">
          <h4 className="font-semibold text-emerald-400 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
            Strengths
          </h4>
          <ul className="space-y-2">
            {grant.strengths.map((str, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-red-500/5 border border-red-500/10 rounded-xl p-4">
          <h4 className="font-semibold text-red-400 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            Risks & Hurdles
          </h4>
          <ul className="space-y-2">
            {grant.risks.length > 0 ? grant.risks.map((risk, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-red-500 mt-0.5">•</span>
                <span>{risk}</span>
              </li>
            )) : <li className="text-neutral-500">No major risks identified.</li>}
          </ul>
        </div>
      </div>

      {grant.status === 'open' && (
        <div className="mt-4 pt-6 border-t border-neutral-800">
          <h4 className="font-semibold text-white text-base mb-4">Initial Preparation Timeline</h4>
          <SubmissionTimeline grantId={grant.id} />
          
          <div className="mt-8 flex justify-end">
             <a 
               href={grant.sourceUrl} 
               target="_blank" 
               rel="noopener noreferrer"
               className="bg-white text-black font-semibold py-2 px-4 rounded-lg hover:bg-neutral-200 transition-colors"
             >
               Visit Official Portal
             </a>
          </div>
        </div>
      )}
    </div>
  );
}
