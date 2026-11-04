<script setup lang="ts">
import { ref } from 'vue'
import type { Tarefa } from '../tipos'
import { formatarData, rotuloPrioridade, rotuloStatus } from '../rotulos'
import { excluirTarefa } from '../api'
import SeletorStatus from './SeletorStatus.vue'

defineProps<{ tarefa: Tarefa }>()

const emit = defineEmits<{
  atualizada: [tarefa: Tarefa]
  excluida: [id: string]
}>()

const excluindo = ref(false)
const erro = ref('')

async function excluir(id: string) {
  if (!window.confirm('Tem certeza de que deseja excluir esta tarefa?')) return

  excluindo.value = true
  erro.value = ''

  try {
    await excluirTarefa(id)
    emit('excluida', id)
  } catch {
    erro.value = 'Não foi possível excluir a tarefa. Tente novamente.'
  } finally {
    excluindo.value = false
  }
}
</script>

<template>
  <article class="cartao">
    <h3>
      <RouterLink :to="`/tarefas/${tarefa.id}`">{{ tarefa.titulo }}</RouterLink>
    </h3>

    <p class="etiquetas">
      <span :class="['etiqueta', `status-${tarefa.status}`]">
        {{ rotuloStatus[tarefa.status] }}
      </span>

      <span :class="['etiqueta', `prioridade-${tarefa.prioridade}`]">
        Prioridade {{ rotuloPrioridade[tarefa.prioridade].toLowerCase() }}
      </span>
    </p>

    <p>Responsável: {{ tarefa.responsavel }}</p>
    <p>Prazo: {{ formatarData(tarefa.prazo) }}</p>

    <SeletorStatus
      :tarefa="tarefa"
      @atualizada="emit('atualizada', $event)"
    />

    <button
      type="button"
      :disabled="excluindo"
      @click="excluir(tarefa.id)"
    >
      {{ excluindo ? 'Excluindo...' : 'Excluir tarefa' }}
    </button>

    <p v-if="erro" role="alert">{{ erro }}</p>
  </article>
</template>