import { NonprofitProfile } from '@/lib/types';

export default function ProfileCard({ profile }: { profile: NonprofitProfile }) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-sm flex flex-col gap-4 text-white">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">{profile.name}</h2>
        <p className="text-sm font-medium text-neutral-400 mt-1">{profile.location} • {profile.nonprofitStatus}</p>
      </div>
      
      <div className="border-t border-neutral-800 pt-4">
        <h3 className="text-sm font-semibold text-neutral-300 mb-2">Our Mission</h3>
        <p className="text-sm text-neutral-400 leading-relaxed">{profile.mission}</p>
      </div>

      <div className="border-t border-neutral-800 pt-4">
        <h3 className="text-sm font-semibold text-neutral-300 mb-2">Focus Areas</h3>
        <div className="flex flex-wrap gap-2">
          {profile.focusAreas.map((area, i) => (
            <span key={i} className="inline-flex items-center rounded-full bg-neutral-800 px-3 py-1 text-xs font-medium">
              {area}
            </span>
          ))}
        </div>
      </div>

      <div className="border-t border-neutral-800 pt-4 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-neutral-300">Annual Budget</h3>
          <p className="text-lg font-medium tracking-tight mt-1">{profile.annualBudget}</p>
        </div>
        <div className="text-right">
          <h3 className="text-sm font-semibold text-neutral-300">Profile Status</h3>
          <p className="text-sm font-medium text-green-400 mt-1">Foundational Data Verified</p>
        </div>
      </div>
    </div>
  );
}
