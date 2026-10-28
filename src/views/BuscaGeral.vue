<script setup lang="ts">
import { listarProjetos, listarTarefas } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import CartaoTarefa from '../components/CartaoTarefa.vue'
import { filtrarProjetos, filtrarTarefas, filtros, temBusca } from '../filtros'
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
      </div>

      <h2>Projetos</h2>
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
      <p v-if="filtrarTarefas(tarefas).length === 0">Nenhuma tarefa encontrada para “{{ filtros.busca.trim() }}”.</p>
      <div class="grade">
        <CartaoTarefa v-for="tarefa in filtrarTarefas(tarefas)" :key="tarefa.id" :tarefa="tarefa" />
      </div>
    </template>
  </CarregaDados>
</template>
