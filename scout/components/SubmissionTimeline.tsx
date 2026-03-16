'use client';

import { TimelineItem } from '@/lib/types';
import { getSubmissionTimeline } from '@/lib/api';
import { useEffect, useState } from 'react';

export default function SubmissionTimeline({ grantId }: { grantId: string }) {
  const [timeline, setTimeline] = useState<TimelineItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    getSubmissionTimeline(grantId).then((data) => {
      if (mounted) {
        setTimeline(data);
        setLoading(false);
      }
    });
    return () => { mounted = false; };
  }, [grantId]);

  if (loading) {
    return <div className="animate-pulse flex space-x-4">
      <div className="flex-1 space-y-4 py-1">
        <div className="h-2 bg-neutral-800 rounded w-3/4"></div>
        <div className="h-2 bg-neutral-800 rounded"></div>
        <div className="h-2 bg-neutral-800 rounded w-5/6"></div>
      </div>
    </div>;
  }

  return (
    <div className="space-y-6">
      {timeline.map((item, id) => (
        <div key={item.id} className="relative flex gap-4">
          <div className="flex flex-col items-center">
            <div className={`w-3 h-3 rounded-full mt-1.5 ${
                item.status === 'complete' ? 'bg-emerald-500 ring-4 ring-emerald-500/20' : 
                item.status === 'in progress' ? 'bg-blue-500 ring-4 ring-blue-500/20' : 
                'bg-neutral-600'
              }`} 
            />
            {id !== timeline.length - 1 && (
              <div className="w-px h-full bg-neutral-800 mt-2 absolute top-4 bottom-[-16px]"></div>
            )}
          </div>
          
          <div className="pb-4">
            <div className="flex items-center gap-3 mb-1">
              <h5 className="font-semibold text-white">{item.title}</h5>
              <span className="text-xs font-medium text-neutral-500">By {item.dueDate}</span>
            </div>
            <p className="text-sm text-neutral-400">{item.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
