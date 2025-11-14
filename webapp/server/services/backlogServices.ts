import api from '../api';
import type { BacklogItem } from '@/composables/useBacklog';

export interface BacklogItemData {
  id_projeto: number;
  titulo: string;
  objetivo: string;
  beneficios: string;
  prioridade: 'Alta' | 'Média' | 'Baixa';
}

export const criarBacklogItem = async (userStory: BacklogItemData): Promise<BacklogItem> => {
  try {
    // API será tipo /projetos/{id_projeto}/backlog/ ?
    const res = await api.post(`/projetos/${userStory.id_projeto}/backlog/`, userStory);
    return res.data;

  } catch (error: any) {
    const msg = error.response?.data?.erro || 'Erro ao criar item do backlog';
    throw new Error(msg);
  }
}

export const listarBacklogItems = async (id_projeto: number): Promise<BacklogItem[]> => {
  try {
    const res = await api.get(`/projetos/${id_projeto}/backlog/`);
    return res.data;

  } catch (error: any) {
    const msg = error.response?.data?.erro || 'Erro ao listar itens do backlog';
    throw new Error(msg);
  }
}

export const atualizarBacklogItem = async (id_projeto: number, item_id: number, itemData: Partial<BacklogItemData>): Promise<BacklogItem> => {
    try {
        const res = await api.put(`/projetos/${id_projeto}/backlog/${item_id}/`, itemData);
        return res.data;
        
    } catch (error: any) {
        const msg = error.response?.data?.erro || 'Erro ao atualizar item do backlog';
        throw new Error(msg);
    }
}

export const excluirBacklogItem = async (id_projeto: number, item_id: number): Promise<void> => {
    try {
        await api.delete(`/projetos/${id_projeto}/backlog/${item_id}/`);

    } catch (error: any) {
        const msg = error.response?.data?.erro || 'Erro ao excluir item do backlog';
        throw new Error(msg);
    }
}