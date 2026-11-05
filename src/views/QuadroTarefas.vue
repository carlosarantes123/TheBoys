<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'
import { atualizarStatusTarefa, excluirTarefa, listarProjetos, listarTarefas } from '../api'
import { useArraste } from '../arraste'
import AlternarVisao from '../components/AlternarVisao.vue'
import CarregaDados from '../components/CarregaDados.vue'
import FiltrosTarefas from '../components/FiltrosTarefas.vue'
import Icone from '../components/Icone.vue'
import MarcaPrioridade from '../components/MarcaPrioridade.vue'
import SeletorStatus from '../components/SeletorStatus.vue'
import { filtrarTarefas, filtros } from '../filtros'
import { formatarData, rotuloStatus } from '../rotulos'
import { removerTarefa, substituirTarefa } from '../tarefas'
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

const erroExclusao = ref('')

// Os desenhos do arraste são pesados: só são baixados quando o quadro abre.
const PalcoArraste = defineAsyncComponent(() => import('../components/arraste/PalcoArraste.vue'))

// Arrastar o cartão para outra coluna (desafio opcional). O seletor de status
// no cartão continua sendo a forma sem arraste de fazer a mesma coisa.
const { estado: arraste, clone, iniciar: iniciarArraste } = useArraste()
const erroMovimento = ref('')
const anuncio = ref('')

async function moverTarefa(tarefas: Tarefa[], id: string, status: Status) {
  const tarefa = tarefas.find((t) => t.id === id)
  erroMovimento.value = ''
  try {
    const salva = await atualizarStatusTarefa(id, status)
    substituirTarefa(tarefas, salva)
    anuncio.value = `Tarefa “${salva.titulo}” movida para ${rotuloStatus[status]}.`
    return true
  } catch {
    erroMovimento.value = `Não foi possível mover “${tarefa?.titulo ?? 'a tarefa'}” para ${rotuloStatus[status]}. Ela voltou para a coluna de antes; tente novamente.`
    return false
  }
}

async function excluir(tarefas: Tarefa[], tarefa: Tarefa) {
  if (!window.confirm(`Excluir a tarefa “${tarefa.titulo}”? Esta ação não pode ser desfeita.`)) return

  erroExclusao.value = ''
  try {
    await excluirTarefa(tarefa.id)
    removerTarefa(tarefas, tarefa.id)
  } catch {
    erroExclusao.value = `Não foi possível excluir “${tarefa.titulo}”. A tarefa continua no quadro; tente novamente.`
  }
}
</script>

<template>
  <div class="page-heading">
    <div>
      <h1>Quadro</h1>
      <p class="page-description">Acompanhe cada tarefa da criação até a entrega. Arraste um cartão para outra etapa ou use o seletor de status no próprio cartão.</p>
    </div>
  </div>

  <AlternarVisao />

  <CarregaDados :carregar="carregar" mensagem="Carregando o quadro…" formato="quadro" v-slot="{ dados: { tarefas, projetos } }">
    <div class="summary-grid">
      <article class="summary-card">
        <span class="summary-icon purple"><Icone nome="quadro" :tamanho="24" /></span>
        <div>
          <span>Total de tarefas</span>
          <strong>{{ tarefas.length }}</strong>
        </div>
      </article>
      <article class="summary-card">
        <span class="summary-icon blue"><Icone nome="relogio" :tamanho="24" /></span>
        <div>
          <span>Em andamento</span>
          <strong>{{ contar(tarefas, 'em-andamento') }}</strong>
        </div>
      </article>
      <article class="summary-card">
        <span class="summary-icon green"><Icone nome="check" :tamanho="24" /></span>
        <div>
          <span>Concluídas</span>
          <strong>{{ contar(tarefas, 'concluida') }}</strong>
        </div>
      </article>
    </div>

    <div class="board-toolbar">
      <div>
        <h2>Tarefas por etapa</h2>
        <span class="task-total">{{ filtrarTarefas(tarefas).length }} tarefas</span>
      </div>
      <div>
        <FiltrosTarefas />
        <label class="search-box">
          <Icone nome="busca" :tamanho="18" />
          <input v-model="filtros.busca" type="search" placeholder="Buscar por título" aria-label="Buscar tarefas por título" />
        </label>
      </div>
    </div>

    <p v-if="erroExclusao" class="notice error" role="alert">{{ erroExclusao }}</p>
    <p v-if="erroMovimento" class="notice error" role="alert">{{ erroMovimento }}</p>

    <div class="kanban-board" @pointerdown="iniciarArraste($event, (id, status) => moverTarefa(tarefas, id, status))">
      <section
        v-for="([status, nome], indice) in colunas"
        :key="status"
        class="kanban-column"
        :class="`coluna-${status}`"
        :data-status="status"
      >
        <header class="column-header">
          <span class="etapa" aria-hidden="true">{{ indice + 1 }}</span>
          <h3>{{ nome }}</h3>
          <span class="column-count">{{ contar(filtrarTarefas(tarefas), status) }}</span>
        </header>

        <div class="column-cards">
          <article
            v-for="tarefa in filtrarTarefas(tarefas).filter((t) => t.status === status)"
            :key="tarefa.id"
            class="task-card"
            :data-tarefa-id="tarefa.id"
            :data-titulo="tarefa.titulo"
          >
            <div class="task-card-top">
              <span class="alca-arraste" aria-hidden="true"><Icone nome="alca" :tamanho="18" /></span>
              <span class="project-name">{{ nomeProjeto(projetos, tarefa.projetoId) }}</span>
              <span class="task-id">#{{ tarefa.id }}</span>
            </div>

            <h4><RouterLink :to="`/tarefas/${tarefa.id}`">{{ tarefa.titulo }}</RouterLink></h4>
            <p v-if="tarefa.descricao" class="task-description">{{ tarefa.descricao }}</p>

            <div class="task-tags">
              <MarcaPrioridade :prioridade="tarefa.prioridade" />
            </div>

            <SeletorStatus :tarefa="tarefa" @atualizada="substituirTarefa(tarefas, $event)" />

            <RouterLink
              class="secondary-button botao-editar"
              :to="`/tarefas/${tarefa.id}/editar`"
              :aria-label="`Editar tarefa ${tarefa.titulo}`"
            >
              <Icone nome="lapis" :tamanho="15" />
              Editar tarefa
            </RouterLink>

            <button
              type="button"
              class="secondary-button botao-excluir"
              :aria-label="`Excluir tarefa ${tarefa.titulo}`"
              @click="excluir(tarefas, tarefa)"
            >
              <Icone nome="lixeira" :tamanho="15" />
              Excluir tarefa
            </button>

            <div class="task-card-footer">
              <span class="assignee-name"><span class="sr-only">Responsável: </span>{{ tarefa.responsavel }}</span>
              <span class="task-deadline">Prazo {{ formatarData(tarefa.prazo) }}</span>
            </div>
          </article>

          <div v-if="contar(filtrarTarefas(tarefas), status) === 0" class="empty-column">
            <p>Nenhuma tarefa nesta etapa.</p>
          </div>
        </div>
      </section>
    </div>
  </CarregaDados>

  <!-- anúncio para leitores de tela quando um cartão muda de coluna -->
  <p class="sr-only" role="status" aria-live="polite">{{ anuncio }}</p>
  <PalcoArraste :estado="arraste" :clone="clone" />
</template>
