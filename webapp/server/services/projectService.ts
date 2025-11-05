import api from '../api'

export interface ProjetoData {
    titulo_projeto: string
    descricao: string
    cpf: string
}

export interface ProjetoResponse {
    id: number
    titulo: string
    descricao: string
    cpf_dono: string
    sprintStatus?: string
}

export const criarProjeto = async (projeto: ProjetoData): Promise<ProjetoResponse> => {
    try {
        const res = await api.post('/projetos/', projeto)
        return res.data
    } catch (error: any) {
        const msg = error.response.data.erro
        throw new Error(msg)
    }
}

export const listarProjetos = async (): Promise<ProjetoResponse[]> => {
    const res = await api.get('/projetos/')
    return res.data
}

export const buscarProjetoPorId = async (id: number): Promise<ProjetoResponse> => {
    const res = await api.get(`/projetos/${id}`)
    return res.data
}
