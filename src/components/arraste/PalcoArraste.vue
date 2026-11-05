<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { EstadoArraste } from '../../arraste'
import { tema } from '../../tema'
// Desenhos originais em SVG, gerados por script (ferramentas/gerar_personagens.py).
import heroiSvg from './heroi.svg?raw'
import vilaoSvg from './vilao.svg?raw'

// Camada por cima de tudo: o cartão que voa e o personagem do tema.
// Herói: fica atrás do cartão e empurra. Vilão: vai na frente e puxa com os tentáculos.
const props = defineProps<{ estado: EstadoArraste; clone: HTMLElement | null }>()

const suporte = ref<HTMLElement | null>(null)
const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches

// O cartão clonado é um elemento pronto; só o colocamos dentro do suporte.
watch(
  () => [props.clone, suporte.value] as const,
  ([copia, alvo]) => {
    if (alvo) alvo.replaceChildren(...(copia ? [copia] : []))
  },
  { flush: 'post' },
)

const desenho = computed(() => (tema.value === 'heroi' ? heroiSvg : vilaoSvg))
const estilo = computed(() => ({
  width: `${props.estado.largura}px`,
  transform: `translate3d(${props.estado.x}px, ${props.estado.y}px, 0)`,
  transitionDuration: `${props.estado.duracao}ms`,
}))
</script>

<template>
  <Teleport to="#app">
    <div
      v-if="estado.fase !== 'parado'"
      class="palco-arraste"
      :class="[`fase-${estado.fase}`, estado.direcao > 0 ? 'para-direita' : 'para-esquerda', `ator-${tema}`]"
      :style="estilo"
      aria-hidden="true"
    >
      <div ref="suporte" class="suporte-cartao" :style="{ transform: `rotate(${estado.inclinacao}deg)` }"></div>
      <!-- v-html só com o desenho do próprio projeto (arquivo estático, sem dado do usuário) -->
      <div v-if="!reduzMovimento" class="ator" v-html="desenho"></div>
    </div>
  </Teleport>
</template>
