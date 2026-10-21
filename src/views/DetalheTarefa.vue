<script setup lang="ts">
import { useRoute } from 'vue-router'
import { buscarTarefa } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import { formatarData, rotuloPrioridade, rotuloStatus } from '../rotulos'

const route = useRoute()
const id = String(route.params.id)
</script>

<template>
  <CarregaDados :carregar="() => buscarTarefa(id)" v-slot="{ dados: tarefa }">
    <h1>{{ tarefa.titulo }}</h1>
    <dl class="detalhes">
      <dt>Descrição</dt>
      <dd>{{ tarefa.descricao }}</dd>
      <dt>Status</dt>
      <dd>{{ rotuloStatus[tarefa.status] }}</dd>
      <dt>Prioridade</dt>
      <dd>{{ rotuloPrioridade[tarefa.prioridade] }}</dd>
      <dt>Responsável</dt>
      <dd>{{ tarefa.responsavel }}</dd>
      <dt>Prazo</dt>
      <dd>{{ formatarData(tarefa.prazo) }}</dd>
      <dt>Projeto</dt>
      <dd><RouterLink :to="`/projetos/${tarefa.projetoId}`">Ver projeto {{ tarefa.projetoId }}</RouterLink></dd>
    </dl>
    <p class="acoes">
      <RouterLink class="primary-button" :to="`/tarefas/${tarefa.id}/editar`">✎ Editar tarefa</RouterLink>
      <RouterLink to="/">← Voltar para as tarefas</RouterLink>
    </p>
  </CarregaDados>
</template>
