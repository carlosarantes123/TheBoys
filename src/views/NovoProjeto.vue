<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { criarProjeto, type NovoProjeto } from '../api'
import FormularioProjeto from '../components/FormularioProjeto.vue'

const router = useRouter()
const salvando = ref(false)
const erro = ref('')

async function salvar(dados: NovoProjeto) {
  salvando.value = true
  erro.value = ''
  try {
    const projeto = await criarProjeto(dados)
    router.push(`/projetos/${projeto.id}`)
  } catch {
    erro.value = 'Não foi possível salvar. Verifique se o JSON Server está funcionando.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <div class="form-heading">
    <RouterLink class="back-button" to="/projetos">← Voltar para os projetos</RouterLink>
    <p class="eyebrow">GERENCIAMENTO DE PROJETOS</p>
    <h1>Novo projeto</h1>
    <p class="page-description">Preencha as informações para cadastrar um projeto.</p>
    <p v-if="erro" class="notice error" role="alert">{{ erro }}</p>
  </div>

  <FormularioProjeto :enviando="salvando" @salvar="salvar" @cancelar="router.push('/projetos')" />
</template>
