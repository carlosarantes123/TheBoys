<script setup lang="ts">
import { listarTarefas } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import CartaoTarefa from '../components/CartaoTarefa.vue'
</script>

<template>
  <h1>Tarefas</h1>
  <CarregaDados :carregar="listarTarefas" v-slot="{ dados }">
    <p v-if="dados.length === 0">Nenhuma tarefa cadastrada.</p>
    <div class="grade">
      <CartaoTarefa v-for="tarefa in dados" :key="tarefa.id" :tarefa="tarefa" />
    </div>
  </CarregaDados>
</template>
