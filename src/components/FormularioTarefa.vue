<script setup lang="ts">
import { reactive } from 'vue'
import { listarProjetos } from '../api'
import CarregaDados from './CarregaDados.vue'
import { rotuloPrioridade, rotuloStatus } from '../rotulos'
import type { NovaTarefa, Prioridade, Status, Tarefa } from '../tipos'

// Sem `tarefa` o formulário cadastra; com `tarefa` ele edita.
const props = defineProps<{ tarefa?: Tarefa; enviando?: boolean }>()
const emit = defineEmits<{ salvar: [dados: NovaTarefa]; cancelar: [] }>()

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

const erros = reactive({ titulo: '', projetoId: '', responsavel: '', prazo: '' })

function validar() {
  erros.titulo = form.titulo.trim() ? '' : 'Informe o título da tarefa.'
  erros.projetoId = form.projetoId ? '' : 'Selecione um projeto.'
  erros.responsavel = form.responsavel.trim() ? '' : 'Informe o responsável.'
  erros.prazo = form.prazo ? '' : 'Informe o prazo.'
  return !Object.values(erros).some(Boolean)
}

function enviar() {
  if (!validar()) return
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
    <form class="task-form" novalidate @submit.prevent="enviar">
      <div class="form-section-title">
        <span class="form-section-icon">✎</span>
        <div>
          <h2>Informações da tarefa</h2>
          <p>Descreva o que precisa ser realizado.</p>
        </div>
      </div>

      <div class="form-field">
        <label for="titulo">Título da tarefa <span>*</span></label>
        <input
          id="titulo"
          v-model="form.titulo"
          type="text"
          maxlength="120"
          placeholder="Ex.: Desenvolver a tela de login"
          required
          :aria-invalid="!!erros.titulo"
          aria-describedby="erro-titulo"
        />
        <small v-if="erros.titulo" id="erro-titulo">{{ erros.titulo }}</small>
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
        <label for="projeto">Projeto <span>*</span></label>
        <select
          id="projeto"
          v-model="form.projetoId"
          required
          :aria-invalid="!!erros.projetoId"
          aria-describedby="erro-projeto"
        >
          <option value="" disabled>Selecione um projeto</option>
          <option v-for="projeto in projetos" :key="projeto.id" :value="projeto.id">
            {{ projeto.nome }} — {{ projeto.disciplina }}
          </option>
        </select>
        <small v-if="projetos.length === 0">Nenhum projeto encontrado. Confira a API.</small>
        <small v-if="erros.projetoId" id="erro-projeto">{{ erros.projetoId }}</small>
      </div>

      <div class="form-row">
        <div class="form-field">
          <label for="responsavel">Responsável <span>*</span></label>
          <input
            id="responsavel"
            v-model="form.responsavel"
            type="text"
            placeholder="Nome do responsável"
            required
            :aria-invalid="!!erros.responsavel"
            aria-describedby="erro-responsavel"
          />
          <small v-if="erros.responsavel" id="erro-responsavel">{{ erros.responsavel }}</small>
        </div>

        <div class="form-field">
          <label for="prazo">Prazo <span>*</span></label>
          <input
            id="prazo"
            v-model="form.prazo"
            type="date"
            required
            :aria-invalid="!!erros.prazo"
            aria-describedby="erro-prazo"
          />
          <small v-if="erros.prazo" id="erro-prazo">{{ erros.prazo }}</small>
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
