<script setup lang="ts">
import { listarProjetos, listarTarefas } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import FiltrosTarefas from '../components/FiltrosTarefas.vue'
import CartaoTarefa from '../components/CartaoTarefa.vue'
import { filtrarProjetos, filtrarTarefas, filtros, temBusca, temFiltros } from '../filtros'
import { formatarData } from '../rotulos'

const carregar = async () => {
  const [tarefas, projetos] = await Promise.all([listarTarefas(), listarProjetos()])
  return { tarefas, projetos }
}
</script>

<template>
  <h1>Busca</h1>

  <CarregaDados :carregar="carregar" v-slot="{ dados: { tarefas, projetos } }">
    <!-- O campo de busca é o da barra superior (App.vue), que traz até esta tela. -->
    <p v-if="!temBusca()">Digite um título no campo de busca, no topo, para buscar entre as tarefas e os projetos.</p>
    <template v-else>
      <div class="board-toolbar">
        <div>
          <span class="task-total">{{ filtrarTarefas(tarefas).length }} tarefas</span>
          <span class="task-total">{{ filtrarProjetos(projetos).length }} projetos</span>
        </div>
        <FiltrosTarefas />
      </div>

      <h2>Projetos</h2>
      <p v-if="temFiltros()" class="aviso-filtros">Os filtros de status e prioridade valem só para as tarefas.</p>
      <p v-if="filtrarProjetos(projetos).length === 0">Nenhum projeto encontrado para “{{ filtros.busca.trim() }}”.</p>
      <div class="grade">
        <article v-for="projeto in filtrarProjetos(projetos)" :key="projeto.id" class="cartao">
          <h3><RouterLink :to="`/projetos/${projeto.id}`">{{ projeto.nome }}</RouterLink></h3>
          <p>{{ projeto.descricao }}</p>
          <p>Disciplina: {{ projeto.disciplina }}</p>
          <p>Criado em {{ formatarData(projeto.criadoEm) }}</p>
        </article>
      </div>

      <h2>Tarefas</h2>
      <p v-if="filtrarTarefas(tarefas).length === 0">Nenhuma tarefa encontrada<template v-if="temBusca()"> para “{{ filtros.busca.trim() }}”</template><template v-if="temFiltros()"> com os filtros escolhidos</template>.</p>
      <div class="grade">
        <CartaoTarefa v-for="tarefa in filtrarTarefas(tarefas)" :key="tarefa.id" :tarefa="tarefa" />
      </div>
    </template>
  </CarregaDados>
</template>
