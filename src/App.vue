<script setup lang="ts">
import { watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AlternarTema from './components/AlternarTema.vue'
import Icone from './components/Icone.vue'
import { filtros } from './filtros'

const route = useRoute()
const router = useRouter()

// Cada tela tem o seu título na aba: quem usa leitor de tela sabe onde está.
watchEffect(() => {
  const titulo = route.meta.titulo as string | undefined
  document.title = titulo ? `${titulo} | TheBoys` : 'TheBoys'
})

// A busca do topo mostra tarefas e projetos juntos, na tela /busca.
function irParaBusca() {
  if (route.path !== '/busca') router.push('/busca')
}
</script>

<template>
  <div class="app-shell">
    <header class="masthead">
      <div class="masthead-linha">
        <RouterLink class="marca" to="/" aria-label="TheBoys, página inicial">TheBoys</RouterLink>

        <nav class="menu" aria-label="Principal">
          <RouterLink class="menu-item" exact-active-class="active" to="/">Tarefas</RouterLink>
          <RouterLink class="menu-item" active-class="active" to="/quadro">Quadro</RouterLink>
          <RouterLink class="menu-item" active-class="active" to="/projetos">Projetos</RouterLink>
        </nav>

        <div class="masthead-acoes">
          <label class="search-box top-search">
            <Icone nome="busca" :tamanho="18" />
            <input
              v-model="filtros.busca"
              type="search"
              placeholder="Buscar tarefas e projetos"
              aria-label="Buscar tarefas e projetos por título"
              @input="irParaBusca"
              @keydown.enter="irParaBusca"
            />
          </label>
          <RouterLink class="primary-button" to="/tarefas/nova">Nova tarefa</RouterLink>
          <AlternarTema />
        </div>
      </div>
    </header>

    <main class="page-content">
      <!-- key: remonta a tela ao trocar de id (ex.: /projetos/1 para /projetos/2) -->
      <RouterView :key="$route.fullPath" />
    </main>
  </div>
</template>
