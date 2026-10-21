<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { NovaTarefa, Projeto, Status, Tarefa } from './tipos'

const API_URL = 'http://localhost:3000'

const statusList: { valor: Status; nome: string }[] = [
  { valor: 'a-fazer', nome: 'A fazer' },
  { valor: 'em-andamento', nome: 'Em andamento' },
  { valor: 'em-revisao', nome: 'Em revisão' },
  { valor: 'concluida', nome: 'Concluídas' },
]

const tarefas = ref<Tarefa[]>([])
const projetos = ref<Projeto[]>([])
const tela = ref<'quadro' | 'nova-tarefa'>('quadro')
const carregando = ref(false)
const salvando = ref(false)
const erro = ref('')
const mensagem = ref('')
const busca = ref('')

const formulario = reactive<NovaTarefa>({
  projetoId: '',
  titulo: '',
  descricao: '',
  status: 'a-fazer',
  prioridade: 'media',
  responsavel: '',
  prazo: '',
})

const erros = reactive({
  titulo: '',
  projetoId: '',
  responsavel: '',
  prazo: '',
})

function limparErros() {
  Object.assign(erros, { titulo: '', projetoId: '', responsavel: '', prazo: '' })
}

function validar() {
  erros.titulo = formulario.titulo.trim() ? '' : 'Informe o título da tarefa.'
  erros.projetoId = formulario.projetoId ? '' : 'Selecione um projeto.'
  erros.responsavel = formulario.responsavel.trim() ? '' : 'Informe o responsável.'
  erros.prazo = formulario.prazo ? '' : 'Informe o prazo.'

  return !Object.values(erros).some(Boolean)
}

const tarefasFiltradas = computed(() => {
  const termo = busca.value.trim().toLowerCase()

  if (!termo) return tarefas.value

  return tarefas.value.filter((tarefa) =>
    [
      tarefa.titulo,
      tarefa.descricao,
      tarefa.responsavel,
    ].some((campo) => campo.toLowerCase().includes(termo)),
  )
})

function tarefasPorStatus(status: Status) {
  return tarefasFiltradas.value.filter((tarefa) => tarefa.status === status)
}

function nomeProjeto(projetoId: string) {
  return projetos.value.find((projeto) => projeto.id === projetoId)?.nome
    ?? 'Projeto não encontrado'
}

function formatarData(data: string) {
  if (!data) return 'Sem prazo'

  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

async function carregarDados() {
  carregando.value = true
  erro.value = ''

  try {
    const [respostaTarefas, respostaProjetos] = await Promise.all([
      fetch(`${API_URL}/tarefas`),
      fetch(`${API_URL}/projetos`),
    ])

    if (!respostaTarefas.ok || !respostaProjetos.ok) {
      throw new Error('Não foi possível consultar a API.')
    }

    tarefas.value = await respostaTarefas.json() as Tarefa[]
    projetos.value = await respostaProjetos.json() as Projeto[]

    if (!formulario.projetoId && projetos.value.length > 0) {
      formulario.projetoId = projetos.value[0].id
    }
  } catch {
    erro.value =
      'Não foi possível carregar os dados. Confira se o JSON Server está rodando na porta 3000.'
  } finally {
    carregando.value = false
  }
}

function abrirFormulario() {
  mensagem.value = ''
  erro.value = ''

  formulario.titulo = ''
  formulario.descricao = ''
  formulario.responsavel = ''
  formulario.prazo = ''
  formulario.status = 'a-fazer'
  formulario.prioridade = 'media'
  formulario.projetoId = projetos.value[0]?.id ?? ''
  limparErros()

  tela.value = 'nova-tarefa'
}

async function salvarTarefa() {
  erro.value = ''
  mensagem.value = ''

  if (!validar()) return

  salvando.value = true

  const novaTarefa: NovaTarefa = {
    ...formulario,
    titulo: formulario.titulo.trim(),
    descricao: formulario.descricao.trim(),
    responsavel: formulario.responsavel.trim(),
  }

  try {
    const resposta = await fetch(`${API_URL}/tarefas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(novaTarefa),
    })

    if (!resposta.ok) {
      throw new Error('Não foi possível salvar a tarefa.')
    }

    const tarefaSalva = await resposta.json() as Tarefa
    tarefas.value.push(tarefaSalva)

    mensagem.value = 'Tarefa cadastrada com sucesso!'
    tela.value = 'quadro'

    formulario.titulo = ''
    formulario.descricao = ''
    formulario.responsavel = ''
    formulario.prazo = ''
    formulario.status = 'a-fazer'
    formulario.prioridade = 'media'
  } catch {
    erro.value =
      'Não foi possível salvar. Verifique se o JSON Server está funcionando.'
  } finally {
    salvando.value = false
  }
}

onMounted(carregarDados)
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <a class="brand" href="#" @click.prevent="tela = 'quadro'">
        <span class="brand-icon">T</span>
        <span>
          <strong>TheBoys</strong>
          <small>Gerenciador de tarefas</small>
        </span>
      </a>

      <p class="menu-label">ESPAÇO DE TRABALHO</p>

      <button
        class="menu-item"
        :class="{ active: tela === 'quadro' }"
        @click="tela = 'quadro'; mensagem = ''; erro = ''"
      >
        <span class="menu-icon">▦</span>
        Meu quadro
      </button>

      <button
        class="menu-item"
        :class="{ active: tela === 'nova-tarefa' }"
        @click="abrirFormulario"
      >
        <span class="menu-icon">＋</span>
        Nova tarefa
      </button>

      <div class="sidebar-bottom">
        <span class="avatar">TB</span>
        <div>
          <strong>Equipe TheBoys</strong>
          <small>Projeto acadêmico</small>
        </div>
      </div>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <div class="breadcrumb">
          <span>Workspace</span>
          <span class="breadcrumb-separator">/</span>
          <strong>{{ tela === 'quadro' ? 'Meu quadro' : 'Nova tarefa' }}</strong>
        </div>

        <button class="primary-button top-create" @click="abrirFormulario">
          <span>＋</span> Nova tarefa
        </button>
      </header>

      <section class="page-content">
        <template v-if="tela === 'quadro'">
          <div class="page-heading">
            <div>
              <p class="eyebrow">VISÃO GERAL</p>
              <h1>Meu quadro</h1>
              <p class="page-description">
                Organize as atividades e acompanhe o progresso da equipe.
              </p>
            </div>

            <button class="primary-button" @click="abrirFormulario">
              ＋ Criar tarefa
            </button>
          </div>

          <div class="summary-grid">
            <article class="summary-card">
              <span class="summary-icon purple">▦</span>
              <div>
                <span>Total de tarefas</span>
                <strong>{{ tarefas.length }}</strong>
              </div>
            </article>

            <article class="summary-card">
              <span class="summary-icon blue">◷</span>
              <div>
                <span>Em andamento</span>
                <strong>{{ tarefas.filter(t => t.status === 'em-andamento').length }}</strong>
              </div>
            </article>

            <article class="summary-card">
              <span class="summary-icon green">✓</span>
              <div>
                <span>Concluídas</span>
                <strong>{{ tarefas.filter(t => t.status === 'concluida').length }}</strong>
              </div>
            </article>
          </div>

          <div class="board-toolbar">
            <div>
              <h2>Quadro de tarefas</h2>
              <span class="task-total">{{ tarefasFiltradas.length }} tarefas</span>
            </div>

            <label class="search-box">
              <span>⌕</span>
              <input
                v-model="busca"
                type="search"
                placeholder="Buscar tarefa..."
                aria-label="Buscar tarefas"
              />
            </label>
          </div>

          <p v-if="mensagem" class="notice success" role="status">
            {{ mensagem }}
          </p>
          <p v-if="erro" class="notice error" role="alert">{{ erro }}</p>
          <p v-if="carregando" class="loading-message" role="status">
            Carregando tarefas...
          </p>

          <div v-else class="kanban-board">
            <section
              v-for="coluna in statusList"
              :key="coluna.valor"
              class="kanban-column"
            >
              <header class="column-header">
                <span class="column-dot" :class="coluna.valor"></span>
                <h3>{{ coluna.nome }}</h3>
                <span class="column-count">
                  {{ tarefasPorStatus(coluna.valor).length }}
                </span>
              </header>

              <div class="column-cards">
                <article
                  v-for="tarefa in tarefasPorStatus(coluna.valor)"
                  :key="tarefa.id"
                  class="task-card"
                >
                  <div class="task-card-top">
                    <span class="project-name">
                      {{ nomeProjeto(tarefa.projetoId) }}
                    </span>
                    <span class="task-id">#{{ tarefa.id }}</span>
                  </div>

                  <h4>{{ tarefa.titulo }}</h4>

                  <p v-if="tarefa.descricao" class="task-description">
                    {{ tarefa.descricao }}
                  </p>

                  <div class="task-tags">
                    <span class="priority-tag" :class="tarefa.prioridade">
                      {{ tarefa.prioridade }}
                    </span>
                  </div>

                  <div class="task-card-footer">
                    <span class="assignee-avatar">
                      {{ tarefa.responsavel.slice(0, 1).toUpperCase() }}
                    </span>
                    <span class="assignee-name">{{ tarefa.responsavel }}</span>
                    <span class="task-deadline">◷ {{ formatarData(tarefa.prazo) }}</span>
                  </div>
                </article>

                <div
                  v-if="tarefasPorStatus(coluna.valor).length === 0 && !carregando"
                  class="empty-column"
                >
                  <span>◇</span>
                  <p>Nenhuma tarefa</p>
                </div>
              </div>
            </section>
          </div>
        </template>

        <template v-else>
          <div class="form-heading">
            <button class="back-button" @click="tela = 'quadro'; erro = ''">
              ← Voltar ao quadro
            </button>
            <p class="eyebrow">GERENCIAMENTO DE ATIVIDADES</p>
            <h1>Nova tarefa</h1>
            <p class="page-description">
              Preencha as informações abaixo para adicionar uma atividade ao quadro.
            </p>
          </div>

          <p v-if="erro" class="notice error" role="alert">{{ erro }}</p>

          <form class="task-form" novalidate @submit.prevent="salvarTarefa">
            <div class="form-section-title">
              <span class="form-section-icon">✎</span>
              <div>
                <h2>Informações da tarefa</h2>
                <p>Descreva o que precisa ser realizado.</p>
              </div>
            </div>

            <div class="form-field">
              <label for="titulo">Título da tarefa <span>*</span></label>
              <input
                id="titulo"
                v-model="formulario.titulo"
                type="text"
                maxlength="120"
                placeholder="Ex.: Desenvolver a tela de login"
                required
                :aria-invalid="!!erros.titulo"
                aria-describedby="erro-titulo"
              />
              <small v-if="erros.titulo" id="erro-titulo">{{ erros.titulo }}</small>
            </div>

            <div class="form-field">
              <label for="descricao">Descrição</label>
              <textarea
                id="descricao"
                v-model="formulario.descricao"
                rows="4"
                placeholder="Descreva os detalhes e objetivos da tarefa..."
              ></textarea>
            </div>

            <div class="form-field">
              <label for="projeto">Projeto <span>*</span></label>
              <select
                id="projeto"
                v-model="formulario.projetoId"
                required
                :aria-invalid="!!erros.projetoId"
                aria-describedby="erro-projeto"
              >
                <option value="" disabled>Selecione um projeto</option>
                <option
                  v-for="projeto in projetos"
                  :key="projeto.id"
                  :value="projeto.id"
                >
                  {{ projeto.nome }} — {{ projeto.disciplina }}
                </option>
              </select>
              <small v-if="projetos.length === 0">
                Nenhum projeto encontrado. Confira a API.
              </small>
              <small v-if="erros.projetoId" id="erro-projeto">
                {{ erros.projetoId }}
              </small>
            </div>

            <div class="form-row">
              <div class="form-field">
                <label for="responsavel">Responsável <span>*</span></label>
                <input
                  id="responsavel"
                  v-model="formulario.responsavel"
                  type="text"
                  placeholder="Nome do responsável"
                  required
                  :aria-invalid="!!erros.responsavel"
                  aria-describedby="erro-responsavel"
                />
                <small v-if="erros.responsavel" id="erro-responsavel">
                  {{ erros.responsavel }}
                </small>
              </div>

              <div class="form-field">
                <label for="prazo">Prazo <span>*</span></label>
                <input
                  id="prazo"
                  v-model="formulario.prazo"
                  type="date"
                  required
                  :aria-invalid="!!erros.prazo"
                  aria-describedby="erro-prazo"
                />
                <small v-if="erros.prazo" id="erro-prazo">{{ erros.prazo }}</small>
              </div>
            </div>

            <div class="form-row">
              <div class="form-field">
                <label for="prioridade">Prioridade</label>
                <select id="prioridade" v-model="formulario.prioridade">
                  <option value="baixa">Baixa</option>
                  <option value="media">Média</option>
                  <option value="alta">Alta</option>
                </select>
              </div>

              <div class="form-field">
                <label for="status">Status inicial</label>
                <select id="status" v-model="formulario.status">
                  <option
                    v-for="coluna in statusList"
                    :key="coluna.valor"
                    :value="coluna.valor"
                  >
                    {{ coluna.nome }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-actions">
              <button
                type="button"
                class="secondary-button"
                @click="tela = 'quadro'; erro = ''"
              >
                Cancelar
              </button>
              <button type="submit" class="primary-button" :disabled="salvando">
                {{ salvando ? 'Salvando...' : '✓ Salvar tarefa' }}
              </button>
            </div>
          </form>
        </template>
      </section>
    </main>
  </div>
</template>