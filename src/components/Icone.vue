<script setup lang="ts">
// Ícones em SVG próprio (traço simples). São decorativos: o texto ao lado diz o que é.
export type NomeIcone =
  | 'lista'
  | 'quadro'
  | 'pasta'
  | 'mais'
  | 'busca'
  | 'estrela'
  | 'trofeu'
  | 'relogio'
  | 'check'
  | 'lixeira'
  | 'raio'

const caminhos: Record<NomeIcone, string[]> = {
  lista: ['M8 6h13', 'M8 12h13', 'M8 18h13', 'M3.5 6h.01', 'M3.5 12h.01', 'M3.5 18h.01'],
  quadro: ['M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z', 'M9 3v18', 'M15 3v18'],
  pasta: ['M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'],
  mais: ['M12 5v14', 'M5 12h14'],
  busca: ['M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14z', 'M21 21l-4.3-4.3'],
  estrela: ['M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z'],
  trofeu: ['M8 21h8', 'M12 17v4', 'M7 4h10v5a5 5 0 0 1-10 0z', 'M17 5h3v2a3 3 0 0 1-3 3', 'M7 5H4v2a3 3 0 0 0 3 3'],
  relogio: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z', 'M12 7v5l3 2'],
  check: ['M5 12.5l4.5 4.5L19 7'],
  lixeira: ['M4 7h16', 'M10 11v6', 'M14 11v6', 'M6 7l1 13h10l1-13', 'M9 7V4h6v3'],
  raio: ['M13 2 4 14h7l-1 8 9-12h-7z'],
}

withDefaults(defineProps<{ nome: NomeIcone; tamanho?: number; cheio?: boolean }>(), {
  tamanho: 20,
  cheio: false,
})
</script>

<template>
  <svg
    class="icone"
    viewBox="0 0 24 24"
    :width="tamanho"
    :height="tamanho"
    :fill="cheio ? 'currentColor' : 'none'"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    focusable="false"
  >
    <path v-for="d in caminhos[nome]" :key="d" :d="d" />
  </svg>
</template>

<style scoped>
.icone {
  flex-shrink: 0;
  vertical-align: middle;
}
</style>
