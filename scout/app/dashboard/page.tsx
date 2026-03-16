import { getNonprofitProfile, getGrantOpportunities } from '@/lib/api';
import ProfileCard from '@/components/ProfileCard';

export default async function Dashboard() {
  const profilePromise = getNonprofitProfile();
  const grantsPromise = getGrantOpportunities();
  
  const [profile, grants] = await Promise.all([profilePromise, grantsPromise]);

  const avgMatchScore = Math.round(
    grants.reduce((acc, curr) => acc + curr.matchScore, 0) / grants.length
  );
  
  return (
    <main className="max-w-7xl mx-auto px-6 py-10 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Mission Dashboard</h1>
        <p className="text-neutral-400">Welcome back. Scout is actively monitoring funding opportunities based on your profile.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main large display column */}
        <div className="lg:col-span-2 space-y-8">
          <ProfileCard profile={profile} />
          
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-6">Recent Activity Highlights</h2>
            <div className="space-y-4">
              <div className="flex items-start gap-4 p-4 rounded-xl bg-neutral-950/50 border border-neutral-800/50">
                <div className="w-2 h-2 rounded-full bg-emerald-500 mt-2"></div>
                <div>
                  <p className="font-medium text-white">New high-match grant discovered</p>
                  <p className="text-sm text-neutral-400 mt-1">Monterey Bay Restoration Grant matches your focus areas at 98%.</p>
                </div>
              </div>
              <div className="flex items-start gap-4 p-4 rounded-xl bg-neutral-950/50 border border-neutral-800/50">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-2"></div>
                <div>
                  <p className="font-medium text-white">Application deadline approaching</p>
                  <p className="text-sm text-neutral-400 mt-1">Coastal Resilience Innovation Fund draft is due next week.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right side stats column */}
        <div className="space-y-4">
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col justify-center text-center">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wide">Opportunities Found</h3>
            <p className="text-4xl font-bold text-white mt-4">{grants.length}</p>
          </div>
          
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col justify-center text-center">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wide">Avg Match Score</h3>
            <p className="text-4xl font-bold text-white mt-4 text-emerald-400">{avgMatchScore}%</p>
          </div>

          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col justify-center text-center">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wide">Upcoming Deadlines</h3>
            <p className="text-4xl font-bold text-amber-400 mt-4">2</p>
          </div>
        </div>
      </div>
    </main>
  );
}
