#!/usr/bin/env python3
"""
Script para buscar informações de uma task do Jira e gerar contexto para agente de IA.
Uso: python jira_context_generator.py TASK-123
"""

import sys
import os
import json
from datetime import datetime

# Carregar variáveis do arquivo .env se existir
DOTENV_AVAILABLE = False
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    pass  # python-dotenv não é obrigatório se usar variáveis de ambiente

try:
    from jira import JIRA
except ImportError:
    print("Erro: Biblioteca 'jira' não encontrada.")
    print("Instale com: pip install jira")
    sys.exit(1)

def load_jira_config():
    """Carrega configurações do Jira de variáveis de ambiente."""
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')

    if not all([jira_url, jira_email, jira_token]):
        print("Erro: Configurações do Jira não encontradas.")

        if not DOTENV_AVAILABLE:
            print("\n⚠️  Aviso: Biblioteca 'python-dotenv' não detectada.")
            print("   Se você usa um arquivo .env, instale com: pip install python-dotenv")

        print("\nConfigure as seguintes variáveis de ambiente:")
        print("  export JIRA_URL='https://sua-empresa.atlassian.net'")
        print("  export JIRA_EMAIL='seu-email@empresa.com'")
        print("  export JIRA_API_TOKEN='seu-token-aqui'")
        print("\nPara gerar um token de API:")
        print("  1. Acesse: https://id.atlassian.com/manage-profile/security/api-tokens")
        print("  2. Clique em 'Create API token'")
        print("  3. Copie o token gerado")
        sys.exit(1)

    return jira_url, jira_email, jira_token

def connect_jira(url, email, token):
    """Conecta ao Jira usando autenticação básica."""
    try:
        jira = JIRA(
            server=url,
            basic_auth=(email, token)
        )
        return jira
    except Exception as e:
        print(f"Erro ao conectar ao Jira: {e}")
        sys.exit(1)

def fetch_issue_details(jira, issue_key):
    """Busca detalhes completos de uma issue do Jira."""
    try:
        issue = jira.issue(issue_key, expand='changelog,renderedFields')
        return issue
    except Exception as e:
        print(f"Erro ao buscar issue '{issue_key}': {e}")
        sys.exit(1)

def format_context(issue):
    """Formata as informações da issue em contexto para IA."""
    context = []

    # Frontmatter com metadata estruturado
    context.append("---")
    context.append(f"jira_key: {issue.key}")
    context.append(f"title: {issue.fields.summary}")
    context.append(f"type: {issue.fields.issuetype.name}")
    context.append(f"status: {issue.fields.status.name}")
    context.append(f"priority: {issue.fields.priority.name if issue.fields.priority else 'N/A'}")
    context.append(f"project: {issue.fields.project.key}")
    context.append(f"link: {issue.permalink()}")
    context.append(f"generated_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context.append("---")
    context.append("")

    # Cabeçalho principal
    context.append(f"# {issue.key}: {issue.fields.summary}")
    context.append("")

    # Informações básicas em formato de tabela
    context.append("## Informações Básicas")
    context.append("")
    context.append("| Campo | Valor |")
    context.append("|-------|-------|")
    context.append(f"| Tipo | {issue.fields.issuetype.name} |")
    context.append(f"| Status | {issue.fields.status.name} |")
    context.append(f"| Prioridade | {issue.fields.priority.name if issue.fields.priority else 'N/A'} |")
    context.append(f"| Projeto | {issue.fields.project.name} ({issue.fields.project.key}) |")
    context.append(f"| Reporter | {issue.fields.reporter.displayName if issue.fields.reporter else 'N/A'} |")
    context.append(f"| Assignee | {issue.fields.assignee.displayName if issue.fields.assignee else 'Não atribuído'} |")
    context.append("")

    # Labels e Componentes (se existirem)
    if issue.fields.labels or issue.fields.components:
        if issue.fields.labels:
            context.append(f"| Labels | {', '.join(issue.fields.labels)} |")
        if issue.fields.components:
            context.append(f"| Componentes | {', '.join([c.name for c in issue.fields.components])} |")
        context.append("")

    # Descrição
    context.append("## Descrição")
    context.append("")
    if issue.fields.description:
        context.append(issue.fields.description)
    else:
        context.append("*Sem descrição*")
    context.append("")

    # Acceptance Criteria (se existir)
    if hasattr(issue.fields, 'customfield_10100'):
        ac = getattr(issue.fields, 'customfield_10100', None)
        if ac:
            context.append("## Critérios de Aceitação")
            context.append("")
            context.append(ac)
            context.append("")

    # Subtasks
    if hasattr(issue.fields, 'subtasks') and issue.fields.subtasks:
        context.append("## Subtasks")
        context.append("")
        for subtask in issue.fields.subtasks:
            context.append(f"- **[{subtask.key}]** {subtask.fields.summary} - *{subtask.fields.status.name}*")
        context.append("")

    # Links relacionados
    if hasattr(issue.fields, 'issuelinks') and issue.fields.issuelinks:
        context.append("## Issues Relacionadas")
        context.append("")
        for link in issue.fields.issuelinks:
            if hasattr(link, 'outwardIssue'):
                related = link.outwardIssue
                context.append(f"- **{link.type.outward}**: [{related.key}] {related.fields.summary}")
            elif hasattr(link, 'inwardIssue'):
                related = link.inwardIssue
                context.append(f"- **{link.type.inward}**: [{related.key}] {related.fields.summary}")
        context.append("")

    # Comentários
    if issue.fields.comment.comments:
        context.append("## Comentários")
        context.append("")
        for idx, comment in enumerate(issue.fields.comment.comments[-5:], 1):
            context.append(f"### Comentário {idx}")
            context.append("")
            context.append(f"**Autor**: {comment.author.displayName}  ")
            context.append(f"**Data**: {comment.created}")
            context.append("")
            context.append(comment.body)
            context.append("")

    # Rodapé
    context.append("---")
    context.append("")
    context.append(f"**Link da Issue**: [{issue.key}]({issue.permalink()})")

    return "\n".join(context)

def main():
    if len(sys.argv) != 2:
        print("Uso: python jira_context_generator.py TASK-123")
        sys.exit(1)

    issue_key = sys.argv[1].upper()

    print(f"Buscando informações da task: {issue_key}...")

    # Carrega configurações
    jira_url, jira_email, jira_token = load_jira_config()

    # Conecta ao Jira
    jira = connect_jira(jira_url, jira_email, jira_token)

    # Busca detalhes da issue
    issue = fetch_issue_details(jira, issue_key)

    # Formata contexto
    context = format_context(issue)

    # Salva em arquivo
    output_file = f"{issue_key}_context.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(context)

    print(f"\n✓ Contexto gerado com sucesso!")
    print(f"✓ Arquivo salvo: {output_file}")
    print(f"✓ Link: {issue.permalink()}")

if __name__ == "__main__":
    main()
