<script setup lang="ts">
import { listarProjetos, listarTarefas } from '../api'
import AlternarVisao from '../components/AlternarVisao.vue'
import CarregaDados from '../components/CarregaDados.vue'
import FiltrosTarefas from '../components/FiltrosTarefas.vue'
import SeletorStatus from '../components/SeletorStatus.vue'
import { filtrarTarefas, filtros } from '../filtros'
import { substituirTarefa } from '../tarefas'
import { formatarData, rotuloPrioridade, rotuloStatus } from '../rotulos'
import type { Projeto, Status, Tarefa } from '../tipos'

const colunas = Object.entries(rotuloStatus) as [Status, string][]

const carregar = async () => {
  const [tarefas, projetos] = await Promise.all([listarTarefas(), listarProjetos()])
  return { tarefas, projetos }
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

  <AlternarVisao />

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
        <span class="task-total">{{ filtrarTarefas(tarefas).length }} tarefas</span>
      </div>
      <div>
        <FiltrosTarefas />
        <label class="search-box">
          <span>⌕</span>
          <input v-model="filtros.busca" type="search" placeholder="Buscar por título..." aria-label="Buscar tarefas por título" />
        </label>
      </div>
    </div>

    <div class="kanban-board">
      <section v-for="[status, nome] in colunas" :key="status" class="kanban-column">
        <header class="column-header">
          <span class="column-dot" :class="status"></span>
          <h3>{{ nome }}</h3>
          <span class="column-count">{{ contar(filtrarTarefas(tarefas), status) }}</span>
        </header>

        <div class="column-cards">
          <article
            v-for="tarefa in filtrarTarefas(tarefas).filter((t) => t.status === status)"
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
            <SeletorStatus :tarefa="tarefa" @atualizada="substituirTarefa(tarefas, $event)" />
            <div class="task-card-footer">
              <span class="assignee-avatar">{{ tarefa.responsavel.slice(0, 1).toUpperCase() }}</span>
              <span class="assignee-name">{{ tarefa.responsavel }}</span>
              <span class="task-deadline">◷ {{ formatarData(tarefa.prazo) }}</span>
            </div>
          </article>

          <div v-if="contar(filtrarTarefas(tarefas), status) === 0" class="empty-column">
            <span>◇</span>
            <p>Nenhuma tarefa</p>
          </div>
        </div>
      </section>
    </div>
  </CarregaDados>
</template>