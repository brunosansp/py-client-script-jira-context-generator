#!/bin/bash
# Script de configuração inicial para o Jira Context Generator

echo "=========================================="
echo "  Configuração do Jira Context Generator"
echo "=========================================="
echo ""

# Detectar shell
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        SHELL_CONFIG="$HOME/.bash_profile"
    fi
    SHELL_NAME="bash"
else
    echo "⚠️  Shell não detectado. Usando ~/.bashrc como padrão."
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
fi

echo "Shell detectado: $SHELL_NAME"
echo "Arquivo de configuração: $SHELL_CONFIG"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.6 ou superior."
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"
echo ""

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip não encontrado. Por favor, instale pip."
    exit 1
fi

echo "✓ pip encontrado"
echo ""

# Perguntar se deseja instalar dependências
read -p "Deseja instalar a biblioteca 'jira'? (s/n): " install_deps
if [ "$install_deps" = "s" ] || [ "$install_deps" = "S" ]; then
    echo "Instalando biblioteca jira..."
    pip3 install jira
    echo ""
fi

# Coletar informações do Jira
echo "Por favor, forneça as seguintes informações:"
echo ""

read -p "URL do Jira (ex: https://sua-empresa.atlassian.net): " jira_url
read -p "Email do Jira: " jira_email
read -sp "Token de API do Jira: " jira_token
echo ""
echo ""

# Validar inputs
if [ -z "$jira_url" ] || [ -z "$jira_email" ] || [ -z "$jira_token" ]; then
    echo "❌ Todos os campos são obrigatórios!"
    exit 1
fi

# Perguntar método de configuração
echo "Como deseja salvar as configurações?"
echo "1) Variáveis de ambiente permanentes (adicionar ao $SHELL_CONFIG)"
echo "2) Arquivo .env local (mais seguro para projetos)"
echo ""
read -p "Escolha (1 ou 2): " config_method

if [ "$config_method" = "1" ]; then
    # Adicionar ao arquivo de configuração do shell
    echo "" >> "$SHELL_CONFIG"
    echo "# Configurações do Jira Context Generator" >> "$SHELL_CONFIG"
    echo "export JIRA_URL=\"$jira_url\"" >> "$SHELL_CONFIG"
    echo "export JIRA_EMAIL=\"$jira_email\"" >> "$SHELL_CONFIG"
    echo "export JIRA_API_TOKEN=\"$jira_token\"" >> "$SHELL_CONFIG"

    echo ""
    echo "✓ Configurações adicionadas ao $SHELL_CONFIG"
    echo ""
    echo "Para aplicar as mudanças, execute:"
    echo "  source $SHELL_CONFIG"
    echo ""
    echo "Ou feche e abra um novo terminal."

elif [ "$config_method" = "2" ]; then
    # Criar arquivo .env
    cat > .env << EOF
JIRA_URL=$jira_url
JIRA_EMAIL=$jira_email
JIRA_API_TOKEN=$jira_token
EOF

    echo ""
    echo "✓ Arquivo .env criado com sucesso!"
    echo ""

    # Adicionar .env ao .gitignore se não existir
    if [ -f .gitignore ]; then
        if ! grep -q "^\.env$" .gitignore; then
            echo ".env" >> .gitignore
            echo "✓ .env adicionado ao .gitignore"
        fi
    else
        echo ".env" > .gitignore
        echo "✓ .gitignore criado com .env"
    fi

    echo ""
    echo "⚠️  IMPORTANTE: Instale python-dotenv para usar o arquivo .env:"
    echo "  pip3 install python-dotenv"
    echo ""
    echo "E descomente as linhas no script jira_context_generator.py:"
    echo "  from dotenv import load_dotenv"
    echo "  load_dotenv()"

else
    echo "❌ Opção inválida!"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Configuração concluída!"
echo "=========================================="
echo ""
echo "Para testar, execute:"
echo "  python3 jira_context_generator.py TASK-123"
echo ""
echo "Substitua TASK-123 pela chave de uma task real do seu Jira."
echo ""
