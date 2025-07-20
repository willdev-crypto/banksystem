# 🏦 Bank System - Sistema Bancário em Python (Flask)

Este projeto é um sistema bancário simples desenvolvido em Python com Flask, permitindo cadastro de usuários, contas bancárias, depósitos, saques, extrato completo e painel administrativo. O sistema simula funcionalidades básicas de um banco, agora com interface web.

## 📋 Funcionalidades

- Cadastro de usuários com validação de CPF único e e-mail obrigatório
- Criação automática de agência e conta corrente
- Login seguro com senha criptografada
- Recuperação de senha por e-mail (simulada)
- Depósitos via boleto bancário (simulado)
- Saques com confirmação de senha e valor mínimo de R$ 0,01
- Emissão de extrato bancário completo com data e hora das movimentações
- Painel do usuário: saldo, agência, conta e extrato
- Painel do administrador: visualização de todos os usuários e saldos
- Apenas um usuário administrador permitido
- Interface web responsiva com Bootstrap

## 🧱 Estrutura do Sistema

- **Usuários:** Armazenados em `usuarios.json` (não enviado ao GitHub), com nome, data de nascimento, CPF, endereço, e-mail, senha (hash), agência, conta, saldo e tipo (admin ou comum).
- **Movimentações:** Armazenadas em `movimentacoes.json` (não enviado ao GitHub), com CPF, tipo, valor, data e hora.
- **Templates:** HTML com Bootstrap, localizados em `templates/`.
- **Arquivos estáticos:** CSS, JS e imagens em `static/`.

## ▶️ Como Usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/willdev-crypto/banksystem.git
   cd banksystem
   ```

2. **Instale as dependências:**
   ```bash
   pip install flask werkzeug
   ```

3. **Execute o sistema:**
   ```bash
   python app.py
   ```
   Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000) no navegador.

## 🔐 Segurança

- Senhas são armazenadas apenas como hash.
- Arquivos `usuarios.json` e `movimentacoes.json` estão no `.gitignore` e **não são enviados ao GitHub**.
- Nunca compartilhe dados sensíveis publicamente.

## 🚀 Melhorias Futuras

- Integração com banco de dados relacional (MySQL/PostgreSQL)
- Envio real de e-mail para recuperação de senha
- Relatórios financeiros em PDF
- API RESTful para integração com outros sistemas

## 👤 Autor

William Oliveira  
Desenvolvedor Python & Front-End  
📧 wil.dgl@hotmail.com

---

> Projeto educacional. Não utilize em produção real sem adaptações de segurança!


