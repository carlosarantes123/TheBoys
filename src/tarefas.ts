import type { Tarefa } from './tipos'

// Troca a tarefa pelo objeto devolvido pela API. Quem busca os dados é o dono
// da lista: o cartão só avisa que a tarefa mudou (o dado desce, o aviso sobe).
export function substituirTarefa(tarefas: Tarefa[], nova: Tarefa) {
  const indice = tarefas.findIndex((tarefa) => tarefa.id === nova.id)
  if (indice !== -1) tarefas[indice] = nova
}
