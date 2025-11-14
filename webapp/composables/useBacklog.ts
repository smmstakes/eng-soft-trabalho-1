import { useState } from '#app';

export interface BacklogItem {
  id: number;
  id_projeto: number;
  titulo: string;
  objetivo: string;
  beneficios: string;
  prioridade: 'Alta' | 'Média' | 'Baixa';
}

export const useBacklog = () => useState<BacklogItem[]>('backlog', () => []);
