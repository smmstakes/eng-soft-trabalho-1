export interface Project {
  id: number;
  projectId: string;
  name: string;
  description: string;
  sprintStatus: string;
}

export const useProject = () => useState<Project | null>('project', () => null);

export const useProjectsList = () => useState<Project[]>('projects-list', () => []);

export const useProjectPassword = () => useState<string>('project-password', () => '');

// Novo state para sprints do projeto
export interface Sprint {
  id: number
  titulo: string
  descricao?: string
  revisao?: string
  inicio?: string
  termino?: string
  status: 'Em andamento' | 'Concluida' | 'Finalizada'
  metas?: { id: number; titulo: string }[]
}

export const useProjectSprints = () => useState<Sprint[]>('project-sprints', () => [])

export type Role = 'Product Owner' | 'Scrum Master' | 'Desenvolvedor';

export interface Member {
  id: number;
  name: string;
  email: string;
  avatarUrl: string;
  role: Role;
  isCurrentUser?: boolean; // Para identificar o usuário logado
}

export const useProjectMembers = () => useState<Member[]>('project-members', () => []);
