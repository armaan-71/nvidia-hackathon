import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] text-center px-4">
      <div className="absolute inset-0 -z-10 h-full w-full bg-neutral-950 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      
      <div className="max-w-3xl space-y-8">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-white to-neutral-500">
          Autonomous funding for nonprofits.
        </h1>
        
        <p className="text-lg md:text-xl text-neutral-400 font-medium max-w-2xl mx-auto leading-relaxed">
          Scout analyzes your organization's profile and matching you with billions in grant funding using autonomous AI agents.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
          <Link href="/dashboard" className="px-8 py-4 bg-white text-black font-semibold rounded-full hover:bg-neutral-200 transition-colors shadow-lg shadow-white/10 w-full sm:w-auto">
            View Dashboard
          </Link>
          <Link href="/grants" className="px-8 py-4 bg-neutral-900 border border-neutral-700 font-semibold rounded-full hover:bg-neutral-800 transition-colors w-full sm:w-auto text-white">
            Explore Grants
          </Link>
        </div>
      </div>
    </main>
  );
}
