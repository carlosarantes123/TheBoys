# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).


### 1. Inicie a API local

Em um terminal, execute:

```bash
npx json-server db.json --port 3000
```

A API ficará disponível em `http://localhost:3000`.

### 2. Inicie o frontend

Em outro terminal, execute:

```bash
npm run dev
```

Abra no navegador o endereço exibido pelo Vite, normalmente `http://localhost:5173`.

## API local

O arquivo `db.json` funciona como banco de dados da aplicação e expõe os seguintes recursos:

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/projetos` | Lista os projetos |
| `GET` | `/projetos/:id` | Retorna um projeto |
| `POST` | `/projetos` | Cria um projeto |
| `GET` | `/tarefas` | Lista as tarefas |
| `GET` | `/tarefas/:id` | Retorna uma tarefa |
| `POST` | `/tarefas` | Cria uma tarefa |
| `PATCH` | `/tarefas/:id` | Atualiza parte de uma tarefa |
| `DELETE` | `/tarefas/:id` | Remove uma tarefa |

Para listar apenas as tarefas de um projeto, use o filtro `projetoId`:

```text
GET http://localhost:3000/tarefas?projetoId=1
```

O arquivo `db.seed.json` preserva uma cópia dos dados iniciais e pode ser usado para restaurar o conteúdo de `db.json` durante o desenvolvimento.

## Modelo de dados

Cada projeto possui nome, descrição, disciplina e data de criação. As tarefas são associadas a um projeto por `projetoId` e incluem título, descrição, responsável, prazo, prioridade e status.

Status aceitos:

- `a-fazer`;
- `em-andamento`;
- `em-revisao`;
- `concluida`.

Prioridades aceitas: `baixa`, `media` e `alta`.

Os contratos TypeScript correspondentes estão definidos em `src/tipos.ts`.

## Scripts

| Comando | Descrição |
| --- | --- |
| `npm run dev` | Inicia o servidor de desenvolvimento |
| `npm run build` | Valida os tipos e gera a versão de produção em `dist/` |
| `npm run preview` | Executa localmente a versão gerada pelo build |

## Estrutura do projeto

```text
.
├── public/             # Arquivos estáticos
├── src/
│   ├── assets/         # Imagens e recursos visuais
│   ├── components/     # Componentes Vue
│   ├── App.vue         # Componente raiz
│   ├── main.ts         # Ponto de entrada da aplicação
│   ├── style.css       # Estilos globais
│   └── tipos.ts        # Tipos do domínio
├── db.json            # Dados utilizados pela API local
├── db.seed.json       # Cópia dos dados iniciais
├── package.json       # Dependências e scripts
└── vite.config.ts     # Configuração do Vite
```

## Fluxo de desenvolvimento

1. Crie uma branch para a sua tarefa.
2. Faça alterações pequenas e focadas.
3. Execute `npm run build` antes de enviar as mudanças.
4. Abra um pull request descrevendo o que foi implementado e como testar.

## Licença

Este repositório ainda não possui uma licença definida.
