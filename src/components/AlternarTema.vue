<script setup lang="ts">
import { escolherTema, tema } from '../tema'
import type { Tema } from '../tema'
import Icone from './Icone.vue'

const opcoes: { valor: Tema; rotulo: string; icone: 'estrela' | 'raio' }[] = [
  { valor: 'heroi', rotulo: 'Herói', icone: 'estrela' },
  { valor: 'vilao', rotulo: 'Vilão', icone: 'raio' },
]
</script>

<template>
  <div class="alternar-tema" role="group" aria-label="Tema do aplicativo">
    <button
      v-for="opcao in opcoes"
      :key="opcao.valor"
      type="button"
      :aria-pressed="tema === opcao.valor"
      @click="escolherTema(opcao.valor)"
    >
      <Icone :nome="opcao.icone" :tamanho="16" :cheio="tema === opcao.valor" />
      {{ opcao.rotulo }}
    </button>
  </div>
</template>
