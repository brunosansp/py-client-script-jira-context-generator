# Guia de Configuração - Jira Context Generator

Este guia explica como configurar e usar o script `jira_context_generator.py` para buscar informações de tasks do Jira e gerar contexto para agentes de IA.

## Pré-requisitos

1. Python 3.6 ou superior instalado
2. Acesso ao Jira da sua empresa
3. Permissões para gerar API tokens no Jira

## Passo 1: Instalar Dependências

### Opção A: Usando ambiente virtual (recomendado)

```bash
cd py-client-script-jira-context-generator
python3 -m venv venv
source venv/bin/activate
pip install jira python-dotenv
```

### Opção B: Instalação global

```bash
pip3 install jira python-dotenv
```

**Nota**: Sempre que for usar o script, ative o ambiente virtual primeiro:

```bash
cd py-client-script-jira-context-generator
source venv/bin/activate
```

## Passo 2: Gerar Token de API do Jira

1. Acesse: https://id.atlassian.com/manage-profile/security/api-tokens
2. Faça login com sua conta Atlassian
3. Clique em **"Create API token"**
4. Dê um nome ao token (ex: "Kiro AI Context Generator")
5. Clique em **"Create"**
6. **IMPORTANTE**: Copie o token imediatamente (você não poderá vê-lo novamente)

## Passo 3: Configurar Variáveis de Ambiente

### Opção A: Configuração Temporária (válida apenas na sessão atual)

```bash
export JIRA_URL='https://sua-empresa.atlassian.net'
export JIRA_EMAIL='seu-email@empresa.com'
export JIRA_API_TOKEN='seu-token-aqui'
```

### Opção B: Configuração Permanente (recomendado)

Adicione as variáveis ao seu arquivo de configuração do shell:

**Para bash (~/.bashrc ou ~/.bash_profile):**

```bash
echo 'export JIRA_URL="https://sua-empresa.atlassian.net"' >> ~/.bashrc
echo 'export JIRA_EMAIL="seu-email@empresa.com"' >> ~/.bashrc
echo 'export JIRA_API_TOKEN="seu-token-aqui"' >> ~/.bashrc
source ~/.bashrc
```

**Para zsh (~/.zshrc):**

```bash
echo 'export JIRA_URL="https://sua-empresa.atlassian.net"' >> ~/.zshrc
echo 'export JIRA_EMAIL="seu-email@empresa.com"' >> ~/.zshrc
echo 'export JIRA_API_TOKEN="seu-token-aqui"' >> ~/.zshrc
source ~/.zshrc
```

### Opção C: Arquivo .env (mais seguro para projetos)

Crie um arquivo `.env` na raiz do projeto:

```bash
JIRA_URL=https://sua-empresa.atlassian.net
JIRA_EMAIL=seu-email@empresa.com
JIRA_API_TOKEN=seu-token-aqui
```

**IMPORTANTE**: Adicione `.env` ao `.gitignore` para não commitar credenciais!

```bash
# Adicione estas linhas ao seu .gitignore:
.env
venv/
*.pyc
__pycache__/
*_context.md
```

Ou execute:

```bash
cat >> .gitignore << 'EOF'

# Python
.env
venv/
*.pyc
__pycache__/
*_context.md
EOF
```

## Passo 4: Verificar Configuração

Teste se as variáveis estão configuradas:

```bash
echo $JIRA_URL
echo $JIRA_EMAIL
echo $JIRA_API_TOKEN
```

## Passo 5: Usar o Script

### Opção 1: Usando o wrapper (mais fácil)

```bash
chmod +x jira-context
./jira-context PRIC-337
```

### Opção 2: Ativando o venv manualmente

```bash
cd py-client-script-jira-context-generator
source venv/bin/activate
python jira_context_generator.py PRIC-337
```

Substitua `PRIC-337` pela chave da sua task no Jira (ex: `PROJ-456`, `DEV-789`).

### Exemplo de Saída

O script irá:

1. Conectar ao Jira
2. Buscar todas as informações da task
3. Gerar um arquivo `PRIC-337_context.md` com o contexto formatado
4. Exibir mensagem de sucesso no terminal

### Informações Extraídas

O script captura:

- ✓ Título e descrição da task
- ✓ Tipo, status e prioridade
- ✓ Reporter e assignee
- ✓ Critérios de aceitação
- ✓ Comentários (últimos 5)
- ✓ Subtasks
- ✓ Issues relacionadas
- ✓ Labels e componentes
- ✓ Link direto para a task

## Passo 6: Usar com Kiro AI

Após gerar o contexto, você pode:

1. **Referenciar o arquivo no Kiro:**
   No chat do Kiro, use: `#PRIC-337_context.md`

2. **Criar um spec baseado na task:**

   ```
   Crie um spec para implementar a task descrita em #PRIC-337_context.md
   ```

3. **Visualizar o conteúdo:**
   ```bash
   cat PRIC-337_context.md
   ```

## Troubleshooting

### Erro: "Biblioteca 'jira' não encontrada"

Ative o ambiente virtual e instale as dependências:

```bash
cd py-client-script-jira-context-generator
source venv/bin/activate
pip install jira python-dotenv
```

### Erro: "Configurações do Jira não encontradas"

Verifique se as variáveis de ambiente estão configuradas:

```bash
echo $JIRA_URL
```

### Erro: "Erro ao conectar ao Jira"

- Verifique se a URL está correta (deve incluir `https://`)
- Confirme que o email está correto
- Verifique se o token de API é válido
- Teste o acesso manual ao Jira no navegador

### Erro: "Erro ao buscar issue"

- Confirme que a chave da task está correta (ex: `PROJ-123`)
- Verifique se você tem permissão para acessar a task
- Confirme que a task existe no projeto

## Dicas de Uso

1. **Usar o wrapper para facilitar:**

   ```bash
   chmod +x jira-context
   ./jira-context PRIC-337
   ```

   O wrapper ativa o venv automaticamente.

2. **Processar múltiplas tasks:**

   ```bash
   source venv/bin/activate
   for task in PRIC-337 PRIC-338 PRIC-339; do
     python jira_context_generator.py $task
   done
   ```

3. **Integrar com workflow do Kiro:**
   Após gerar o contexto, referencie no chat: `#PRIC-337_context.md`

## Segurança

⚠️ **NUNCA** commite seu token de API no Git!

- Use variáveis de ambiente
- Adicione `.env` ao `.gitignore`
- Rotacione tokens periodicamente
- Use tokens com permissões mínimas necessárias

## Suporte

Se encontrar problemas:

1. Verifique a documentação da API do Jira: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
2. Consulte a documentação da biblioteca: https://jira.readthedocs.io/
3. Verifique os logs de erro no terminal
