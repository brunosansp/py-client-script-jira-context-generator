# Exemplo de Uso: Jira Context Generator

Este documento mostra na prática como usar o Jira Context Generator para extrair informações de tasks do Jira e criar specs no Kiro.

## Exemplo Real: PRIC-600

### Passo 1: Extrair Contexto do Jira

Primeiro, ative o ambiente virtual e execute o script:

```bash
cd py-client-script-jira-context-generator
source venv/bin/activate
python jira_context_generator.py PRIC-600
```

Ou use o wrapper (mais fácil):

```bash
./jira-context PRIC-600
```

**Saída esperada:**

```
Buscando informações da task: PRIC-600...

✓ Contexto gerado com sucesso!
✓ Arquivo salvo: PRIC-600_context.md
✓ Link: https://empresa.atlassian.net/browse/PRIC-600
```

### Passo 2: Ver o Contexto Gerado

O arquivo `PRIC-600_context.md` foi criado com todas as informações da task:

```bash
cat PRIC-600_context.md
```

**Conteúdo do arquivo:**

**Metadados estruturados:**

```yaml
---
jira_key: PRIC-600
title: Guard rails para transferencias internacionais
type: História
status: Em Refinamento
priority: Medium
project: PRIC
---
```

**Informações extraídas automaticamente:**

- ✅ Título e descrição da task
- ✅ Status, prioridade, assignee
- ✅ Critérios de aceitação
- ✅ Regras de negócio
- ✅ Subtasks (se houver)
- ✅ Comentários recentes
- ✅ Issues relacionadas
- ✅ Link direto para o Jira

### Passo 3: Usar no Kiro AI

Agora você pode usar esse contexto no Kiro de duas formas:

#### Forma 1: Referenciar o arquivo (recomendado)

No chat do Kiro, digite:

```
#PRIC-600_context.md

Crie um spec para implementar esta funcionalidade
```

O Kiro vai ler o arquivo automaticamente e criar o spec baseado nas informações.

#### Forma 2: Pedir análise específica

```
Analise os critérios de aceitação em #PRIC-600_context.md e sugira
uma arquitetura para implementar
```

### Passo 4: O Kiro Cria o Spec

O Kiro vai perguntar como você quer começar:

- **Requirements** (requisitos primeiro)
- **Technical Design** (design técnico primeiro)

Depois, ele cria automaticamente 3 arquivos:

1. **requirements.md** - O que precisa ser feito
2. **design.md** - Como será implementado
3. **tasks.md** - Lista de tarefas para executar

Exemplo de estrutura criada:

```
.kiro/specs/guard-rails-internacional/
├── requirements.md
├── design.md
└── tasks.md
```

## Exemplo Prático Completo

### Cenário: Você recebeu a task PRIC-600 para implementar

**1. Extrair contexto:**

```bash
cd py-client-script-jira-context-generator
./jira-context PRIC-600
```

**2. Abrir o Kiro e digitar:**

```
#PRIC-600_context.md

Crie um spec para esta task
```

**3. O Kiro pergunta:**

```
What do you want to start with?
- Requirements
- Technical Design
```

**4. Você escolhe "Requirements"**

**5. O Kiro cria os documentos automaticamente**

**6. Você revisa e aprova**

**7. Pronto! Agora você tem um plano completo para implementar**

## Por Que Isso é Útil?

### Antes (processo manual)

1. Abrir task no Jira
2. Ler e entender tudo
3. Copiar informações importantes
4. Criar documentação manualmente
5. Planejar implementação
6. Criar lista de tarefas

⏱️ **Tempo: 2-4 horas**

### Depois (com automação)

1. `./jira-context PRIC-600`
2. No Kiro: `#PRIC-600_context.md` + "Crie um spec"
3. Revisar e aprovar

⏱️ **Tempo: 5-10 minutos**

## Casos de Uso Comuns

### Trabalhar com múltiplas tasks relacionadas

```bash
# Gerar contexto de várias tasks
./jira-context PRIC-600
./jira-context PRIC-601
./jira-context PRIC-602

# No Kiro
"Crie um spec que integre as funcionalidades de
#PRIC-600_context.md, #PRIC-601_context.md e #PRIC-602_context.md"
```

### Atualizar spec existente

```bash
# Gerar contexto atualizado da task
./jira-context PRIC-600

# No Kiro
"Atualize o spec em .kiro/specs/guard-rails-internacional/
com as novas informações de #PRIC-600_context.md"
```

### Analisar impacto antes de implementar

```bash
# No Kiro
"Analise o impacto da implementação descrita em #PRIC-600_context.md
no código existente em src/"
```

## Dicas Rápidas

### 1. Atalho para facilitar

Torne o comando mais fácil de usar:

```bash
chmod +x jira-context
```

Agora você pode usar:

```bash
./jira-context PRIC-600
```

### 2. Ver o conteúdo gerado

```bash
cat PRIC-600_context.md
```

Ou abra no editor do Kiro para visualizar formatado.

### 3. Organizar arquivos gerados

Os arquivos `*_context.md` ficam no diretório `py-client-script-jira-context-generator/`. Você pode movê-los ou referenciá-los diretamente no Kiro.

## Problemas Comuns

### "Biblioteca 'jira' não encontrada"

Você esqueceu de ativar o venv:

```bash
cd py-client-script-jira-context-generator
source venv/bin/activate
pip install jira python-dotenv
```

### "Configurações do Jira não encontradas"

Você precisa configurar as credenciais primeiro. Execute:

```bash
./setup_jira.sh
```

### Contexto muito grande

Se o arquivo gerado for muito extenso, peça ao Kiro para resumir:

```
Resuma os pontos principais de #PRIC-600_context.md focando em:
- Critérios de aceitação
- Regras de negócio críticas
```

## Próximos Passos

1. ✅ Configure suas credenciais do Jira (se ainda não fez)
2. ✅ Teste com uma task real do seu projeto
3. ✅ Experimente criar um spec com o Kiro
4. ✅ Compartilhe com seu time

---

**Mais informações:**

- `README.md` - Guia rápido de instalação
- `GUIA_JIRA_CONTEXT.md` - Documentação completa
