<script setup lang="ts" generic="T">
import { onMounted, ref } from 'vue'
import { ErroNaoEncontrado } from '../api'

const props = defineProps<{ carregar: () => Promise<T> }>()

const dados = ref<T | null>(null)
const carregando = ref(true)
const erro = ref<Error | null>(null)

async function executar() {
  carregando.value = true
  erro.value = null
  try {
    dados.value = (await props.carregar()) as never
  } catch (e) {
    erro.value = e instanceof Error ? e : new Error(String(e))
  } finally {
    carregando.value = false
  }
}

onMounted(executar)
</script>

<template>
  <p v-if="carregando" role="status">Carregando…</p>
  <p v-else-if="erro instanceof ErroNaoEncontrado" role="alert">Não encontrado.</p>
  <div v-else-if="erro" role="alert">
    <p>Não foi possível carregar os dados. A API está no ar?</p>
    <button type="button" @click="executar">Tentar de novo</button>
  </div>
  <slot v-else-if="dados" :dados="dados as T" />
</template>
