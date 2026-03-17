import { getNonprofitProfile, getDashboardData } from '@/lib/api';
import ProfileCard from '@/components/ProfileCard';

export default async function Dashboard() {
  const profilePromise = getNonprofitProfile();
  const dashDataPromise = getDashboardData();
  
  const [profile, dashData] = await Promise.all([profilePromise, dashDataPromise]);
  const { stats, recent_activity: activities } = dashData;
  
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
              {activities.length === 0 ? (
                <p className="text-sm text-neutral-500 italic py-4">No recent activity. Start a chat with Scout to find grants.</p>
              ) : (
                activities.map((act: any, idx: number) => (
                  <div key={idx} className="flex items-start gap-4 p-4 rounded-xl bg-neutral-950/50 border border-neutral-800/50">
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      act.agent.includes('discovery') ? 'bg-emerald-500' : 
                      act.agent.includes('analyzer') ? 'bg-violet-500' : 'bg-blue-500'
                    }`}></div>
                    <div>
                      <p className="font-medium text-white capitalize">{act.agent.replace('_', ' ')}: Active</p>
                      <p className="text-sm text-neutral-400 mt-1 line-clamp-2">{act.action}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Right side stats column */}
        <div className="space-y-4">
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col justify-center text-center">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wide">Opportunities Found</h3>
            <p className="text-4xl font-bold text-white mt-4">{stats.opportunities_found}</p>
          </div>
          
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col justify-center text-center">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wide">Avg Match Score</h3>
            <p className="text-4xl font-bold text-white mt-4 text-emerald-400">{stats.avg_match_score}%</p>
          </div>

          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col justify-center text-center">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wide">Upcoming Deadlines</h3>
            <p className="text-4xl font-bold text-amber-400 mt-4">{stats.upcoming_deadlines}</p>
          </div>
        </div>
      </div>
    </main>
  );
}
