<script setup lang="ts">
import { reactive, useTemplateRef } from 'vue'
import { listarProjetos } from '../api'
import CarregaDados from './CarregaDados.vue'
import { focarPrimeiroErro } from '../foco'
import { rotuloPrioridade, rotuloStatus } from '../rotulos'
import type { NovaTarefa, Prioridade, Status, Tarefa } from '../tipos'

// Sem `tarefa` o formulário cadastra; com `tarefa` ele edita.
const props = defineProps<{ tarefa?: Tarefa; enviando?: boolean; projetoIdInicial?: string }>()
const emit = defineEmits<{ salvar: [dados: NovaTarefa]; cancelar: [] }>()

const formulario = useTemplateRef<HTMLFormElement>('formulario')

const opcoesStatus = Object.entries(rotuloStatus) as [Status, string][]
const opcoesPrioridade = Object.entries(rotuloPrioridade) as [Prioridade, string][]

const form = reactive<NovaTarefa>({
  projetoId: props.tarefa?.projetoId ?? props.projetoIdInicial ?? '',
  titulo: props.tarefa?.titulo ?? '',
  descricao: props.tarefa?.descricao ?? '',
  status: props.tarefa?.status ?? 'a-fazer',
  prioridade: props.tarefa?.prioridade ?? 'media',
  responsavel: props.tarefa?.responsavel ?? '',
  prazo: props.tarefa?.prazo ?? '',
})

const erros = reactive({ titulo: '', projetoId: '', responsavel: '', prazo: '' })

function validar() {
  erros.titulo = form.titulo.trim() ? '' : 'Informe o título da tarefa.'
  erros.projetoId = form.projetoId ? '' : 'Selecione um projeto.'
  erros.responsavel = form.responsavel.trim() ? '' : 'Informe o responsável.'
  erros.prazo = form.prazo ? '' : 'Informe o prazo.'
  return !Object.values(erros).some(Boolean)
}

function enviar() {
  if (!validar()) {
    focarPrimeiroErro(formulario.value)
    return
  }
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
    <form ref="formulario" class="task-form" novalidate @submit.prevent="enviar">
      <div class="form-section-title">
        <span class="form-section-icon" aria-hidden="true">✎</span>
        <div>
          <h2>Informações da tarefa</h2>
          <p>Descreva o que precisa ser realizado.</p>
        </div>
      </div>

      <div class="form-field">
        <label for="titulo">Título da tarefa <span aria-hidden="true">*</span></label>
        <input
          id="titulo"
          v-model="form.titulo"
          type="text"
          maxlength="120"
          placeholder="Ex.: Desenvolver a tela de login"
          required
          :aria-invalid="!!erros.titulo"
          :aria-describedby="erros.titulo ? 'erro-titulo' : undefined"
        />
        <small v-if="erros.titulo" id="erro-titulo" class="field-error">⚠ Erro: {{ erros.titulo }}</small>
      </div>

      <div class="form-field">
        <label for="descricao">Descrição</label>
        <textarea
          id="descricao"
          v-model="form.descricao"
          rows="4"
          placeholder="Descreva os detalhes e objetivos da tarefa..."
        ></textarea>
      </div>

      <div class="form-field">
        <label for="projeto">Projeto <span aria-hidden="true">*</span></label>
        <select
          id="projeto"
          v-model="form.projetoId"
          required
          :aria-invalid="!!erros.projetoId"
          :aria-describedby="erros.projetoId ? 'erro-projeto' : undefined"
        >
          <option value="" disabled>Selecione um projeto</option>
          <option v-for="projeto in projetos" :key="projeto.id" :value="projeto.id">
            {{ projeto.nome }} — {{ projeto.disciplina }}
          </option>
        </select>
        <small v-if="projetos.length === 0">Nenhum projeto encontrado. Confira a API.</small>
        <small v-if="erros.projetoId" id="erro-projeto" class="field-error">⚠ Erro: {{ erros.projetoId }}</small>
      </div>

      <div class="form-row">
        <div class="form-field">
          <label for="responsavel">Responsável <span aria-hidden="true">*</span></label>
          <input
            id="responsavel"
            v-model="form.responsavel"
            type="text"
            placeholder="Nome do responsável"
            required
            :aria-invalid="!!erros.responsavel"
            :aria-describedby="erros.responsavel ? 'erro-responsavel' : undefined"
          />
          <small v-if="erros.responsavel" id="erro-responsavel" class="field-error">⚠ Erro: {{ erros.responsavel }}</small>
        </div>

        <div class="form-field">
          <label for="prazo">Prazo <span aria-hidden="true">*</span></label>
          <input
            id="prazo"
            v-model="form.prazo"
            type="date"
            required
            :aria-invalid="!!erros.prazo"
            :aria-describedby="erros.prazo ? 'erro-prazo' : undefined"
          />
          <small v-if="erros.prazo" id="erro-prazo" class="field-error">⚠ Erro: {{ erros.prazo }}</small>
        </div>
      </div>

      <div class="form-row">
        <div class="form-field">
          <label for="prioridade">Prioridade</label>
          <select id="prioridade" v-model="form.prioridade">
            <option v-for="[valor, rotulo] in opcoesPrioridade" :key="valor" :value="valor">
              {{ rotulo }}
            </option>
          </select>
        </div>

        <div class="form-field">
          <label for="status">{{ tarefa ? 'Status' : 'Status inicial' }}</label>
          <select id="status" v-model="form.status">
            <option v-for="[valor, rotulo] in opcoesStatus" :key="valor" :value="valor">
              {{ rotulo }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="secondary-button" @click="emit('cancelar')">Cancelar</button>
        <button type="submit" class="primary-button" :disabled="enviando">
          {{ enviando ? 'Salvando...' : tarefa ? '✓ Salvar alterações' : '✓ Salvar tarefa' }}
        </button>
      </div>
    </form>
  </CarregaDados>
</template>
