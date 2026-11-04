
<script setup lang="ts">
import { listarTarefas } from '../api'
import AlternarVisao from '../components/AlternarVisao.vue'
import Icone from '../components/Icone.vue'
import CarregaDados from '../components/CarregaDados.vue'
import FiltrosTarefas from '../components/FiltrosTarefas.vue'
import CartaoTarefa from '../components/CartaoTarefa.vue'
import { removerTarefa, substituirTarefa } from '../tarefas'
import { filtrarTarefas, filtros, temBusca, temFiltros } from '../filtros'
</script>

<template>
  <h1>Tarefas</h1>
  <AlternarVisao />

  <CarregaDados :carregar="listarTarefas" mensagem="Carregando tarefas…" v-slot="{ dados }">
    <div class="board-toolbar">
      <div>
        <span class="task-total">{{ filtrarTarefas(dados).length }} tarefas</span>
      </div>
      <div>
        <FiltrosTarefas />
        <label class="search-box">
          <Icone nome="busca" :tamanho="18" />
          <input v-model="filtros.busca" type="search" placeholder="Buscar por título" aria-label="Buscar tarefas por título" />
        </label>
      </div>
    </div>

    <p v-if="dados.length === 0" class="vazio">Nenhuma tarefa cadastrada. Use “Nova tarefa” para criar a primeira.</p>
    <p v-else-if="filtrarTarefas(dados).length === 0">Nenhuma tarefa encontrada<template v-if="temBusca()"> para “{{ filtros.busca.trim() }}”</template><template v-if="temFiltros()"> com os filtros escolhidos</template>.</p>

    <h2 class="sr-only">Lista de tarefas</h2>
    <div class="grade">
      <CartaoTarefa
        v-for="tarefa in filtrarTarefas(dados)"
        :key="tarefa.id"
        :tarefa="tarefa"
        @atualizada="substituirTarefa(dados, $event)"
        @excluida="removerTarefa(dados, $event)"
      />
    </div>
  </CarregaDados>
</template>
