<script setup lang="ts">
import { reactive } from 'vue'
import { listarProjetos } from '../api'
import CarregaDados from './CarregaDados.vue'
import { rotuloPrioridade, rotuloStatus } from '../rotulos'
import type { NovaTarefa, Prioridade, Status, Tarefa } from '../tipos'

// Sem `tarefa` o formulário cadastra; com `tarefa` ele edita.
const props = defineProps<{ tarefa?: Tarefa; enviando?: boolean }>()
const emit = defineEmits<{ salvar: [dados: NovaTarefa] }>()

const opcoesStatus = Object.entries(rotuloStatus) as [Status, string][]
const opcoesPrioridade = Object.entries(rotuloPrioridade) as [Prioridade, string][]

const form = reactive<NovaTarefa>({
  projetoId: props.tarefa?.projetoId ?? '',
  titulo: props.tarefa?.titulo ?? '',
  descricao: props.tarefa?.descricao ?? '',
  status: props.tarefa?.status ?? 'a-fazer',
  prioridade: props.tarefa?.prioridade ?? 'media',
  responsavel: props.tarefa?.responsavel ?? '',
  prazo: props.tarefa?.prazo ?? '',
})

function enviar() {
  emit('salvar', {
    ...form,
    titulo: form.titulo.trim(),
    descricao: form.descricao.trim(),
    responsavel: form.responsavel.trim(),
  })
}
</script>

<template>
  <CarregaDados :carregar="listarProjetos" v-slot="{ dados: projetos }">
    <form class="formulario" @submit.prevent="enviar">
      <label>
        Título
        <input v-model="form.titulo" type="text" required pattern=".*\S.*" />
      </label>

      <label>
        Descrição
        <textarea v-model="form.descricao" rows="4" />
      </label>

      <label>
        Projeto
        <select v-model="form.projetoId" required>
          <option value="" disabled>Selecione um projeto</option>
          <option v-for="projeto in projetos" :key="projeto.id" :value="projeto.id">
            {{ projeto.nome }}
          </option>
        </select>
      </label>

      <label>
        Status
        <select v-model="form.status" required>
          <option v-for="[valor, rotulo] in opcoesStatus" :key="valor" :value="valor">
            {{ rotulo }}
          </option>
        </select>
      </label>

      <label>
        Prioridade
        <select v-model="form.prioridade" required>
          <option v-for="[valor, rotulo] in opcoesPrioridade" :key="valor" :value="valor">
            {{ rotulo }}
          </option>
        </select>
      </label>

      <label>
        Responsável
        <input v-model="form.responsavel" type="text" required pattern=".*\S.*" />
      </label>

      <label>
        Prazo
        <input v-model="form.prazo" type="date" required />
      </label>

      <button type="submit" :disabled="enviando">
        {{ tarefa ? 'Salvar alterações' : 'Cadastrar tarefa' }}
      </button>
    </form>
  </CarregaDados>
</template>
