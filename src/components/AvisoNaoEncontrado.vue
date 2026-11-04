<script setup lang="ts">
// Mostrado quando a API responde 404: a tarefa ou o projeto da URL não existe (ou foi excluído).
</script>

<template>
  <div class="nao-encontrado" role="alert">
    <p class="nao-encontrado-titulo">Não encontrado</p>
    <p>O item que você tentou abrir não existe ou foi excluído.</p>
    <p class="nao-encontrado-links">
      <RouterLink class="primary-button" to="/">Ver as tarefas</RouterLink>
      <RouterLink class="secondary-button" to="/projetos">Ver os projetos</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.nao-encontrado {
  max-width: 620px;
  padding: 18px 20px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface);
}

.nao-encontrado p {
  margin: 0 0 8px;
  font-size: 13px;
  line-height: 1.5;
}

.nao-encontrado .nao-encontrado-titulo {
  color: var(--text);
  font-size: 16px;
  font-weight: 700;
}

.nao-encontrado-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.nao-encontrado-links a {
  text-decoration: none;
}
</style>
