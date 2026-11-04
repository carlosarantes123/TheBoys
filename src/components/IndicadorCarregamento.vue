<script setup lang="ts">
// Indicação visível enquanto os dados não chegam: um aviso com spinner
// e um "esqueleto" no formato da tela, para o conteúdo não pular quando chegar.
export type FormatoCarregamento = 'cartoes' | 'quadro' | 'detalhe' | 'formulario'

withDefaults(defineProps<{ mensagem?: string; formato?: FormatoCarregamento }>(), {
  mensagem: 'Carregando…',
  formato: 'cartoes',
})
</script>

<template>
  <div class="carregamento" aria-busy="true">
    <p class="carregamento-aviso" role="status">
      <span class="carregamento-spinner" aria-hidden="true"></span>
      {{ mensagem }}
    </p>

    <!-- O esqueleto é só visual: leitores de tela ouvem apenas o aviso acima. -->
    <div aria-hidden="true">
      <div v-if="formato === 'cartoes'" class="grade">
        <div v-for="n in 6" :key="n" class="cartao esqueleto-cartao">
          <span class="esqueleto linha titulo"></span>
          <span class="esqueleto linha curta"></span>
          <span class="esqueleto linha"></span>
          <span class="esqueleto linha media"></span>
        </div>
      </div>

      <template v-else-if="formato === 'quadro'">
        <div class="summary-grid">
          <div v-for="n in 3" :key="n" class="summary-card">
            <span class="esqueleto bloco icone"></span>
            <div class="esqueleto-resumo">
              <span class="esqueleto linha curta"></span>
              <span class="esqueleto linha numero"></span>
            </div>
          </div>
        </div>
        <div class="kanban-board">
          <div v-for="coluna in 4" :key="coluna" class="kanban-column">
            <span class="esqueleto linha media"></span>
            <div v-for="n in 2" :key="n" class="cartao esqueleto-cartao">
              <span class="esqueleto linha curta"></span>
              <span class="esqueleto linha titulo"></span>
              <span class="esqueleto linha"></span>
            </div>
          </div>
        </div>
      </template>

      <template v-else-if="formato === 'detalhe'">
        <span class="esqueleto linha cabecalho"></span>
        <div class="detalhes esqueleto-detalhes">
          <template v-for="n in 6" :key="n">
            <span class="esqueleto linha rotulo"></span>
            <span class="esqueleto linha"></span>
          </template>
        </div>
      </template>

      <div v-else class="task-form esqueleto-formulario">
        <div v-for="n in 4" :key="n" class="esqueleto-campo">
          <span class="esqueleto linha rotulo"></span>
          <span class="esqueleto bloco campo"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.carregamento-aviso {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 16px;
  padding: 8px 14px;
  border: 1px solid #ddd8ff;
  border-radius: 999px;
  color: var(--primary);
  background: #f3f1ff;
  font-size: 13px;
  font-weight: 700;
}

.carregamento-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #ddd8ff;
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: girar 0.8s linear infinite;
}

.esqueleto {
  display: block;
  border-radius: 6px;
  background: linear-gradient(90deg, #ecedf3 25%, #f6f6fa 50%, #ecedf3 75%);
  background-size: 200% 100%;
  animation: brilhar 1.4s ease-in-out infinite;
}

.linha {
  width: 100%;
  height: 10px;
  margin: 8px 0;
}

.linha.titulo { width: 70%; height: 14px; }
.linha.curta { width: 40%; }
.linha.media { width: 60%; }
.linha.rotulo { width: 90px; }
.linha.numero { width: 32px; height: 18px; }
.linha.cabecalho { width: min(380px, 70%); height: 24px; margin-bottom: 20px; }

.bloco.icone {
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  border-radius: 9px;
}

.bloco.campo {
  width: 100%;
  height: 38px;
}

.esqueleto-resumo {
  flex: 1;
}

.esqueleto-cartao {
  margin-top: 10px;
}

.esqueleto-detalhes .linha {
  margin: 4px 0;
}

.esqueleto-campo + .esqueleto-campo {
  margin-top: 18px;
}

@keyframes girar {
  to { transform: rotate(360deg); }
}

@keyframes brilhar {
  from { background-position: 100% 0; }
  to { background-position: -100% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .carregamento-spinner { animation-duration: 2.4s; }
  .esqueleto { animation: none; }
}
</style>
