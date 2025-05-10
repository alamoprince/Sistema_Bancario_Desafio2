# # Sistema Bancário Simples em Python

Este projeto é uma simulação de um sistema bancário básico desenvolvido em Python, com foco em operações essenciais como cadastro de usuários, criação de contas, depósitos, saques e visualização de extratos. O sistema foi refatorado para utilizar conceitos de Programação Orientada a Objetos (POO) para melhor organização, manutenibilidade e escalabilidade.

## Funcionalidades Principais

*   **Gestão de Usuários:**
    *   Cadastro de novos usuários com CPF (validação de 11 dígitos e unicidade), nome completo, data de nascimento e endereço completo.
*   **Gestão de Contas Bancárias:**
    *   Criação de contas correntes vinculadas a um usuário existente.
    *   Cada conta possui agência (fixa "0001"), número sequencial, saldo, histórico de transações (extrato), limite de saques diários e limite de valor por saque.
*   **Operações Bancárias:**
    *   **Depósito:** Permite adicionar fundos à conta.
    *   **Saque:** Permite retirar fundos da conta, respeitando:
        *   Saldo disponível.
        *   Limite de valor por saque (R$ 500,00 por padrão).
        *   Limite de 3 saques diários (considerando as últimas 24 horas).
    *   **Extrato:** Exibe todas as transações realizadas na conta (depósitos e saques) e o saldo atual.
*   **Listagens:**
    *   Listar todas as contas cadastradas no sistema.
    *   Listar todos os usuários cadastrados.
*   **Interface:**
    *   Interação via console (terminal) com menus navegáveis.

## Tecnologias Utilizadas

*   **Python 3.x**
*   Módulos Nativos:
    *   `datetime` e `timedelta` para manipulação de datas e horários (controle de saques diários).
    *   `typing` para type hints, melhorando a legibilidade e auxiliando na detecção de erros.

## Como Executar

1.  **Pré-requisitos:**
    *   Certifique-se de ter o Python 3 instalado em seu sistema.

2.  **Baixar o código:**
    *   Salve o código fornecido em um arquivo com a extensão `.py` (por exemplo, `sistema_bancario.py`).

3.  **Executar o script:**
    *   Abra um terminal ou prompt de comando.
    *   Navegue até o diretório onde você salvou o arquivo.
    *   Execute o comando:
        ```bash
        python sistema_bancario.py
        ```

4.  **Interagir com o sistema:**
    *   Siga as instruções apresentadas no menu do console para realizar as operações.

## Estrutura do Código

O código está organizado da seguinte forma:

*   **Constantes:** Definições de valores fixos como agência padrão, limites de saque, etc.
*   **Funções Auxiliares:** Pequenas funções utilitárias (ex: `limpar_cpf`, `formatar_moeda`, `validar_data`).
*   **Classes de Domínio:**
    *   `Usuario`: Representa um cliente do banco, com seus dados pessoais.
    *   `ContaBancaria`: Representa uma conta bancária, com seus atributos (saldo, extrato, etc.) e métodos para operações (depositar, sacar).
*   **Classe de Gestão:**
    *   `Banco`: Centraliza a gestão de usuários e contas, contendo listas de ambos e métodos para criá-los e buscá-los.
*   **Interface com Usuário:**
    *   Funções de menu (`menu_principal`, `menu_operacoes_bancarias`) que controlam o fluxo de interação com o usuário.
*   **Bloco de Execução Principal:**
    *   A seção `if __name__ == "__main__":` que inicializa o sistema.

## Melhorias Implementadas (em relação a uma versão procedural anterior)

*   **Orientação a Objetos (OOP):** Uso de classes (`Usuario`, `ContaBancaria`, `Banco`) para melhor encapsulamento e organização.
*   **Separação de Responsabilidades:** Cada classe e função tem um propósito mais definido.
*   **Validação de Dados:** Verificações mais robustas nas entradas do usuário (CPF, data, valores).
*   **Tratamento de Erros:** Uso de `try-except` para lidar com entradas inválidas.
*   **Legibilidade:** Código mais claro e organizado, com uso de type hints e comentários.
*   **Reusabilidade:** Componentes como as classes podem ser mais facilmente reutilizados ou estendidos.

## Possíveis Melhorias Futuras

*   **Persistência de Dados:** Salvar e carregar dados de usuários e contas em arquivos (JSON, CSV, SQLite) para que as informações não sejam perdidas ao fechar o programa.
*   **Mais Tipos de Conta:** Implementar outros tipos de conta (ex: Conta Poupança, Conta Salário).
*   **Transferências:** Adicionar funcionalidade de transferência de valores entre contas.
*   **Autenticação:** Sistema de login com senha para usuários.
*   **Interface Gráfica (GUI):** Desenvolver uma interface gráfica utilizando bibliotecas como Tkinter, PyQt, ou Kivy.
*   **Interface Web:** Transformar em uma aplicação web usando frameworks como Flask ou Django.
*   **Testes Unitários:** Escrever testes para garantir o correto funcionamento das classes e funções.
*   **Log de Transações Detalhado:** Gerar logs mais completos das operações para auditoria.
*   **Internacionalização (i18n):** Suporte a múltiplos idiomas.

---
