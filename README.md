# TheBoys · Gerenciador de Tarefas Acadêmicas

Projeto em equipe da disciplina **Desenvolvimento Frontend — 2026.2**: uma aplicação para organizar as tarefas dos projetos acadêmicos, com lista de tarefas, páginas de projeto, cadastro, edição e exclusão, busca, filtros e visão de quadro.

## Aplicação publicada

- **Site:** _(link do Static Site no Render — a preencher)_
- **API:** <https://theboys-api-d12x.onrender.com> (ex.: [`/tarefas`](https://theboys-api-d12x.onrender.com/tarefas))

Os dois ficam no [Render](https://render.com), no plano gratuito:

- A **API** é um *Web Service* que roda o mesmo `json-server` e o mesmo `db.json` do repositório (Build Command `npm ci`, Start Command `npm run api`). Ela dorme após uns 15 minutos sem uso, e o primeiro acesso depois disso leva cerca de 50 segundos: abra o site um pouco antes de apresentar. Quando o serviço reinicia ou é publicado de novo, os dados voltam ao `db.json` do GitHub.
- O **site** é um *Static Site* (Build Command `npm ci && npm run build`, Publish Directory `dist`) com a regra de reescrita `/*` → `/index.html` (Rewrite), para que as rotas internas, como `/tarefas/2`, abram direto e no recarregar.
- O endereço da API vem da variável `VITE_API_URL`: `.env.development` aponta para `http://localhost:3000` (`npm run dev`) e `.env.production` para a API no Render (`npm run build`).

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
- **Google Fonts** (Kanit e Pirata One), carregadas pelo `index.html`: é o único recurso externo do projeto; sem internet, o navegador usa uma fonte parecida

## Como rodar o projeto

Pré-requisito: **Node.js 22.12 ou superior** (`node -v`), o mínimo exigido pelo json-server e pelo Vite. Testado com o Node 22.20.

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

A API local responde rápido demais para ver o indicador de carregamento. Para simular uma rede lenta, defina um atraso em milissegundos ao iniciar a aplicação:

```bash
VITE_ATRASO_API=1500 npm run dev
```

No PowerShell (Windows): `$env:VITE_ATRASO_API=1500; npm run dev`.

Se a API falhar ao carregar uma tela, aparece um aviso explicando o problema e o botão **Tentar de novo**, que refaz a busca sem recarregar a página. Para ver o aviso, pare o json-server (Ctrl+C no terminal 1) e abra qualquer tela. Depois suba o json-server de novo e clique em **Tentar de novo**. O aviso distingue:

- **Sem conexão com a API**: o servidor não respondeu (json-server parado ou endereço errado);
- **A API está com problemas**: o servidor respondeu com erro 5xx;
- qualquer outra falha, com uma mensagem genérica.

## Tema: Herói e Vilão

O aplicativo tem dois temas: o claro é o **Herói** (estilo gibi, com retícula de meio-tom, legendas e botões em paralelogramo) e o escuro é o **Vilão** (noite índigo, painéis de cantos cortados e títulos góticos). O botão **Herói | Vilão** no topo troca o tema com um corte diagonal na tela.

- Na primeira visita, o tema segue a preferência do sistema (claro = Herói, escuro = Vilão). A escolha fica salva no navegador (`localStorage`, chave `theboys-tema`).
- Com "reduzir movimento" ligado no sistema, a troca é imediata, sem o corte.
- O visual fica em `src/tema.css`, carregado depois do `src/style.css`, e a troca em `src/tema.ts`.

## Arrastar cartões no quadro (desafio opcional)

No **Quadro**, arraste um cartão para outra etapa. No tema Herói, um herói voa atrás do cartão e o empurra; no tema Vilão, uma figura de sobretudo vai à frente e o puxa com tentáculos. O personagem troca de lado conforme a direção do arraste.

- A gravação é pessimista: o cartão só pousa na coluna nova depois que a API confirma. Se a API falhar, ele volta e aparece um aviso.
- **Esc** cancela o arraste. Soltar na mesma coluna não grava nada.
- Funciona com mouse ou caneta, em telas a partir de 701 px. Em qualquer tela, o seletor de status do cartão faz a mesma mudança sem arrastar (teclado, leitor de tela e toque).
- Com "reduzir movimento" ligado no sistema, o arraste funciona sem personagem e sem animação.
- Os desenhos são SVGs gerados por `ferramentas/gerar_personagens.py` (precisa de Python 3; só para quem for mexer na arte): `python ferramentas/gerar_personagens.py`.

## Rotas da aplicação

| Rota | Tela |
| --- | --- |
| `/` | Lista de todas as tarefas |
| `/quadro` | Quadro Kanban, com resumo e busca |
| `/tarefas/nova` | Cadastro de tarefa |
| `/tarefas/:id` | Detalhe de uma tarefa |
| `/tarefas/:id/editar` | Edição de uma tarefa |
| `/projetos` | Lista de projetos |
| `/projetos/novo` | Cadastro de projeto |
| `/projetos/:id` | Página do projeto, com as tarefas dele |
| `/projetos/:id/editar` | Edição de um projeto |
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
| `PATCH` | `/tarefas/:id` | Muda só o status de uma tarefa |
| `DELETE` | `/tarefas/:id` | Exclui uma tarefa |
| `GET` | `/projetos` | Lista os projetos |
| `GET` | `/projetos/:id` | Retorna um projeto |
| `GET` | `/projetos/:id?_embed=tarefas` | Retorna um projeto com as tarefas dele |
| `POST` | `/projetos` | Cadastra um projeto |
| `PUT` | `/projetos/:id` | Atualiza um projeto |

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
| `npm run api` | Sobe o json-server aceitando conexões externas (usado pelo Render; a porta vem de `PORT`, padrão 3000) |

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
│   │   ├── AvisoErroApi.vue   # Mensagem de falha da API com o botão "Tentar de novo"
│   │   ├── IndicadorCarregamento.vue # Aviso com spinner e esqueleto da tela enquanto os dados não chegam
│   │   ├── FiltrosTarefas.vue # Seletores de status e prioridade das tarefas
│   │   └── FormularioTarefa.vue # Formulário de tarefa, usado para criar e editar
│   └── views/            # Telas ligadas às rotas
└── package.json
```

## Organização da equipe

As tarefas estão no [quadro do GitHub Projects](https://github.com/users/carlosarantes123/projects/1), com um milestone por marco e cada issue com responsável. Cada integrante trabalha em uma branch e abre um pull request para a `main`.
