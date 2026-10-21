<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { atualizarTarefa, buscarTarefa } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import FormularioTarefa from '../components/FormularioTarefa.vue'
import type { NovaTarefa } from '../tipos'

const route = useRoute()
const router = useRouter()
const id = String(route.params.id)
const salvando = ref(false)
const erro = ref('')

async function salvar(dados: NovaTarefa) {
  salvando.value = true
  erro.value = ''
  try {
    await atualizarTarefa(id, dados)
    router.push(`/tarefas/${id}`)
  } catch {
    erro.value = 'Não foi possível salvar. Verifique se o JSON Server está funcionando.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <div class="form-heading">
    <RouterLink class="back-button" :to="`/tarefas/${id}`">← Voltar para a tarefa</RouterLink>
    <p class="eyebrow">GERENCIAMENTO DE ATIVIDADES</p>
    <h1>Editar tarefa</h1>
    <p class="page-description">Altere as informações e salve para atualizar a tarefa.</p>
    <p v-if="erro" class="notice error" role="alert">{{ erro }}</p>
  </div>

  <CarregaDados :carregar="() => buscarTarefa(id)" v-slot="{ dados: tarefa }">
    <FormularioTarefa
      :tarefa="tarefa"
      :enviando="salvando"
      @salvar="salvar"
      @cancelar="router.push(`/tarefas/${id}`)"
    />
  </CarregaDados>
</template>
