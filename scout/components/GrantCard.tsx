'use client';

import { GrantOpportunity } from '@/lib/types';
import MatchReasoningCard from './MatchReasoningCard';
import { useState } from 'react';

export default function GrantCard({ grant }: { grant: GrantOpportunity }) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const scoreColor = 
    grant.matchScore >= 90 ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
    grant.matchScore >= 75 ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
    'bg-red-500/10 text-red-400 border-red-500/20';

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-2xl overflow-hidden shadow-sm transition-all hover:border-neutral-700">
      <div 
        className="p-6 cursor-pointer flex flex-col md:flex-row gap-4 justify-between items-start md:items-center"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="space-y-2 flex-1">
          <div className="flex items-center gap-3 mb-1">
            <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium border ${scoreColor}`}>
              {grant.matchScore}% Match
            </span>
            <span className="text-xs font-medium text-neutral-500 bg-neutral-800 px-2 py-1 rounded-md capitalize">
              {grant.status}
            </span>
          </div>
          <h3 className="text-xl font-bold text-white tracking-tight">{grant.title}</h3>
          <p className="text-sm font-medium text-neutral-400">{grant.funder}</p>
        </div>

        <div className="flex flex-row md:flex-col gap-6 md:gap-2 text-left md:text-right w-full md:w-auto mt-4 md:mt-0 pt-4 md:pt-0 border-t border-neutral-800 md:border-0">
          <div>
            <p className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Amount</p>
            <p className="text-lg font-medium text-white">{grant.fundingAmount}</p>
          </div>
          <div>
            <p className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1">Deadline</p>
            <p className="text-sm font-medium text-neutral-300">{grant.deadline}</p>
          </div>
        </div>
      </div>
      
      {isExpanded && (
        <div className="border-t border-neutral-800 bg-neutral-950 p-6">
          <MatchReasoningCard grant={grant} />
        </div>
      )}
    </div>
  );
}
