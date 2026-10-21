<script setup lang="ts">
import { ref } from 'vue'
import { listarProjetos, listarTarefas } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import { formatarData, rotuloPrioridade, rotuloStatus } from '../rotulos'
import type { Projeto, Status, Tarefa } from '../tipos'

const colunas = Object.entries(rotuloStatus) as [Status, string][]
const busca = ref('')

const carregar = async () => {
  const [tarefas, projetos] = await Promise.all([listarTarefas(), listarProjetos()])
  return { tarefas, projetos }
}

function filtrar(tarefas: Tarefa[]) {
  const termo = busca.value.trim().toLowerCase()
  if (!termo) return tarefas
  return tarefas.filter((tarefa) =>
    [tarefa.titulo, tarefa.descricao, tarefa.responsavel].some((campo) =>
      campo.toLowerCase().includes(termo),
    ),
  )
}

function nomeProjeto(projetos: Projeto[], projetoId: string) {
  return projetos.find((projeto) => projeto.id === projetoId)?.nome ?? 'Projeto não encontrado'
}

function contar(tarefas: Tarefa[], status: Status) {
  return tarefas.filter((tarefa) => tarefa.status === status).length
}
</script>

<template>
  <div class="page-heading">
    <div>
      <p class="eyebrow">VISÃO GERAL</p>
      <h1>Meu quadro</h1>
      <p class="page-description">Organize as atividades e acompanhe o progresso da equipe.</p>
    </div>
    <RouterLink class="primary-button" to="/tarefas/nova">＋ Criar tarefa</RouterLink>
  </div>

  <CarregaDados :carregar="carregar" v-slot="{ dados: { tarefas, projetos } }">
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
          <strong>{{ contar(tarefas, 'em-andamento') }}</strong>
        </div>
      </article>
      <article class="summary-card">
        <span class="summary-icon green">✓</span>
        <div>
          <span>Concluídas</span>
          <strong>{{ contar(tarefas, 'concluida') }}</strong>
        </div>
      </article>
    </div>

    <div class="board-toolbar">
      <div>
        <h2>Quadro de tarefas</h2>
        <span class="task-total">{{ filtrar(tarefas).length }} tarefas</span>
      </div>
      <label class="search-box">
        <span>⌕</span>
        <input v-model="busca" type="search" placeholder="Buscar tarefa..." aria-label="Buscar tarefas" />
      </label>
    </div>

    <div class="kanban-board">
      <section v-for="[status, nome] in colunas" :key="status" class="kanban-column">
        <header class="column-header">
          <span class="column-dot" :class="status"></span>
          <h3>{{ nome }}</h3>
          <span class="column-count">{{ contar(filtrar(tarefas), status) }}</span>
        </header>

        <div class="column-cards">
          <article
            v-for="tarefa in filtrar(tarefas).filter((t) => t.status === status)"
            :key="tarefa.id"
            class="task-card"
          >
            <div class="task-card-top">
              <span class="project-name">{{ nomeProjeto(projetos, tarefa.projetoId) }}</span>
              <span class="task-id">#{{ tarefa.id }}</span>
            </div>
            <h4><RouterLink :to="`/tarefas/${tarefa.id}`">{{ tarefa.titulo }}</RouterLink></h4>
            <p v-if="tarefa.descricao" class="task-description">{{ tarefa.descricao }}</p>
            <div class="task-tags">
              <span class="priority-tag" :class="tarefa.prioridade">
                {{ rotuloPrioridade[tarefa.prioridade] }}
              </span>
            </div>
            <div class="task-card-footer">
              <span class="assignee-avatar">{{ tarefa.responsavel.slice(0, 1).toUpperCase() }}</span>
              <span class="assignee-name">{{ tarefa.responsavel }}</span>
              <span class="task-deadline">◷ {{ formatarData(tarefa.prazo) }}</span>
            </div>
          </article>

          <div v-if="contar(filtrar(tarefas), status) === 0" class="empty-column">
            <span>◇</span>
            <p>Nenhuma tarefa</p>
          </div>
        </div>
      </section>
    </div>
  </CarregaDados>
</template>
