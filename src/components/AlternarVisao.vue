<template>
  <nav class="alternar-visao" aria-label="Alternar visão das tarefas">
    <RouterLink to="/" exact-active-class="ativa">Lista</RouterLink>
    <RouterLink to="/quadro" exact-active-class="ativa">Quadro</RouterLink>
  </nav>
</template>

<style scoped>
.alternar-visao {
  display: inline-flex;
  margin-bottom: 20px;
  padding: 3px;
  border: 1px solid var(--border);
  border-radius: 9px;
  background: var(--surface);
}

.alternar-visao a {
  padding: 8px 18px;
  border-radius: 7px;
  color: #4f5366;
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
}

.alternar-visao a:hover {
  background: #f5f5fa;
}

.alternar-visao a.ativa {
  color: #fff;
  background: var(--primary);
}

.alternar-visao a:focus-visible {
  outline: 3px solid #c5bdff;
  outline-offset: 2px;
}
</style>