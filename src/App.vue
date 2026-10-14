<template>
  <header class="topo">
    <span class="marca">TheBoys · Gerenciador de Tarefas</span>
    <nav aria-label="Principal">
      <RouterLink to="/">Tarefas</RouterLink>
      <RouterLink to="/projetos">Projetos</RouterLink>
    </nav>
  </header>
  <main class="conteudo">
    <!-- key: remonta a tela ao trocar de id (ex.: /projetos/1 → /projetos/2) -->
    <RouterView :key="$route.fullPath" />
  </main>
</template>
