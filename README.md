# TheBoys · Gerenciador de Tarefas Acadêmicas

Projeto em equipe da disciplina **Desenvolvimento Frontend — 2026.2**: uma aplicação para organizar as tarefas dos projetos acadêmicos, com lista de tarefas, páginas de projeto e, nos próximos marcos, cadastro, edição, filtros e visão de quadro.

## Equipe TheBoys

| Integrante | GitHub |
| --- | --- |
| Carlos Eduardo Arantes | [@carlosarantes123](https://github.com/carlosarantes123) |
| Igor Evangelista Cruz | [@igorCruz23](https://github.com/igorCruz23) |
| Heitor Mota da Cruz | [@heitorcruz-tech](https://github.com/heitorcruz-tech) |
| João Vitor Fernandes | — [@jvfernandessilva06-hash](https://github.com/jvfernandessilva06-hash)|

## Framework e tecnologias

- **Vue 3** com **TypeScript**, criado com o **Vite** (`npm create vite@latest`, template `vue-ts`)
- **Vue Router** para as rotas
- **json-server** como API local, a partir do `db.json`

## Como rodar o projeto

Pré-requisito: **Node.js 24 ou superior** (`node -v`).

```bash
git clone https://github.com/carlosarantes123/TheBoys.git
cd TheBoys
npm install
```

Depois, em **dois terminais** na raiz do projeto:

```bash
# terminal 1 — API local em http://localhost:3000
npx json-server db.json
```

```bash
# terminal 2 — aplicação em http://localhost:5173
npm run dev
```

Para voltar aos dados originais, copie o `db.seed.json` por cima do `db.json`.

## Rotas da aplicação

| Rota | Tela |
| --- | --- |
| `/` | Lista de todas as tarefas |
| `/quadro` | Quadro Kanban, com resumo e busca |
| `/tarefas/nova` | Cadastro de tarefa |
| `/tarefas/:id` | Detalhe de uma tarefa |
| `/tarefas/:id/editar` | Edição de uma tarefa |
| `/projetos` | Lista de projetos |
| `/projetos/:id` | Página do projeto, com as tarefas dele |
| `/busca` | Busca por título em tarefas e projetos (campo no topo da página), com filtros de status e prioridade nas tarefas |
| qualquer outra | Página não encontrada |

## API local

O `json-server` transforma cada chave do `db.json` em uma rota:

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/tarefas` | Lista as tarefas |
| `GET` | `/tarefas/:id` | Retorna uma tarefa |
| `POST` | `/tarefas` | Cadastra uma tarefa |
| `PUT` | `/tarefas/:id` | Atualiza uma tarefa |
| `GET` | `/projetos` | Lista os projetos |
| `GET` | `/projetos/:id?_embed=tarefas` | Retorna um projeto com as tarefas dele |

> **Atenção:** `GET /tarefas?projetoId=1` volta vazio, porque o json-server lê o `1` da URL como número e no `db.json` o `projetoId` é o texto `"1"`. Para as tarefas de um projeto, use o `_embed`.

## Contrato de dados

O formato de projetos e tarefas é o mesmo para toda a turma e não deve ser alterado:

- `db.json` — os dados; `db.seed.json` — cópia intacta para recomeçar do zero
- `src/tipos.ts` — os tipos `Projeto`, `Tarefa`, `NovaTarefa`, `Status` e `Prioridade`

Status aceitos: `a-fazer`, `em-andamento`, `em-revisao`, `concluida`.
Prioridades aceitas: `baixa`, `media`, `alta`.

## Scripts

| Comando | Descrição |
| --- | --- |
| `npm run dev` | Inicia o servidor de desenvolvimento |
| `npm run build` | Confere os tipos e gera a versão de produção em `dist/` |
| `npm run preview` | Serve localmente a versão gerada pelo build |

## Estrutura do projeto

```text
.
├── db.json               # Dados da API local
├── db.seed.json          # Cópia intacta dos dados iniciais
├── src/
│   ├── api.ts            # Funções tipadas de acesso à API
│   ├── filtros.ts        # Estado único da busca por título e dos filtros de status e prioridade
│   ├── router.ts         # Rotas da aplicação
│   ├── rotulos.ts        # Textos de status/prioridade e formatação de datas
│   ├── tipos.ts          # Contrato de dados
│   ├── App.vue           # Layout base: menu lateral, barra superior e rotas
│   ├── components/
│   │   ├── CartaoTarefa.vue   # Cartão de uma tarefa
│   │   ├── CarregaDados.vue   # Estados de carregando, erro e não encontrado
│   │   ├── FiltrosTarefas.vue # Seletores de status e prioridade das tarefas
│   │   └── FormularioTarefa.vue # Formulário de tarefa, usado para criar e editar
│   └── views/            # Telas ligadas às rotas
└── package.json
```

## Organização da equipe

As tarefas estão no [quadro do GitHub Projects](https://github.com/users/carlosarantes123/projects/1), com um milestone por marco e cada issue com responsável. Cada integrante trabalha em uma branch e abre um pull request para a `main`.
