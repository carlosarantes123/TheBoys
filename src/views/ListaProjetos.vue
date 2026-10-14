<script setup lang="ts">
import { listarProjetos } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import { formatarData } from '../rotulos'
</script>

<template>
  <h1>Projetos</h1>
  <CarregaDados :carregar="listarProjetos" v-slot="{ dados }">
    <p v-if="dados.length === 0">Nenhum projeto cadastrado.</p>
    <div class="grade">
      <article v-for="projeto in dados" :key="projeto.id" class="cartao">
        <h3><RouterLink :to="`/projetos/${projeto.id}`">{{ projeto.nome }}</RouterLink></h3>
        <p>{{ projeto.descricao }}</p>
        <p>Disciplina: {{ projeto.disciplina }}</p>
        <p>Criado em {{ formatarData(projeto.criadoEm) }}</p>
      </article>
    </div>
  </CarregaDados>
</template>
