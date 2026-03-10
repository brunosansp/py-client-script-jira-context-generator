# Jira AI Context Generator

Ferramenta para extrair informações de tasks do Jira e gerar contexto formatado para agentes de IA.

## O que faz?

Conecta-se ao Jira, busca detalhes de uma issue e gera um arquivo markdown estruturado com todas as informações relevantes para usar com o Kiro AI.

## Instalação Rápida (5 minutos)

```bash
# 1. Navegar até o diretório
cd py-client-script-jira-context-generator

# 2. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install jira python-dotenv

# 4. Configurar credenciais
./setup_jira.sh
```

## Uso Básico

```bash
# Ativar venv (se não estiver ativo)
source venv/bin/activate

# Gerar contexto de uma task
python jira_context_generator.py PRIC-337

# Ou usar o wrapper (ativa venv automaticamente)
./jira-context PRIC-337
```

Isso gera `PRIC-337_context.md` com todas as informações da task.

## Usar com Kiro

No chat do Kiro:

```
#PRIC-337_context.md

Crie um spec para implementar esta task
```

O Kiro vai ler o arquivo e criar automaticamente:

- `requirements.md` - Requisitos
- `design.md` - Design técnico
- `tasks.md` - Plano de implementação

## Documentação

- **[EXAMPLE_USAGE.md](EXAMPLE_USAGE.md)** - Tutorial prático com exemplo real
- **[GUIA_JIRA_CONTEXT.md](GUIA_JIRA_CONTEXT.md)** - Documentação completa e referência

## Troubleshooting Rápido

**Erro: "Biblioteca 'jira' não encontrada"**

```bash
source venv/bin/activate
pip install jira python-dotenv
```

**Erro: "Configurações do Jira não encontradas"**

```bash
./setup_jira.sh
```

**Mais problemas?** Veja [GUIA_JIRA_CONTEXT.md](GUIA_JIRA_CONTEXT.md#troubleshooting)

## Arquivos

- `jira_context_generator.py` - Script principal
- `jira-context` - Wrapper executável
- `setup_jira.sh` - Configuração interativa
- `.env.example` - Template de configuração

## Segurança

⚠️ **NUNCA** commite credenciais no Git! O arquivo `.env` está no `.gitignore`.
