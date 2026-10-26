<script setup lang="ts">
import type { Tarefa } from '../tipos'
import { formatarData, rotuloPrioridade, rotuloStatus } from '../rotulos'
import SeletorStatus from './SeletorStatus.vue'

defineProps<{ tarefa: Tarefa }>()
</script>

<template>
  <article class="cartao">
    <h3>
      <RouterLink :to="`/tarefas/${tarefa.id}`">{{ tarefa.titulo }}</RouterLink>
    </h3>
    <p class="etiquetas">
      <span :class="['etiqueta', `status-${tarefa.status}`]">{{ rotuloStatus[tarefa.status] }}</span>
      <span :class="['etiqueta', `prioridade-${tarefa.prioridade}`]">
        Prioridade {{ rotuloPrioridade[tarefa.prioridade].toLowerCase() }}
      </span>
    </p>
    <p>Responsável: {{ tarefa.responsavel }}</p>
    <p>Prazo: {{ formatarData(tarefa.prazo) }}</p>
    <SeletorStatus :tarefa="tarefa" />
  </article>
</template>