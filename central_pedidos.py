import threading
import time

# servidor simulados
principal = {
    "online": True,
    "estoque": 10
}

replica = {
    "online": True,
    "estoque": 10
}

# controle de concorrencia
MAXIMO_SIMULTANEO = 2

semaforo = threading.Semaphore(MAXIMO_SIMULTANEO)

trava = threading.Lock()

pedidos_confirmados = []

def processar_pedido(numero):
    with semaforo:
        time.sleep(0.1)

        with trava:
            if principal["estoque"] > 0:
                principal["estoque"] -= 1
                pedidos_confirmados.append(numero)

def sicronizar():
    with trava:
        replica["estoque"] = principal["estoque"]

def consultar_estoque():
    with trava:
        if principal["online"]:
            return (
                "PRINCIPAL",
                principal["estoque"]
            )

        if replica["online"]:
            return (
                "REPLICA",
                replica["estoque"]
            )
        return "INDISPONIVEL", None

print("=== CENTRAL DE PEDIDOS ===")

print(
    "Limite simultaneo: ",
    MAXIMO_SIMULTANEO
)

print(
    "Estoque inicial: ",
    principal["estoque"]
)

trabalhadores = [
    threading.Thread(
        target=processar_pedido,
        args=(numero, )
    )
    for numero in [101, 102, 103]
]

for trabalhador in trabalhadores:
    trabalhador.start()

for trabalhador in trabalhadores:
    trabalhador.join()

print(
    "pedidos confirmados:",
    sorted(pedidos_confirmados)
)

print(
    "Estoque principal:",
    principal["estoque"]
)

print(
    "Replica antes:",
    replica["estoque"]
)

sicronizar()

print(
    "Replica depois:",
    replica["estoque"]
)

# simulacao de falha
principal["online"] = False

nome, estoque = consultar_estoque()

print(
    "Consulta apos falha:",
    nome,
    estoque
)