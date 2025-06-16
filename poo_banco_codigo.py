from abc import ABC, abstractmethod
from datetime import datetime

# Classe Transacao (Interface)
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Subclasse Deposito
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

# Subclasse Saque
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        tipo = transacao.__class__.__name__
        self.transacoes.append({"tipo": tipo, "valor": transacao.valor, "data": data})

# Classe Conta
class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        print("@@@ Saldo insuficiente. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        print("@@@ Valor de depósito inválido. @@@")
        return False

# ContaCorrente (herda Conta)
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("@@@ Limite de saques excedido. @@@")
            return False
        if valor > self.limite:
            print("@@@ Valor excede o limite permitido. @@@")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False

# Classe Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# PessoaFisica (herda Cliente)
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento