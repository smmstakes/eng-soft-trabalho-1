interface Project {
  id: number;
  projectId: string;
  name: string;
  description: string;
  sprintStatus: string;
}

export const useProject = 
  () => useState<Project | null>('project', () => null);

export const useProjectsList = 
  () => useState<Project[]>('projects-list', () => []);

export const useProjectPassword =
  () => useState<string>('project-password', () => '');


export type Role = 'Product Owner' | 'Scrum Master' | 'Desenvolvedor';

export interface Member {
  id: number;
  name: string;
  email: string;
  avatarUrl: string;
  role: Role;
  isCurrentUser?: boolean; // Para identificar o usuário logado
}

export const useProjectMembers = 
  () => useState<Member[]>('project-members', () => []);
