import { createRouter, createWebHistory } from 'vue-router'
import ListaTarefas from './views/ListaTarefas.vue'
import QuadroTarefas from './views/QuadroTarefas.vue'
import NovaTarefa from './views/NovaTarefa.vue'
import EditarTarefa from './views/EditarTarefa.vue'
import DetalheTarefa from './views/DetalheTarefa.vue'
import ListaProjetos from './views/ListaProjetos.vue'
import PaginaProjeto from './views/PaginaProjeto.vue'
import NaoEncontrada from './views/NaoEncontrada.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: ListaTarefas, meta: { titulo: 'Tarefas' } },
    { path: '/quadro', component: QuadroTarefas, meta: { titulo: 'Meu quadro' } },
    { path: '/tarefas/nova', component: NovaTarefa, meta: { titulo: 'Nova tarefa' } },
    { path: '/tarefas/:id', component: DetalheTarefa, meta: { titulo: 'Tarefa' } },
    { path: '/tarefas/:id/editar', component: EditarTarefa, meta: { titulo: 'Editar tarefa' } },
    { path: '/projetos', component: ListaProjetos, meta: { titulo: 'Projetos' } },
    { path: '/projetos/:id', component: PaginaProjeto, meta: { titulo: 'Projeto' } },
    { path: '/:rota(.*)*', component: NaoEncontrada, meta: { titulo: 'Não encontrada' } },
  ],
})
