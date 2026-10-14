import { createRouter, createWebHistory } from 'vue-router'
import ListaTarefas from './views/ListaTarefas.vue'
import DetalheTarefa from './views/DetalheTarefa.vue'
import ListaProjetos from './views/ListaProjetos.vue'
import PaginaProjeto from './views/PaginaProjeto.vue'
import NaoEncontrada from './views/NaoEncontrada.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: ListaTarefas },
    { path: '/tarefas/:id', component: DetalheTarefa },
    { path: '/projetos', component: ListaProjetos },
    { path: '/projetos/:id', component: PaginaProjeto },
    { path: '/:rota(.*)*', component: NaoEncontrada },
  ],
})
