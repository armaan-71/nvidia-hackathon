import { getGrantOpportunities } from '@/lib/api';
import GrantCard from '@/components/GrantCard';

export default async function GrantsPage() {
  const grants = await getGrantOpportunities();

  return (
    <main className="max-w-5xl mx-auto px-6 py-10 space-y-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Grant Opportunities</h1>
          <p className="text-neutral-400">Review the curated list of grants matched to your profile.</p>
        </div>
        
        {/* Simple mock search/filter bar visuals */}
        <div className="flex gap-2 w-full md:w-auto">
          <input 
            type="text" 
            placeholder="Search grants..." 
            className="bg-neutral-900 border border-neutral-800 text-white text-sm rounded-lg px-4 py-2 w-full md:w-64 focus:outline-none focus:border-neutral-600"
            disabled
          />
          <button className="bg-neutral-800 border border-neutral-700 text-white text-sm font-medium rounded-lg px-4 py-2 hover:bg-neutral-700 transition">
            Filter
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {grants.length === 0 ? (
          <div className="bg-neutral-900 border border-neutral-800 border-dashed rounded-2xl p-12 text-center">
            <h3 className="text-xl font-medium text-white mb-2">No grants found</h3>
            <p className="text-neutral-500">Try adjusting your filters or expanding your focus areas.</p>
          </div>
        ) : (
          grants.map(grant => (
            <GrantCard key={grant.id} grant={grant} />
          ))
        )}
      </div>
    </main>
  );
}
