import { nextTick, ref } from 'vue'

// Dois universos para o mesmo app: o claro é o de herói; o escuro, o de vilão.
export type Tema = 'heroi' | 'vilao'

const CHAVE = 'theboys-tema'

function temaInicial(): Tema {
  try {
    const salvo = localStorage.getItem(CHAVE)
    if (salvo === 'heroi' || salvo === 'vilao') return salvo
  } catch {
    // Armazenamento bloqueado (janela privada, por exemplo): segue a preferência do sistema.
  }
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'vilao' : 'heroi'
}

export const tema = ref<Tema>(temaInicial())

function aplicar(valor: Tema) {
  document.documentElement.dataset.tema = valor
  const cor = valor === 'heroi' ? '#1f4fd8' : '#0a0818'
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', cor)
}

aplicar(tema.value)

// A troca é um corte diagonal na tela (View Transitions). Sem suporte, ou com
// "reduzir movimento" ligado, a troca é imediata.
export function escolherTema(novo: Tema) {
  if (novo === tema.value) return

  const trocar = async () => {
    tema.value = novo
    aplicar(novo)
    try {
      localStorage.setItem(CHAVE, novo)
    } catch {
      // Sem armazenamento, a escolha vale só nesta visita.
    }
    await nextTick()
  }

  const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!document.startViewTransition || reduzMovimento) {
    trocar()
    return
  }

  document.documentElement.dataset.transicao = novo
  document
    .startViewTransition(trocar)
    .finished.finally(() => delete document.documentElement.dataset.transicao)
}
