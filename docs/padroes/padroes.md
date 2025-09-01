# Guia de Padrões de Contribuição para o Projeto

## Padrões de Branches
### Nomenclatura

Toda nova branch deve ser criada a partir da branch main e seguir o formato:

```bash
<tipo>/<descricao-curta>
```

- `<tipo>`: Indica a natureza do trabalho. Deve ser um dos seguintes:
    - feature: Para o desenvolvimento de novas funcionalidades.
    - fix: Para a correção de bugs.
    - chore: Para tarefas de manutenção, configuração ou outras atividades que não alteram o código da aplicação (ex: atualizar dependências).
    - docs: Para alterações na documentação.
    - refactor: Para refatoração de código sem alterar sua funcionalidade.

- `<descricao-curta>`: Um resumo do trabalho, em poucas palavras, usando kebab-case (palavras separadas por hífens). É uma boa prática incluir o número da Issue relacionada, se houver.

### Exemplos

```bash
# Adicionar login com Google (Issue #42)

> feature/42-login-com-google

# Corrigir erro de validação no formulário

> fix/erro-validacao-formulario

# Atualizar a versão do Docker

> chore/atualizar-versao-docker

# Adicionar documentação da API

> docs/documentacao-api-endpoints

# Refatorar o serviço de usuários

> refactor/servico-de-usuarios
```

### Fluxo de Trabalho

Sempre comece da main: Antes de criar sua branch, certifique-se de que sua main local está atualizada: `git checkout main && git pull`.

Crie sua branch: `git checkout -b <tipo>/<descricao-curta>`

> **NOTA:** a branch de trabalho deve ser excluída para manter o repositório limpo.

## Padrões de Commit

Nós utilizamos o padrão Conventional Commits.

### Estrutura do Commit

```bash
<tipo>(<escopo>): <descrição>
```

- `<tipo>`: Define a categoria do commit.

- `<escopo>`: (Opcional) Contexto da alteração (ex: api, login, database).

- `<descrição>`: Resumo conciso da alteração, em letra minúscula e no imperativo.

### Tipos de Commit

| Tipo     | Descrição                                                                 |
|----------|---------------------------------------------------------------------------|
| `feat`   | Adiciona uma nova funcionalidade.                                         |
| `fix`    | Corrige um bug.                                                           |
| `docs`   | Altera somente a documentação.                                            |
| `style`  | Altera formatação de código (espaços, ponto e vírgula, etc.).             |
| `refactor`| Refatora o código sem alterar a funcionalidade externa.                  |
| `perf`   | Melhora o desempenho do código.                                           |
| `test`   | Adiciona ou corrige testes.                                               |
| `chore`  | Atualiza tarefas de build, configuração, etc. (não mexe no código fonte). |
| `build`  | Altera o sistema de build ou dependências externas.                       |
| `ci`     | Altera arquivos de configuração de Integração Contínua (CI).              |

### Exemplos

```bash
feat(login): adicionar autenticação via email e senha

fix(api): corrigir cálculo de imposto no checkout

feat(profile): permitir que o usuário atualize sua foto
```

### Dicas e Boas Práticas

- **Commits Atômicos:** Faça commits pequenos e focados em uma única coisa. É mais fácil de revisar e, se necessário, de reverter.
- **Use o Imperativo:** Escreva a descrição como se estivesse dando uma ordem. "adicionar" ao invés de "adicionado". "corrigir" ao invés de "corrigido".
- **Não use ponto final na descrição.**

##  Padrões de Issue

As Issues são o centro do nosso trabalho. 
Elas registram bugs, novas ideias e tarefas. 
Usar templates garante que tenhamos todas as informações necessárias desde o início.

### Elementos de uma Boa Issue

- **Título Claro e Direto:** Use os prefixos [BUG], [FEAT] ou [TASK] para identificar rapidamente o tipo de issue.
- **Descrição Detalhada:** Siga o template correspondente para fornecer todo o contexto necessário.
- **Labels (Etiquetas):** Use labels para categorizar (bug, feature, documentation), priorizar (high-priority) ou sinalizar o esforço (good first issue).
- **Assignees (Responsáveis):** Atribua a issue a quem irá trabalhar nela.

### Nossos Templates

#### Bug Report

- **Finalidade:** Para relatar qualquer comportamento inesperado ou erro no sistema.
- **Campos Principais:**
  - **Descrição do Bug:** Um resumo claro e conciso do que está acontecendo.
  - **Comportamento Esperado:** O que deveria ter acontecido.

#### Feature Request (Solicitação de Funcionalidade)

- **Finalidade:** Para propor uma nova funcionalidade ou melhoria.
- **Campos Principais:**
  - **Qual item do backlog está relacionado?** Descreva o cenário ou a dor do usuário que motiva esta nova funcionalidade.
  - **Descreva a feature:** Descreva a solução proposta, detalhe como a nova funcionalidade deve se comportar.

#### Tarefa Geral (Task / Chore)

- **Finalidade:** Para tarefas que não são bugs nem features (ex: "Configurar o linter", "Modelar o banco de dados").
- **Campos Principais:**
  - **Qual o objetivo dessa task?** O que se espera alcançar com a conclusão da tarefa.
  - **O que deve ser feito?** Descreva as etapas necessárias para concluir a tarefa.
