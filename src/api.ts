import type { NovaTarefa, Projeto, Status, Tarefa } from './tipos'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3000'

// Atraso opcional (em ms) para ver o indicador de carregamento com a API local,
// que responde rápido demais. Ex.: VITE_ATRASO_API=1500 npm run dev
const ATRASO_MS = Number(import.meta.env.VITE_ATRASO_API ?? 0)

export class ErroNaoEncontrado extends Error {}

// A API não respondeu (json-server parado, endereço errado, sem rede).
export class ErroSemConexao extends Error {
  constructor() {
    super(`Sem conexão com a API em ${BASE_URL}`)
  }
}

// A API respondeu, mas com um status de erro (ex.: 500).
export class ErroApi extends Error {
  readonly status: number

  constructor(status: number) {
    super(`Falha na API (${status})`)
    this.status = status
  }
}

// O fetch só rejeita quando não há resposta nenhuma; erros HTTP chegam como resposta.
async function requisitar(caminho: string, opcoes?: RequestInit): Promise<Response> {
  let resposta: Response
  try {
    resposta = await fetch(`${BASE_URL}${caminho}`, opcoes)
  } catch {
    throw new ErroSemConexao()
  }
  if (resposta.status === 404) throw new ErroNaoEncontrado(caminho)
  if (!resposta.ok) throw new ErroApi(resposta.status)
  return resposta
}

async function buscar<T>(caminho: string, opcoes?: RequestInit): Promise<T> {
  if (ATRASO_MS > 0) await new Promise((resolver) => setTimeout(resolver, ATRASO_MS))
  const resposta = await requisitar(caminho, opcoes)
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
export async function excluirTarefa(id: string): Promise<void> {
  await requisitar(`/tarefas/${encodeURIComponent(id)}`, { method: 'DELETE' })
}