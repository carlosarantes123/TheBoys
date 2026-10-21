<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { criarTarefa } from '../api'
import FormularioTarefa from '../components/FormularioTarefa.vue'
import type { NovaTarefa } from '../tipos'

const router = useRouter()
const salvando = ref(false)
const erro = ref('')

async function salvar(dados: NovaTarefa) {
  salvando.value = true
  erro.value = ''
  try {
    const tarefa = await criarTarefa(dados)
    router.push(`/tarefas/${tarefa.id}`)
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

  <FormularioTarefa :enviando="salvando" @salvar="salvar" @cancelar="router.back()" />
</template>
