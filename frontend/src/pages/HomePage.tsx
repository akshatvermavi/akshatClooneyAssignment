import React, { useEffect, useState } from 'react';
import type { HomeResponse } from '../api';
import { fetchHome } from '../api';

export function HomePage() {
  const [data, setData] = useState<HomeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHome()
      .then(setData)
      .catch(() => setError('Failed to load home data'));
  }, []);

  return (
    <div className="flex-1 overflow-auto" data-testid="home-page">
      <div className="px-6 py-4 space-y-6">
        <section>
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">
            My tasks
          </h2>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 min-h-[120px]">
            {error && <div className="text-xs text-red-600">{error}</div>}
            {!data && !error && <div className="text-xs text-slate-400">Loading…</div>}
            {data && (
              <ul className="divide-y divide-slate-100" data-dynamic="true">
                {data.my_tasks.map((t) => (
                  <li key={t.id} className="py-1.5 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className="h-3 w-3 border rounded-full" />
                      <span>{t.name}</span>
                    </div>
                    <span className="text-slate-400">{t.project_name}</span>
                  </li>
                ))}
                {data.my_tasks.length === 0 && (
                  <li className="text-xs text-slate-400">No tasks assigned to you yet.</li>
                )}
              </ul>
            )}
          </div>
        </section>

        <section>
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">
            Recent projects
          </h2>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 grid grid-cols-2 gap-3">
            {data && (
              <>
                {data.recent_projects.map((p) => (
                  <article
                    key={p.id}
                    className="border border-slate-200 rounded-md px-3 py-2 text-xs flex items-center justify-between hover:border-asanaPrimary/60"
                    data-dynamic="true"
                  >
                    <span>{p.name}</span>
                    <span className="inline-flex h-5 w-5 rounded-full bg-asanaPrimary/80" />
                  </article>
                ))}
                {data.recent_projects.length === 0 && (
                  <div className="text-xs text-slate-400">No recent projects.</div>
                )}
              </>
            )}
            {!data && !error && <div className="text-xs text-slate-400">Loading…</div>}
          </div>
        </section>
      </div>
    </div>
  );
}
