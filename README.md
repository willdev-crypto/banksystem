# 🏦 Bank System - Sistema Bancário em Python

Este projeto é um sistema bancário simples desenvolvido em Python, que permite a criação de usuários, contas bancárias, realização de depósitos, saques e emissão de extrato. O sistema simula funcionalidades básicas de um banco com operações por terminal.

## 📋 Funcionalidades

- Cadastro de usuários com validação de CPF único.
- Criação de contas bancárias vinculadas a usuários.
- Verificação de CPF cadastrado.
- Depósitos com validação de valor.
- Saques com limite diário e por valor.
- Emissão de extrato bancário com histórico de transações.
- Interface por terminal com menus interativos.

## 🧱 Estrutura do Sistema

- **Usuários:** Armazenados em memória com nome, data de nascimento, CPF e endereço.
- **Contas:** Vinculadas a usuários, com número sequencial e agência padrão.
- **Operações Bancárias:**
  - **Depósito:** Aceita valores positivos.
  - **Saque:** Limite de 3 saques por sessão, até R$ 500,00 por operação.
  - **Extrato:** Exibe todas as movimentações realizadas e o saldo atual.

## ▶️ Como Usar

1. **Execute o script `main()`**
   ```bash
   interface.py
Menu Principal:

[c] Criar Usuário

[v] Verificar se CPF está cadastrado

[e] Entrar no sistema bancário (com CPF)

[q] Sair

Menu do Sistema Bancário (após login):

[a] Criar nova conta

[l] Listar contas cadastradas

[u] Listar todos os usuários

[d] Realizar depósito

[s] Realizar saque

[e] Ver extrato

[q] Sair da conta bancária

🔐 Regras de Negócio
Cada CPF só pode ser cadastrado uma vez.

Cada conta criada é automaticamente vinculada ao CPF informado.

Os saques são limitados a 3 por sessão e até R$ 500,00 por operação.

O extrato mostra apenas as transações feitas na sessão atual.

🧪 Exemplo de Uso
text
Copiar
Editar
Bem-vindo(a) ao Bank System!
[c] Criar Usuário
[v] CPF Cadastrado
[e] Ver Conta e detalhes
[q] Sair
Escolha uma opção: c
Nome: João Silva
Data de Nascimento (dd/mm/aaaa): 01/01/1990
CPF (apenas números): 12345678900
Endereço (logradouro, número, cidade/estado): Rua A, 123, SP/SP
Usuário criado com sucesso!
🛠 Tecnologias Utilizadas
Python 3

Módulo datetime (embora não utilizado ainda, está disponível para futuras melhorias).


🚀 Melhorias Futuras
Persistência de dados com arquivos ou banco de dados.

Interface gráfica com Tkinter ou Flask.

Sistema de login com autenticação.

Implementação de histórico completo por usuário/conta.

👤 Autor:

William Oliveira

Desenvolvedor Front-End & Analista de Sistemas

📧 wil.dgl@hotmail.com


