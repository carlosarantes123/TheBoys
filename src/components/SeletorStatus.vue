<script setup lang="ts">
import { ref } from 'vue'
import { atualizarStatusTarefa } from '../api'
import { rotuloStatus } from '../rotulos'
import type { Status, Tarefa } from '../tipos'

const props = defineProps<{ tarefa: Tarefa }>()
// Avisa o dono da lista com a tarefa devolvida pela API; ele troca o objeto no array.
const emit = defineEmits<{ atualizada: [tarefa: Tarefa] }>()

const opcoes = Object.entries(rotuloStatus) as [Status, string][]
const salvando = ref(false)
const erro = ref('')

async function mudar(evento: Event) {
  const seletor = evento.target as HTMLSelectElement
  const anterior = props.tarefa.status
  const novo = seletor.value as Status

  salvando.value = true
  erro.value = ''
  try {
    const salva = await atualizarStatusTarefa(props.tarefa.id, novo)
    emit('atualizada', salva)
  } catch {
    erro.value = 'Não foi possível salvar o status. Tente de novo.'
    seletor.value = anterior
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <div class="seletor-status">
    <select
      :value="tarefa.status"
      :disabled="salvando"
      :aria-label="`Status da tarefa ${tarefa.titulo}`"
      @change="mudar"
    >
      <option v-for="[valor, nome] in opcoes" :key="valor" :value="valor">{{ nome }}</option>
    </select>
    <small v-if="erro" role="alert">{{ erro }}</small>
  </div>
</template>

<style scoped>
.seletor-status {
  margin: 8px 0 12px;
}

.seletor-status select {
  width: 100%;
  min-height: 32px;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: #4f5366;
  background: #fff;
  font-size: 11px;
}

.seletor-status small {
  display: block;
  margin-top: 4px;
  color: #c14d58;
  font-size: 10px;
}
</style>