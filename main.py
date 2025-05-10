from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

# ================================================
# Constantes
# ================================================
AGENCIA_PADRAO = "0001"
LIMITE_SAQUES_DIARIOS_PADRAO = 3
LIMITE_VALOR_SAQUE_PADRAO = 500.0

# ================================================
# Funções Auxiliares
# ================================================
def limpar_cpf(cpf: str) -> str:
    """Remove caracteres não numéricos de uma string de CPF."""
    return ''.join(filter(str.isdigit, cpf))

def formatar_moeda(valor: float) -> str:
    """Formata um valor float para o formato de moeda R$ XX,XX."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def obter_data_hora_atual_str() -> str:
    """Retorna a data e hora atuais formatadas."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def validar_data(data_str: str) -> Optional[datetime]:
    """Valida e converte uma string de data (dd/mm/aaaa) para datetime."""
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None

# ================================================
# Classes de Domínio
# ================================================
class Usuario:
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime, endereco: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco

    def __str__(self) -> str:
        return f"Nome: {self.nome}, CPF: {self.cpf}, Nascimento: {self.data_nascimento.strftime('%d/%m/%Y')}"

class ContaBancaria:
    def __init__(self, numero_conta: int, titular: Usuario, agencia: str = AGENCIA_PADRAO):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.titular = titular
        self.saldo: float = 0.0
        self.extrato: List[str] = []
        self.saques_realizados: List[datetime] = [] # Armazena Timestamps dos saques
        self.limite_saques_diarios = LIMITE_SAQUES_DIARIOS_PADRAO
        self.limite_valor_saque = LIMITE_VALOR_SAQUE_PADRAO

    def _registrar_transacao(self, tipo: str, valor: float):
        self.extrato.append(f"{obter_data_hora_atual_str()} - {tipo}: {formatar_moeda(valor)}")

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Erro: Valor do depósito deve ser positivo.")
            return False
        self.saldo += valor
        self._registrar_transacao("Depósito", valor)
        print("✅ Depósito realizado com sucesso!")
        return True

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Erro: Valor do saque deve ser positivo.")
            return False

        # Verifica saques nas últimas 24 horas
        agora = datetime.now()
        saques_ultimas_24h = [
            s for s in self.saques_realizados if agora - s < timedelta(days=1)
        ]
        
        # Se o dia mudou, resetar a lista de saques para contar apenas os de hoje
        # Ou, se a lógica é "últimas 24h", a linha acima já cuida disso.
        # Se a lógica fosse "por dia calendário", precisaríamos de um reset
        # if self.saques_realizados and self.saques_realizados[-1].date() < agora.date():
        #    self.saques_realizados = [] # Resetaria para o novo dia

        if self.saldo < valor:
            print("Erro: Saldo insuficiente.")
            return False
        if valor > self.limite_valor_saque:
            print(f"Erro: Limite por saque é de {formatar_moeda(self.limite_valor_saque)}.")
            return False
        if len(saques_ultimas_24h) >= self.limite_saques_diarios:
            print("Erro: Limite de saques diários atingido.")
            return False

        self.saldo -= valor
        self.saques_realizados.append(datetime.now())
        self._registrar_transacao("Saque", valor)
        print("✅ Saque realizado com sucesso!")
        return True

    def exibir_extrato(self):
        print(f"\n═{' EXTRATO ':=^48}")
        print(f"Agência: {self.agencia} | Conta: {self.numero_conta:04d}") # Formata número da conta
        print(f"Titular: {self.titular.nome}")
        print("\nMovimentações:")
        if not self.extrato:
            print("Nenhuma movimentação registrada.")
        else:
            for movimento in self.extrato:
                print(movimento)
        print(f"\nSaldo atual: {formatar_moeda(self.saldo)}")
        print("=" * 50)

    def __str__(self) -> str:
        return f"Conta {self.numero_conta:04d} (Ag. {self.agencia}) - Titular: {self.titular.nome} - Saldo: {formatar_moeda(self.saldo)}"

# ================================================
# Gestão do Banco (Centraliza usuários e contas)
# ================================================
class Banco:
    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.contas: List[ContaBancaria] = []
        self._proximo_numero_conta = 1

    def buscar_usuario_por_cpf(self, cpf: str) -> Optional[Usuario]:
        cpf_limpo = limpar_cpf(cpf)
        return next((u for u in self.usuarios if u.cpf == cpf_limpo), None)

    def cadastrar_usuario(self) -> Optional[Usuario]:
        print("\n--- Cadastro de Novo Usuário ---")
        cpf = limpar_cpf(input("CPF (apenas números): ").strip())

        if len(cpf) != 11:
            print("Erro: CPF deve conter 11 dígitos.")
            return None
        if self.buscar_usuario_por_cpf(cpf):
            print("Erro: CPF já cadastrado.")
            return None

        nome = input("Nome completo: ").strip()
        if not nome:
            print("Erro: Nome não pode ser vazio.")
            return None
            
        data_nasc_str = input("Data nascimento (dd/mm/aaaa): ").strip()
        data_nasc = validar_data(data_nasc_str)
        if not data_nasc:
            print("Erro: Data de nascimento inválida.")
            return None
        
        logradouro = input("Logradouro: ").strip()
        nro = input("Número: ").strip()
        bairro = input("Bairro: ").strip()
        cidade = input("Cidade: ").strip()
        uf = input("UF (sigla): ").strip().upper()
        
        if not all([logradouro, nro, bairro, cidade, uf]):
            print("Erro: Todos os campos do endereço são obrigatórios.")
            return None
        if len(uf) != 2:
            print("Erro: UF deve ter 2 caracteres.")
            return None

        endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{uf}"
        novo_usuario = Usuario(cpf, nome, data_nasc, endereco)
        self.usuarios.append(novo_usuario)
        print("✅ Usuário cadastrado com sucesso!")
        return novo_usuario

    def criar_conta_bancaria(self) -> Optional[ContaBancaria]:
        print("\n--- Criação de Nova Conta ---")
        cpf_titular = limpar_cpf(input("CPF do titular: ").strip())
        usuario_titular = self.buscar_usuario_por_cpf(cpf_titular)

        if not usuario_titular:
            print("Erro: Usuário não encontrado. Cadastre o usuário primeiro.")
            return None

        nova_conta = ContaBancaria(numero_conta=self._proximo_numero_conta, titular=usuario_titular)
        self.contas.append(nova_conta)
        self._proximo_numero_conta += 1
        print(f"✅ Conta {nova_conta.numero_conta:04d} criada com sucesso para {usuario_titular.nome}!")
        return nova_conta

    def selecionar_conta(self, cpf_usuario: str) -> Optional[ContaBancaria]:
        cpf_limpo = limpar_cpf(cpf_usuario)
        usuario = self.buscar_usuario_por_cpf(cpf_limpo)
        if not usuario:
            print("Erro: Usuário não encontrado.")
            return None

        contas_do_usuario = [c for c in self.contas if c.titular.cpf == cpf_limpo]

        if not contas_do_usuario:
            print(f"Nenhuma conta encontrada para o CPF {cpf_limpo}.")
            return None

        if len(contas_do_usuario) == 1:
            print(f"Conta {contas_do_usuario[0].numero_conta:04d} selecionada automaticamente.")
            return contas_do_usuario[0]

        print("\nSuas contas:")
        for i, conta in enumerate(contas_do_usuario):
            print(f"{i + 1}. Conta {conta.numero_conta:04d} - Saldo: {formatar_moeda(conta.saldo)}")

        while True:
            try:
                escolha = int(input("Digite o número da opção da conta: "))
                if 1 <= escolha <= len(contas_do_usuario):
                    return contas_do_usuario[escolha - 1]
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    
    def listar_contas_cadastradas(self):
        print("\n═{' CONTAS CADASTRADAS ':=^48}")
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self.contas:
            print(conta) # Usa o __str__ da classe ContaBancaria
        print("=" * 50)

# ================================================
# Interface com Usuário (Menus e Interação)
# ================================================
def menu_operacoes_bancarias(conta_selecionada: ContaBancaria):
    while True:
        print("\n═{' OPERAÇÕES ':=^48}")
        print(f"Conta: {conta_selecionada.numero_conta:04d} | Titular: {conta_selecionada.titular.nome}")
        print("1 - Depositar")
        print("2 - Sacar")
        print("3 - Extrato")
        print("4 - Voltar ao Menu Principal")

        sub_opcao = input("Opção: ").strip()

        if sub_opcao == "1":
            try:
                valor = float(input("Valor do depósito: R$ ").strip().replace(",", "."))
                conta_selecionada.depositar(valor)
            except ValueError:
                print("Erro: Valor inválido para depósito.")
        elif sub_opcao == "2":
            try:
                valor = float(input("Valor do saque: R$ ").strip().replace(",", "."))
                conta_selecionada.sacar(valor)
            except ValueError:
                print("Erro: Valor inválido para saque.")
        elif sub_opcao == "3":
            conta_selecionada.exibir_extrato()
        elif sub_opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_principal(banco: Banco):
    while True:
        print("\n═{' SISTEMA BANCÁRIO PYTHON ':=^48}")
        print("1 - Novo Usuário")
        print("2 - Nova Conta Bancária")
        print("3 - Acessar Conta (Operações)")
        print("4 - Listar Contas Cadastradas")
        print("5 - Listar Usuários Cadastrados") # Nova opção
        print("6 - Sair")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            banco.cadastrar_usuario()
        elif opcao == "2":
            banco.criar_conta_bancaria()
        elif opcao == "3":
            cpf = input("Digite o CPF do titular da conta: ").strip()
            conta_selecionada = banco.selecionar_conta(cpf)
            if conta_selecionada:
                menu_operacoes_bancarias(conta_selecionada)
        elif opcao == "4":
            banco.listar_contas_cadastradas()
        elif opcao == "5":
            print("\n═{' USUÁRIOS CADASTRADOS ':=^48}")
            if not banco.usuarios:
                print("Nenhum usuário cadastrado.")
            for usuario in banco.usuarios:
                print(usuario) # Usa o __str__ da classe Usuario
            print("=" * 50)
        elif opcao == "6":
            print("\nObrigado por utilizar nossos serviços!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# ================================================
# Execução Principal
# ================================================
if __name__ == "__main__":
    meu_banco = Banco()
    menu_principal(meu_banco)
