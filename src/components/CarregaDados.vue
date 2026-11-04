<script setup lang="ts" generic="T">
import { onMounted, ref } from 'vue'
import { ErroNaoEncontrado } from '../api'
import AvisoErroApi from './AvisoErroApi.vue'
import AvisoNaoEncontrado from './AvisoNaoEncontrado.vue'
import IndicadorCarregamento, { type FormatoCarregamento } from './IndicadorCarregamento.vue'

const props = defineProps<{
  carregar: () => Promise<T>
  // Texto e formato do indicador mostrado enquanto os dados não chegam.
  mensagem?: string
  formato?: FormatoCarregamento
}>()

const dados = ref<T | null>(null)
const carregando = ref(true)
const erro = ref<Error | null>(null)
// Quantas vezes a pessoa clicou em "Tentar de novo" (zera quando dá certo).
const tentativas = ref(0)

function tentarDeNovo() {
  tentativas.value++
  executar()
}

async function executar() {
  carregando.value = true
  erro.value = null
  try {
    dados.value = (await props.carregar()) as never
    tentativas.value = 0
  } catch (e) {
    erro.value = e instanceof Error ? e : new Error(String(e))
  } finally {
    carregando.value = false
  }
}

onMounted(executar)
</script>

<template>
  <IndicadorCarregamento v-if="carregando" :mensagem="mensagem" :formato="formato" />
  <AvisoNaoEncontrado v-else-if="erro instanceof ErroNaoEncontrado" />
  <AvisoErroApi v-else-if="erro" :erro="erro" :tentativas="tentativas" @tentar-de-novo="tentarDeNovo" />
  <slot v-else-if="dados" :dados="dados as T" />
</template>
