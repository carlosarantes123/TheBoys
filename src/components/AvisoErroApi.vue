<script setup lang="ts">
// Aviso mostrado quando a API falha ao carregar os dados, com a opção de tentar de novo.
import { computed, onMounted, ref } from 'vue'
import { ErroApi, ErroSemConexao } from '../api'

const props = defineProps<{ erro: Error; tentativas: number }>()
const emit = defineEmits<{ tentarDeNovo: [] }>()

const botao = ref<HTMLButtonElement | null>(null)

const aviso = computed(() => {
  if (props.erro instanceof ErroSemConexao) {
    return {
      titulo: 'Sem conexão com a API',
      detalhe:
        'O servidor não respondeu. Verifique se o json-server está rodando (npx json-server db.json) e tente de novo.',
    }
  }
  if (props.erro instanceof ErroApi && props.erro.status >= 500) {
    return {
      titulo: 'A API está com problemas',
      detalhe: `O servidor respondeu com erro (${props.erro.status}). Aguarde um instante e tente de novo.`,
    }
  }
  return {
    titulo: 'Não foi possível carregar os dados',
    detalhe: 'Algo deu errado ao buscar as informações. Tente de novo.',
  }
})

// Ao clicar em "Tentar de novo" o botão some (vira o carregamento). Se falhar outra vez,
// o foco volta para ele, para quem usa teclado não ficar perdido no topo da página.
onMounted(() => {
  if (props.tentativas > 0) botao.value?.focus()
})
</script>

<template>
  <div class="erro-api" role="alert">
    <span class="erro-api-icone" aria-hidden="true">!</span>
    <div>
      <p class="erro-api-titulo">{{ aviso.titulo }}</p>
      <p class="erro-api-detalhe">{{ aviso.detalhe }}</p>
      <p v-if="tentativas > 0" class="erro-api-tentativas">
        Ainda sem sucesso depois de {{ tentativas }} {{ tentativas === 1 ? 'nova tentativa' : 'novas tentativas' }}.
      </p>
      <button ref="botao" type="button" class="primary-button" @click="emit('tentarDeNovo')">
        Tentar de novo
      </button>
    </div>
  </div>
</template>

<style scoped>
.erro-api {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  max-width: 620px;
  padding: 18px 20px;
  border: 1px solid #f6c9cf;
  border-radius: 10px;
  color: #6b1420;
  background: #fff0f1;
}

.erro-api-icone {
  display: grid;
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  place-items: center;
  border-radius: 50%;
  color: #fff;
  background: #b42336;
  font-weight: 800;
}

.erro-api p {
  margin: 0 0 6px;
  font-size: 13px;
  line-height: 1.5;
}

.erro-api .erro-api-titulo {
  color: #b42336;
  font-size: 15px;
  font-weight: 700;
}

.erro-api .erro-api-tentativas {
  font-weight: 600;
}

.erro-api button {
  margin-top: 8px;
}
</style>
