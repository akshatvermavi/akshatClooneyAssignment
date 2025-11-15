import React, { useEffect, useState } from 'react';
import type { Project, ProjectCreate } from '../api';
import { fetchProjects, createProject } from '../api';

interface Props {
  onSelectProject: (id: number) => void;
}

export function ProjectsPage({ onSelectProject }: Props) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [newProjectName, setNewProjectName] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch(() => setError('Failed to load projects'));
  }, []);

  const canCreate = newProjectName.trim().length > 0 && !isSaving;

  const handleAddProject = async () => {
    if (!canCreate) return;
    setIsSaving(true);
    try {
      const payload: ProjectCreate = {
        name: newProjectName.trim(),
        workspace_id: 1,
        color: '#3a258e',
      };
      const created = await createProject(payload);
      setProjects((prev) => [created, ...prev]);
      setNewProjectName('');
      setError(null);
    } catch {
      setError('Failed to create project');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="flex-1 overflow-auto" data-testid="projects-page">
      <div className="px-6 py-4">
        <div className="mb-3 flex gap-2 items-center">
          <input
            className="border border-slate-300 rounded px-2 py-1 text-xs flex-1"
            placeholder="New project name…"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            disabled={isSaving}
          />
          <button
            className="px-3 py-1 rounded-full text-xs font-semibold text-white bg-asanaPrimary disabled:opacity-40"
            onClick={handleAddProject}
            disabled={!canCreate}
          >
            Add project
          </button>
        </div>
        {error && <div className="text-xs text-red-600 mb-2">{error}</div>}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200">
          <table className="min-w-full text-xs">
            <thead className="bg-slate-50 border-b">
              <tr>
                <th className="text-left px-4 py-2 font-semibold text-slate-500">Name</th>
                <th className="text-left px-4 py-2 font-semibold text-slate-500">Workspace</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p) => (
                <tr
                  key={p.id}
                  className="border-b last:border-b-0 hover:bg-slate-50 cursor-pointer"
                  onClick={() => onSelectProject(p.id)}
                  data-dynamic="true"
                >
                  <td className="px-4 py-1.5 flex items-center gap-2">
                    <span className="inline-flex h-4 w-4 rounded-sm bg-asanaPrimary/70" />
                    {p.name}
                  </td>
                  <td className="px-4 py-1.5 text-slate-400">Workspace {p.workspace_id}</td>
                </tr>
              ))}
              {projects.length === 0 && (
                <tr>
                  <td className="px-4 py-4 text-slate-400 text-xs" colSpan={2}>
                    {error ?? 'No projects yet.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
