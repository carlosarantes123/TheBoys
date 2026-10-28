<script setup lang="ts">
import { filtros, limparFiltros, temFiltros } from '../filtros'
import { rotuloPrioridade, rotuloStatus } from '../rotulos'
import type { Prioridade, Status } from '../tipos'

const opcoesStatus = Object.entries(rotuloStatus) as [Status, string][]
const opcoesPrioridade = Object.entries(rotuloPrioridade) as [Prioridade, string][]
</script>

<template>
  <div class="filtros-tarefas">
    <select v-model="filtros.status" aria-label="Filtrar tarefas por status">
      <option value="">Todos os status</option>
      <option v-for="[valor, nome] in opcoesStatus" :key="valor" :value="valor">{{ nome }}</option>
    </select>
    <select v-model="filtros.prioridade" aria-label="Filtrar tarefas por prioridade">
      <option value="">Todas as prioridades</option>
      <option v-for="[valor, nome] in opcoesPrioridade" :key="valor" :value="valor">
        Prioridade {{ nome.toLowerCase() }}
      </option>
    </select>
    <button v-if="temFiltros()" type="button" class="limpar" @click="limparFiltros">Limpar filtros</button>
  </div>
</template>

<style scoped>
.filtros-tarefas {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.filtros-tarefas select {
  min-height: 40px;
  padding: 0 10px;
  border: 1px solid var(--border);
  border-radius: 8px;
  color: #4f5366;
  background: #fff;
  font-size: 11px;
}

.limpar {
  min-height: 40px;
  padding: 0 12px;
  border: 0;
  border-radius: 8px;
  color: var(--primary);
  background: transparent;
  font-size: 11px;
  font-weight: 700;
}

.limpar:hover {
  background: #f5f5fa;
}

@media (max-width: 600px) {
  .filtros-tarefas select {
    flex: 1;
  }
}
</style>
