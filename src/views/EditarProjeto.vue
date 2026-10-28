<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { atualizarProjeto, buscarProjeto, type NovoProjeto } from '../api'
import CarregaDados from '../components/CarregaDados.vue'
import FormularioProjeto from '../components/FormularioProjeto.vue'

const route = useRoute()
const router = useRouter()
const id = String(route.params.id)
const salvando = ref(false)
const erro = ref('')

async function salvar(dados: NovoProjeto) {
  salvando.value = true
  erro.value = ''
  try {
    await atualizarProjeto(id, dados)
    router.push(`/projetos/${id}`)
  } catch {
    erro.value = 'Não foi possível salvar. Verifique se o JSON Server está funcionando.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <div class="form-heading">
    <RouterLink class="back-button" :to="`/projetos/${id}`">← Voltar para o projeto</RouterLink>
    <p class="eyebrow">GERENCIAMENTO DE PROJETOS</p>
    <h1>Editar projeto</h1>
    <p class="page-description">Altere as informações e salve para atualizar o projeto.</p>
    <p v-if="erro" class="notice error" role="alert">{{ erro }}</p>
  </div>

  <CarregaDados :carregar="() => buscarProjeto(id)" v-slot="{ dados: projeto }">
    <FormularioProjeto
      :projeto="projeto"
      :enviando="salvando"
      @salvar="salvar"
      @cancelar="router.push(`/projetos/${id}`)"
    />
  </CarregaDados>
</template>
