import { nextTick, reactive, shallowRef } from 'vue'
import type { Status } from './tipos'

// Arrastar um cartão do quadro para outra coluna (desafio opcional, issue 46).
//
// Usa Pointer Events em vez do arraste nativo do HTML: assim o cartão "voando"
// pode ser desenhado por nós, com o personagem do tema acompanhando.
// A gravação é pessimista, como o resto do app: o cartão só pousa na coluna nova
// depois que a API confirma; se falhar, ele volta para onde estava.
// O seletor de status continua no cartão como alternativa sem arraste
// (teclado, leitor de tela, toque), por isso o arraste só liga com mouse ou caneta.

export type FaseArraste = 'parado' | 'arrastando' | 'gravando' | 'entregando' | 'voltando' | 'saindo'

export interface EstadoArraste {
  fase: FaseArraste
  tarefaId: string
  titulo: string
  statusOrigem: Status | ''
  statusAlvo: Status | ''
  // canto superior esquerdo do cartão que voa, em coordenadas da janela
  x: number
  y: number
  largura: number
  // 1 = indo para a direita; -1 = para a esquerda. O personagem troca de lado.
  direcao: 1 | -1
  inclinacao: number
  // em milissegundos; 0 = segue o ponteiro sem transição
  duracao: number
}

// Devolve true se a API gravou o novo status.
export type MoverTarefa = (tarefaId: string, status: Status) => Promise<boolean>

const LIMIAR_PX = 6
const INTERATIVOS = 'a, button, select, input, textarea, label'

function esperar(ms: number) {
  return new Promise((resolver) => setTimeout(resolver, ms))
}

function reduzMovimento() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export function useArraste() {
  const estado = reactive<EstadoArraste>({
    fase: 'parado',
    tarefaId: '',
    titulo: '',
    statusOrigem: '',
    statusAlvo: '',
    x: 0,
    y: 0,
    largura: 0,
    direcao: 1,
    inclinacao: 0,
    duracao: 0,
  })
  // cópia visual do cartão que acompanha o ponteiro
  const clone = shallowRef<HTMLElement | null>(null)

  let cartao: HTMLElement | null = null
  let quadro: HTMLElement | null = null
  let colunaAlvo: HTMLElement | null = null
  let mover: MoverTarefa | null = null
  let inicio = { x: 0, y: 0 }
  let deslocamento = { x: 0, y: 0 }
  let ultimoX = 0
  let velocidade = 0
  // cada arraste ganha um número; um fim atrasado de arraste antigo não mexe no novo
  let geracao = 0

  function marcarColuna(coluna: HTMLElement | null) {
    if (coluna === colunaAlvo) return
    colunaAlvo?.classList.remove('coluna-alvo')
    colunaAlvo = coluna
    colunaAlvo?.classList.add('coluna-alvo')
  }

  function limparOuvintes() {
    window.removeEventListener('pointermove', aoMover)
    window.removeEventListener('pointerup', aoSoltar)
    window.removeEventListener('pointercancel', aoCancelar)
    window.removeEventListener('keydown', aoTeclar)
  }

  function reiniciar() {
    marcarColuna(null)
    cartao?.classList.remove('origem-arraste')
    quadro?.classList.remove('com-arraste')
    document.body.classList.remove('arrastando-cartao')
    cartao = null
    quadro = null
    mover = null
    clone.value = null
    Object.assign(estado, { fase: 'parado', tarefaId: '', titulo: '', statusOrigem: '', statusAlvo: '', duracao: 0, inclinacao: 0 })
  }

  // Chamado no pointerdown do quadro. Só começa de fato depois de mover alguns pixels,
  // para não atrapalhar quem só quer clicar ou selecionar texto.
  function iniciar(evento: PointerEvent, aoMoverTarefa: MoverTarefa) {
    // se o personagem ainda está saindo de cena, encerra a saída e deixa arrastar de novo
    if (estado.fase === 'saindo') reiniciar()
    geracao++
    if (estado.fase !== 'parado' || evento.button !== 0 || !evento.isPrimary) return
    if (!window.matchMedia('(min-width: 701px) and (pointer: fine)').matches) return
    const alvo = evento.target as HTMLElement
    if (alvo.closest(INTERATIVOS)) return
    const encontrado = alvo.closest<HTMLElement>('.task-card[data-tarefa-id]')
    if (!encontrado) return

    cartao = encontrado
    quadro = encontrado.closest<HTMLElement>('.kanban-board')
    mover = aoMoverTarefa
    inicio = { x: evento.clientX, y: evento.clientY }
    ultimoX = evento.clientX
    velocidade = 0
    window.addEventListener('pointermove', aoMover)
    window.addEventListener('pointerup', aoSoltar)
    window.addEventListener('pointercancel', aoCancelar)
    window.addEventListener('keydown', aoTeclar)
  }

  function comecar(evento: PointerEvent) {
    if (!cartao) return
    const rect = cartao.getBoundingClientRect()
    deslocamento = { x: evento.clientX - rect.left, y: evento.clientY - rect.top }

    const copia = cartao.cloneNode(true) as HTMLElement
    copia.removeAttribute('data-tarefa-id')
    copia.classList.add('cartao-voando')
    copia.style.width = `${rect.width}px`
    clone.value = copia

    Object.assign(estado, {
      fase: 'arrastando',
      tarefaId: cartao.dataset.tarefaId ?? '',
      titulo: cartao.dataset.titulo ?? '',
      statusOrigem: (cartao.closest<HTMLElement>('[data-status]')?.dataset.status ?? '') as Status,
      statusAlvo: '',
      x: rect.left,
      y: rect.top,
      largura: rect.width,
      inclinacao: 0,
      duracao: 0,
    })
    // o navegador pode ter começado a selecionar texto antes de o arraste valer
    window.getSelection()?.removeAllRanges()
    cartao.classList.add('origem-arraste')
    quadro?.classList.add('com-arraste')
    document.body.classList.add('arrastando-cartao')
  }

  function aoMover(evento: PointerEvent) {
    if (estado.fase === 'parado') {
      if (Math.hypot(evento.clientX - inicio.x, evento.clientY - inicio.y) < LIMIAR_PX) return
      comecar(evento)
    }
    if (estado.fase !== 'arrastando') return
    evento.preventDefault()

    estado.x = evento.clientX - deslocamento.x
    estado.y = evento.clientY - deslocamento.y

    // direção com um pouco de inércia, para o personagem não ficar trocando de lado à toa
    velocidade = velocidade * 0.75 + (evento.clientX - ultimoX) * 0.25
    ultimoX = evento.clientX
    if (velocidade > 1.5) estado.direcao = 1
    else if (velocidade < -1.5) estado.direcao = -1
    estado.inclinacao = Math.max(-7, Math.min(7, velocidade * 0.9))

    // coluna embaixo do ponteiro (o cartão que voa não recebe eventos, então não atrapalha)
    const coluna = document.elementFromPoint(evento.clientX, evento.clientY)?.closest<HTMLElement>('.kanban-column[data-status]') ?? null
    marcarColuna(coluna)
    estado.statusAlvo = (coluna?.dataset.status ?? '') as Status | ''

    // rolagem automática do quadro quando ele não cabe na tela
    if (quadro && quadro.scrollWidth > quadro.clientWidth) {
      const r = quadro.getBoundingClientRect()
      if (evento.clientX > r.right - 60) quadro.scrollLeft += 14
      else if (evento.clientX < r.left + 60) quadro.scrollLeft -= 14
    }
  }

  async function voar(destino: DOMRect | null, ms: number) {
    if (!destino) return
    const distancia = Math.hypot(destino.left - estado.x, destino.top - estado.y)
    if (Math.abs(destino.left - estado.x) > 4) estado.direcao = destino.left > estado.x ? 1 : -1
    estado.duracao = reduzMovimento() ? 0 : Math.round(Math.min(ms, Math.max(260, distancia / 1.6)))
    estado.inclinacao = 0
    estado.x = destino.left
    estado.y = destino.top
    await esperar(estado.duracao)
  }

  async function voltar() {
    const minha = geracao
    const origem = cartao
    estado.fase = 'voltando'
    await voar(origem?.getBoundingClientRect() ?? null, 450)
    if (minha === geracao) reiniciar()
  }

  async function aoSoltar() {
    limparOuvintes()
    if (estado.fase === 'parado') {
      reiniciar()
      return
    }
    if (estado.fase !== 'arrastando') return

    const minha = geracao
    const atual = () => minha === geracao
    const { tarefaId, statusOrigem, statusAlvo } = estado
    marcarColuna(null)
    if (!statusAlvo || statusAlvo === statusOrigem || !mover) {
      await voltar()
      return
    }

    // segura o cartão sobre a coluna enquanto a API responde
    estado.fase = 'gravando'
    const gravou = await mover(tarefaId, statusAlvo)
    if (!atual()) return
    if (!gravou) {
      await voltar()
      return
    }

    // a tela já mudou: o cartão de verdade está na coluna nova; voa até ele e pousa
    await nextTick()
    const destino = document.querySelector<HTMLElement>(`.task-card[data-tarefa-id="${CSS.escape(tarefaId)}"]`)
    destino?.classList.add('chegando')
    estado.fase = 'entregando'
    await voar(destino?.getBoundingClientRect() ?? null, 650)
    destino?.classList.remove('chegando')
    if (!atual()) return
    if (destino && !reduzMovimento()) {
      destino.classList.add('pousou')
      setTimeout(() => destino.classList.remove('pousou'), 600)
    }

    // o personagem vai embora (herói sai voando; vilão recolhe os tentáculos e some)
    clone.value = null
    estado.fase = 'saindo'
    await esperar(reduzMovimento() ? 0 : 600)
    if (atual()) reiniciar()
  }

  function aoCancelar() {
    limparOuvintes()
    if (estado.fase === 'arrastando') voltar()
    else reiniciar()
  }

  function aoTeclar(evento: KeyboardEvent) {
    if (evento.key === 'Escape') aoCancelar()
  }

  return { estado, clone, iniciar }
}
