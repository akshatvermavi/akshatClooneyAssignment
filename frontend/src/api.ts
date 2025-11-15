import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${baseURL}/api`,
});

export interface HomeProjectSummary {
  id: number;
  name: string;
  color?: string | null;
  icon?: string | null;
}

export interface HomeTaskSummary {
  id: number;
  name: string;
  project_id: number;
  project_name: string;
  status: string;
}

export interface HomeResponse {
  my_tasks: HomeTaskSummary[];
  recent_projects: HomeProjectSummary[];
}

export interface Project {
  id: number;
  name: string;
  workspace_id: number;
  color?: string | null;
}

export interface ProjectCreate {
  name: string;
  workspace_id: number;
  color?: string | null;
  icon?: string | null;
}

export interface Task {
  id: number;
  name: string;
  description?: string | null;
  status: string;
  assignee?: string | null;
  project_id: number;
}

export interface TaskCreate {
  name: string;
  project_id: number;
  description?: string | null;
  status?: string;
  assignee?: string | null;
}

export async function fetchHome(): Promise<HomeResponse> {
  const res = await api.get<HomeResponse>('/home');
  return res.data;
}

export async function fetchProjects(): Promise<Project[]> {
  const res = await api.get<Project[]>('/projects');
  return res.data;
}

export async function fetchProjectTasks(projectId: number): Promise<Task[]> {
  const res = await api.get<Task[]>(`/projects/${projectId}/tasks`);
  return res.data;
}

export async function createProject(payload: ProjectCreate): Promise<Project> {
  const res = await api.post<Project>('/projects', payload);
  return res.data;
}

export async function createTask(payload: TaskCreate): Promise<Task> {
  const res = await api.post<Task>('/tasks', payload);
  return res.data;
}
