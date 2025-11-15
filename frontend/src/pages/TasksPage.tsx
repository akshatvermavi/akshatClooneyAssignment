import React, { useEffect, useState } from 'react';
import type { Task, TaskCreate } from '../api';
import { fetchProjectTasks, createTask } from '../api';

interface Props {
  projectId: number | null;
}

export function TasksPage({ projectId }: Props) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [newTaskName, setNewTaskName] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!projectId) return;
    fetchProjectTasks(projectId)
      .then(setTasks)
      .catch(() => setError('Failed to load tasks'));
  }, [projectId]);

  const canCreate = Boolean(projectId && newTaskName.trim().length > 0 && !isSaving);

  const handleAddTask = async () => {
    if (!projectId || !newTaskName.trim()) return;
    setIsSaving(true);
    try {
      const payload: TaskCreate = {
        name: newTaskName.trim(),
        project_id: projectId,
        status: 'inbox',
        assignee: 'me',
      };
      const created = await createTask(payload);
      setTasks((prev) => [created, ...prev]);
      setNewTaskName('');
      setError(null);
    } catch (e) {
      setError('Failed to create task');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="flex-1 overflow-auto" data-testid="tasks-page">
      <div className="flex h-full">
        <div className="flex-1 px-6 py-4 border-r bg-white">
          <div className="mb-3 flex gap-2 items-center">
            <input
              className="border border-slate-300 rounded px-2 py-1 text-xs flex-1"
              placeholder={projectId ? 'Add a task name…' : 'Select a project first…'}
              value={newTaskName}
              onChange={(e) => setNewTaskName(e.target.value)}
              disabled={!projectId || isSaving}
            />
            <button
              className="px-3 py-1 rounded-full text-xs font-semibold text-white bg-asanaPrimary disabled:opacity-40"
              onClick={handleAddTask}
              disabled={!canCreate}
            >
              Add
            </button>
          </div>
          {error && <div className="text-xs text-red-600 mb-2">{error}</div>}
          <table className="min-w-full text-xs">
            <thead className="bg-slate-50 border-b">
              <tr>
                <th className="text-left px-3 py-2 font-semibold text-slate-500">Task</th>
                <th className="text-left px-3 py-2 font-semibold text-slate-500">Status</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((t) => (
                <tr key={t.id} className="border-b last:border-b-0 hover:bg-slate-50" data-dynamic="true">
                  <td className="px-3 py-1.5 flex items-center gap-2">
                    <span className="h-3 w-3 border rounded-full" />
                    {t.name}
                  </td>
                  <td className="px-3 py-1.5 text-slate-400">{t.status}</td>
                </tr>
              ))}
              {tasks.length === 0 && (
                <tr>
                  <td className="px-3 py-4 text-xs text-slate-400" colSpan={2}>
                    {projectId ? error ?? 'No tasks yet.' : 'Select a project from Projects to view tasks.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <aside className="w-80 bg-slate-50 p-4 text-xs hidden md:block">
          <div className="font-semibold mb-2">Task details</div>
          <p className="text-slate-400">
            Select a task on the left to view details. This approximates Asana's right-hand details pane.
          </p>
        </aside>
      </div>
    </div>
  );
}
