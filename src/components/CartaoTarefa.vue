<script setup lang="ts">
import { ref } from 'vue'
import type { Tarefa } from '../tipos'
import { formatarData, rotuloStatus } from '../rotulos'
import { excluirTarefa } from '../api'
import Icone from './Icone.vue'
import SeletorStatus from './SeletorStatus.vue'
import MarcaPrioridade from './MarcaPrioridade.vue'

const props = defineProps<{ tarefa: Tarefa }>()

const emit = defineEmits<{
  atualizada: [tarefa: Tarefa]
  excluida: [id: string]
}>()

const excluindo = ref(false)
const erro = ref('')

async function excluir(id: string) {
  if (!window.confirm(`Excluir a tarefa “${props.tarefa.titulo}”? Esta ação não pode ser desfeita.`)) return

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
  <article class="cartao cartao-tarefa">
    <h3>
      <RouterLink :to="`/tarefas/${tarefa.id}`">{{ tarefa.titulo }}</RouterLink>
    </h3>

    <p class="etiquetas">
      <span :class="['etiqueta', `status-${tarefa.status}`]">
        {{ rotuloStatus[tarefa.status] }}
      </span>

      <MarcaPrioridade :prioridade="tarefa.prioridade" />
    </p>

    <p>Responsável: {{ tarefa.responsavel }}</p>
    <p>Prazo: {{ formatarData(tarefa.prazo) }}</p>

    <SeletorStatus
      :tarefa="tarefa"
      @atualizada="emit('atualizada', $event)"
    />

    <button
      type="button"
      class="secondary-button botao-excluir"
      :disabled="excluindo"
      :aria-label="`Excluir tarefa ${tarefa.titulo}`"
      @click="excluir(tarefa.id)"
    >
      <Icone nome="lixeira" :tamanho="15" />
      {{ excluindo ? 'Excluindo...' : 'Excluir tarefa' }}
    </button>

    <p v-if="erro" role="alert">{{ erro }}</p>
  </article>
</template>