import React, { useState } from 'react';
import { HomePage } from './pages/HomePage';
import { ProjectsPage } from './pages/ProjectsPage';
import { TasksPage } from './pages/TasksPage';

export type PageKey = 'home' | 'projects' | 'tasks';

export default function App() {
  const [page, setPage] = useState<PageKey>('home');
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(1);
  return (
    <div className="flex h-screen bg-asanaBackground text-slate-900">
      <aside
        className="w-64 bg-asanaSidebar text-white flex flex-col"
        data-testid="sidebar"
      >
        <div className="px-4 py-3 text-lg font-semibold tracking-tight border-b border-slate-800">
          Clooney
        </div>
        <nav className="flex-1 px-2 py-4 space-y-1 text-sm">
          <button
            className={`w-full text-left px-3 py-2 rounded-md hover:bg-slate-800 ${
              page === 'home' ? 'bg-slate-800' : ''
            }`}
            onClick={() => setPage('home')}
            data-testid="nav-home"
          >
            Home
          </button>
          <button
            className={`w-full text-left px-3 py-2 rounded-md hover:bg-slate-800 ${
              page === 'projects' ? 'bg-slate-800' : ''
            }`}
            onClick={() => setPage('projects')}
            data-testid="nav-projects"
          >
            Projects
          </button>
          <button
            className={`w-full text-left px-3 py-2 rounded-md hover:bg-slate-800 ${
              page === 'tasks' ? 'bg-slate-800' : ''
            }`}
            onClick={() => setPage('tasks')}
            data-testid="nav-tasks"
          >
            My tasks
          </button>
        </nav>
      </aside>

      <main className="flex-1 flex flex-col">
        <header
          className="h-12 flex items-center justify-between px-4 border-b bg-white"
          data-testid="topbar"
        >
          <div className="font-semibold text-sm">{page === 'home' ? 'Home' : page === 'projects' ? 'Projects' : 'My tasks'}</div>
          <button
            className="px-3 py-1 rounded-full text-xs font-semibold text-white bg-asanaPrimary hover:opacity-90"
            data-testid="primary-cta"
            onClick={() => setPage('tasks')}
          >
            Add task
          </button>
        </header>

        {page === 'home' && <HomePage />}
        {page === 'projects' && (
          <ProjectsPage
            onSelectProject={(id) => {
              setSelectedProjectId(id);
              setPage('tasks');
            }}
          />
        )}
        {page === 'tasks' && <TasksPage projectId={selectedProjectId} />}
      </main>
    </div>
  );
}
