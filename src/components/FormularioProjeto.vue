<script setup lang="ts">
import { reactive, useTemplateRef } from 'vue'
import type { NovoProjeto } from '../api'
import { focarPrimeiroErro } from '../foco'
import type { Projeto } from '../tipos'

// Sem `projeto` o formulário cadastra; com `projeto` ele edita.
const props = defineProps<{ projeto?: Projeto; enviando?: boolean }>()
const emit = defineEmits<{ salvar: [dados: NovoProjeto]; cancelar: [] }>()

const formulario = useTemplateRef<HTMLFormElement>('formulario')

const form = reactive({
  nome: props.projeto?.nome ?? '',
  descricao: props.projeto?.descricao ?? '',
  disciplina: props.projeto?.disciplina ?? '',
})

const erros = reactive({ nome: '', disciplina: '' })

function validar() {
  erros.nome = form.nome.trim() ? '' : 'Informe o nome do projeto.'
  erros.disciplina = form.disciplina.trim() ? '' : 'Informe a disciplina.'
  return !Object.values(erros).some(Boolean)
}

function enviar() {
  if (!validar()) {
    focarPrimeiroErro(formulario.value)
    return
  }
  emit('salvar', {
    nome: form.nome.trim(),
    descricao: form.descricao.trim(),
    disciplina: form.disciplina.trim(),
    criadoEm: props.projeto?.criadoEm ?? new Date().toISOString().slice(0, 10),
  })
}
</script>

<template>
  <form ref="formulario" class="task-form" novalidate @submit.prevent="enviar">
    <div class="form-section-title">
      <span class="form-section-icon" aria-hidden="true">✎</span>
      <div>
        <h2>Informações do projeto</h2>
        <p>Campos marcados com * são obrigatórios.</p>
      </div>
    </div>

    <div class="form-field">
      <label for="nome">Nome do projeto <span aria-hidden="true">*</span></label>
      <input
        id="nome"
        v-model="form.nome"
        type="text"
        maxlength="120"
        placeholder="Ex.: Gerenciador de Tarefas"
        required
        :aria-invalid="!!erros.nome"
        :aria-describedby="erros.nome ? 'erro-nome' : undefined"
      />
      <small v-if="erros.nome" id="erro-nome" class="field-error">⚠ Erro: {{ erros.nome }}</small>
    </div>

    <div class="form-field">
      <label for="disciplina">Disciplina <span aria-hidden="true">*</span></label>
      <input
        id="disciplina"
        v-model="form.disciplina"
        type="text"
        maxlength="120"
        placeholder="Ex.: Desenvolvimento Frontend"
        required
        :aria-invalid="!!erros.disciplina"
        :aria-describedby="erros.disciplina ? 'erro-disciplina' : undefined"
      />
      <small v-if="erros.disciplina" id="erro-disciplina" class="field-error">
        ⚠ Erro: {{ erros.disciplina }}
      </small>
    </div>

    <div class="form-field">
      <label for="descricao-projeto">Descrição</label>
      <textarea
        id="descricao-projeto"
        v-model="form.descricao"
        rows="4"
        placeholder="Descreva o objetivo do projeto..."
      ></textarea>
    </div>

    <div class="form-actions">
      <button type="button" class="secondary-button" @click="emit('cancelar')">Cancelar</button>
      <button type="submit" class="primary-button" :disabled="enviando">
        {{ enviando ? 'Salvando...' : projeto ? '✓ Salvar alterações' : '✓ Salvar projeto' }}
      </button>
    </div>
  </form>
</template>
