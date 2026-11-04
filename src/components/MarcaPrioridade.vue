<script setup lang="ts">
import { rotuloPrioridade } from '../rotulos'
import type { Prioridade } from '../tipos'
import Icone from './Icone.vue'

// A prioridade escrita por extenso, com uma forma que reforça o peso dela.
// A forma muda com o tema (cápsulas no herói, cortes no vilão) e é só reforço visual.
defineProps<{ prioridade: Prioridade }>()
</script>

<template>
  <span class="marca-prioridade" :class="`prio-${prioridade}`">
    <Icone v-if="prioridade === 'alta'" nome="raio" :tamanho="14" cheio />
    Prioridade {{ rotuloPrioridade[prioridade].toLowerCase() }}
  </span>
</template>
