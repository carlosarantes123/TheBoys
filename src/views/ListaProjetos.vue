<script setup lang="ts">
import { listarProjetos } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import { filtrarProjetos, filtros } from '../filtros'
import { formatarData } from '../rotulos'
</script>

<template>
  <h1>Projetos</h1>
  <CarregaDados :carregar="listarProjetos" v-slot="{ dados }">
    <div class="board-toolbar">
      <div>
        <span class="task-total">{{ filtrarProjetos(dados).length }} projetos</span>
      </div>
      <label class="search-box">
        <span>⌕</span>
        <input v-model="filtros.busca" type="search" placeholder="Buscar por título..." aria-label="Buscar projetos por título" />
      </label>
    </div>

    <p v-if="dados.length === 0">Nenhum projeto cadastrado.</p>
    <p v-else-if="filtrarProjetos(dados).length === 0">Nenhum projeto encontrado para “{{ filtros.busca.trim() }}”.</p>
    <div class="grade">
      <article v-for="projeto in filtrarProjetos(dados)" :key="projeto.id" class="cartao">
        <h3><RouterLink :to="`/projetos/${projeto.id}`">{{ projeto.nome }}</RouterLink></h3>
        <p>{{ projeto.descricao }}</p>
        <p>Disciplina: {{ projeto.disciplina }}</p>
        <p>Criado em {{ formatarData(projeto.criadoEm) }}</p>
      </article>
    </div>
  </CarregaDados>
</template>
