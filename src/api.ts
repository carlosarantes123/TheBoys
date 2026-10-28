import type { NovaTarefa, Projeto, Status, Tarefa } from './tipos'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3000'

export class ErroNaoEncontrado extends Error {}

async function buscar<T>(caminho: string, opcoes?: RequestInit): Promise<T> {
  const resposta = await fetch(`${BASE_URL}${caminho}`, opcoes)
  if (resposta.status === 404) throw new ErroNaoEncontrado(caminho)
  if (!resposta.ok) throw new Error(`Falha na API (${resposta.status})`)
  return resposta.json() as Promise<T>
}

function enviarJson<T>(caminho: string, metodo: 'POST' | 'PUT' | 'PATCH', dados: unknown): Promise<T> {
  return buscar<T>(caminho, {
    method: metodo,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  })
}

export type ProjetoComTarefas = Projeto & { tarefas: Tarefa[] }
export type NovoProjeto = Omit<Projeto, 'id'>

export const listarTarefas = () => buscar<Tarefa[]>('/tarefas')
export const buscarTarefa = (id: string) => buscar<Tarefa>(`/tarefas/${encodeURIComponent(id)}`)
export const criarTarefa = (dados: NovaTarefa) => enviarJson<Tarefa>('/tarefas', 'POST', dados)
export const atualizarTarefa = (id: string, dados: NovaTarefa) =>
  enviarJson<Tarefa>(`/tarefas/${encodeURIComponent(id)}`, 'PUT', dados)
// Atualiza só o status (PATCH), sem reenviar a tarefa inteira.
export const atualizarStatusTarefa = (id: string, status: Status) =>
  enviarJson<Tarefa>(`/tarefas/${encodeURIComponent(id)}`, 'PATCH', { status })
export const listarProjetos = () => buscar<Projeto[]>('/projetos')
export const buscarProjeto = (id: string) =>
  buscar<Projeto>(`/projetos/${encodeURIComponent(id)}`)
export const criarProjeto = (dados: NovoProjeto) =>
  enviarJson<Projeto>('/projetos', 'POST', dados)
export const atualizarProjeto = (id: string, dados: NovoProjeto) =>
  enviarJson<Projeto>(`/projetos/${encodeURIComponent(id)}`, 'PUT', dados)
// O filtro ?projetoId= não funciona no json-server para ids numéricos; usa-se _embed.
export const buscarProjetoComTarefas = (id: string) =>
  buscar<ProjetoComTarefas>(`/projetos/${encodeURIComponent(id)}?_embed=tarefas`)