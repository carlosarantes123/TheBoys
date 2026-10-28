<script setup lang="ts">
import { useRoute } from 'vue-router'
import { buscarProjetoComTarefas } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import CartaoTarefa from '../components/CartaoTarefa.vue'
import { substituirTarefa } from '../tarefas'
import { formatarData } from '../rotulos'

const route = useRoute()
const id = String(route.params.id)
</script>

<template>
  <CarregaDados :carregar="() => buscarProjetoComTarefas(id)" v-slot="{ dados: projeto }">
    <h1>{{ projeto.nome }}</h1>
    <p>{{ projeto.descricao }}</p>
    <p>Disciplina: {{ projeto.disciplina }} · Criado em {{ formatarData(projeto.criadoEm) }}</p>
    <p class="acoes">
      <RouterLink class="primary-button" :to="`/tarefas/nova?projetoId=${projeto.id}`">
        ＋ Nova tarefa neste projeto
      </RouterLink>
      <RouterLink class="secondary-button" :to="`/projetos/${projeto.id}/editar`">
        ✎ Editar projeto
      </RouterLink>
    </p>
    <h2>Tarefas do projeto</h2>
    <p v-if="projeto.tarefas.length === 0">Este projeto ainda não tem tarefas.</p>
    <div class="grade">
      <CartaoTarefa
        v-for="tarefa in projeto.tarefas"
        :key="tarefa.id"
        :tarefa="tarefa"
        @atualizada="substituirTarefa(projeto.tarefas, $event)"
      />
    </div>
    <p><RouterLink to="/projetos">← Voltar para os projetos</RouterLink></p>
  </CarregaDados>
</template>
