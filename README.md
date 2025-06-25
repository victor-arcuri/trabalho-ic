# Trabalho de IC

## 📚 Sumário

- [🎯 Objetivo](#-objetivo)
- [📝 Base Teórica do Trabalho](#-base-teórica-do-trabalho)
- [💻 Base Prática do Trabalho](#-base-prática-do-trabalho)
  - [API](#api)
  - [Catraca](#catraca)
  - [Totem](#totem)
  - [App Mobile](#app-mobile)
- [✅ Requisitos](#-requisitos)
- [⚙️ Instalação](#-instalação)
- [🚀 Execução](#-execução)
- [📝 Notas](#-notas)
- [🧹 Remover ambiente virtual](#-remover-ambiente-virtual)

---

## 🎯 Objetivo
O trabalho de Introdução à Computação visa fortalecer a programação ética e a boa conduta social dos estudantes do curso, ao incentivá-los a utilizar sua criatividade e capacidade de resolução de problemas para criarem soluções tecnológicas para o ambiente universitário, as quais promovam o bem-estar social e a melhorem aspectos do dia-a-dia, solucionando problemas ou facilitando outros aspectos. 

---

## 📝 Base Teórica do Trabalho 
### O Problema
Atualmente, na UFMG, os estudantes se deparam com um grande problema: a falta de otimização e organização nas filas dos restaurantes universitários levam à superlotação do local e a grande perda de tempo para que seja possível se alimentar.

### A Solução
Visando corrigir essa falta de otimização, desejamos criar um sistema de controle de pagamento para acelerar as filas, por meio de um cartão específico para uso nos restaurantes universitários. Esse cartão poderá ser recarregado por totens espalhados no campus, ou por um aplicativo mobile, permitindo que o pagamento seja realizado automaticamente ao passar o cartão na catraca, caso haja saldo. Os totens e o aplicativo também devem apresentar o índice de lotação de cada restaurante, auxiliando na escolha de qual ir, sem que seja preciso conferir pessoalmente.

---

## 💻 Base Prática do Trabalho
Na prática, a partir de uma pesquisa, criaremos um documento com dados e informações embasando nossa ideia, além de detalhá-la. Além disso, criaremos mock-ups visuais das aplicações, slides para a apresentação e protótipos das funcionalidades básicas das aplicações, incluindo uma API, um banco de dados básico, um aplicativo mobile e uma aplicação para os totens, os quais todos serão detalhados a diante.

### API
A API será responsável por conectar as aplicações com o banco de dados, gerando uma camada extra de proteção, uma vez que o usuário não terá permissão para interagir diretamente com o banco e alterar valores como seu saldo, responsabilidade da API. 

#### Funcionalidades
- Adicionar um usuário ao banco
- Remover um usuário do banco
- Alterar informações do usuário no banco
- Obter informações de usuário específico do banco
- Adicionar um restaurante ao banco
- Remover um restaurante do banco
- Alterar informações do restaurante no banco
- Obter informações de um usuário específico do banco

Mais especificamente:

- Aumentar o saldo de um usuário por meio de uma recarga
- Debitar pagamento do saldo de um usuário
- Aumentar ou diminuir o número de pessoas em um restaurante

### Catraca
O protótipo da catraca é uma aplicação básica que tem como objetivo simular o processo de entrada e saída na catraca, por meio do uso do cartão para subtrair automaticamente o valor da entrada no restaurante universitário. Para fins de prototipagem, a aplicação permite:

- Escolher para qual restaurante será a catraca
- Entrar com o código da matrícula (simulando a passagem do cartão), subtraindo o valor de entrada e aumentando a taxa de lotação do restaurante na API
- Entrar sem o código da matrícula (simulando aqueles que entram pagando direto com antendentes), apenas aumentando a taxa de lotação do restaurante na API
- Sair do restaurante, reduzindo a taxa de lotação do restaurante na API

### Totem
O protótipo do totem é uma aplicação básica que tem como objetivo simular o processo da utilização do cartão nos totens espalhados pela faculdade, permitindo sua recarga e a análise da lotação dos restaurantes. Suas funcionalidades incluem:

- Ver saldo do cartão
- Permitir recarga do cartão
- Ver lotação dos restaurantes

### App Mobile
Tendo em vista que as funcionalidades do app mobile seriam as mesmas do totem, variando apenas métodos de pagamento, não há necessidade de criar um protótipo específico para ele.

---

## ✅ Requisitos

- Python 3.7 ou superior
- `pip` instalado
- `curl` (já vem no Windows 10+ e Linux)

---

## ⚙️ Instalação

Primeiro, clone o repositório:

```bash
git clone https://github.com/victor-arcuri/trabalho-ic/
cd trabalho-ic
```

<details>
<summary>🔵 Linux/macOS</summary>

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

</details>

<details>
<summary>🟣 Windows</summary>

```cmd
python -m venv venv
venv\Scriptsctivate
pip install -r requirements.txt
```

</details>

---

## 🚀 Execução

<details>
<summary>🔵 Linux/macOS</summary>

```bash
uvicorn api.main --reload
python3 -m catraca.main
python3 -m totem.main
./run.sh
```

</details>

<details>
<summary>🟣 Windows</summary>

```cmd
uvicorn api.main --reload
python3 -m catraca.main
python3 -m totem.main
run.bat
```

</details>

---

## 📝 Notas

- O script `run` ativa o ambiente, inicia a API e abre duas janelas (totem e catraca).
- Logs da API são salvos em `api.log`.

---

## 🧹 Remover ambiente virtual

```bash
rm -rf venv          # Linux/macOS
rd /s /q venv        # Windows
```
