<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const tituloPagina = computed(() => (route.meta.titulo as string | undefined) ?? 'TheBoys')
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <RouterLink class="brand" to="/">
        <span class="brand-icon">T</span>
        <span>
          <strong>TheBoys</strong>
          <small>Gerenciador de tarefas</small>
        </span>
      </RouterLink>

      <p class="menu-label">ESPAÇO DE TRABALHO</p>

      <nav aria-label="Principal">
        <RouterLink class="menu-item" exact-active-class="active" to="/">
          <span class="menu-icon">☰</span>
          Tarefas
        </RouterLink>
        <RouterLink class="menu-item" active-class="active" to="/quadro">
          <span class="menu-icon">▦</span>
          Meu quadro
        </RouterLink>
        <RouterLink class="menu-item" active-class="active" to="/projetos">
          <span class="menu-icon">◫</span>
          Projetos
        </RouterLink>
        <RouterLink class="menu-item" exact-active-class="active" to="/tarefas/nova">
          <span class="menu-icon">＋</span>
          Nova tarefa
        </RouterLink>
      </nav>

      <div class="sidebar-bottom">
        <span class="avatar">TB</span>
        <div>
          <strong>Equipe TheBoys</strong>
          <small>Projeto acadêmico</small>
        </div>
      </div>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <div class="breadcrumb">
          <span>Workspace</span>
          <span class="breadcrumb-separator">/</span>
          <strong>{{ tituloPagina }}</strong>
        </div>

        <RouterLink class="primary-button top-create" to="/tarefas/nova">
          <span>＋</span> Nova tarefa
        </RouterLink>
      </header>

      <section class="page-content">
        <!-- key: remonta a tela ao trocar de id (ex.: /projetos/1 → /projetos/2) -->
        <RouterView :key="$route.fullPath" />
      </section>
    </main>
  </div>
</template>
