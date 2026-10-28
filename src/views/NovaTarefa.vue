<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { criarTarefa } from '../api'
import FormularioTarefa from '../components/FormularioTarefa.vue'
import type { NovaTarefa } from '../tipos'

const route = useRoute()
const router = useRouter()
// Vindo da página de um projeto (?projetoId=1), o projeto já vem selecionado.
const projetoIdInicial = typeof route.query.projetoId === 'string' ? route.query.projetoId : undefined
const salvando = ref(false)
const erro = ref('')

async function salvar(dados: NovaTarefa) {
  salvando.value = true
  erro.value = ''
  try {
    await criarTarefa(dados)
    router.push('/')
  } catch {
    erro.value = 'Não foi possível salvar. Verifique se o JSON Server está funcionando.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <div class="form-heading">
    <button class="back-button" type="button" @click="router.back()">← Voltar</button>
    <p class="eyebrow">GERENCIAMENTO DE ATIVIDADES</p>
    <h1>Nova tarefa</h1>
    <p class="page-description">
      Preencha as informações abaixo para adicionar uma atividade ao quadro.
    </p>
    <p v-if="erro" class="notice error" role="alert">{{ erro }}</p>
  </div>

  <FormularioTarefa
    :enviando="salvando"
    :projeto-id-inicial="projetoIdInicial"
    @salvar="salvar"
    @cancelar="router.back()"
  />
</template>
