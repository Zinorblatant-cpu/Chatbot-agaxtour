queue = []

def add_to_queue(token: str):
    """
    Adiciona o token de um usuário à fila de atendimento.
    Retorna a posição atual do usuário na fila.
    """
    if token not in queue:
        queue.append(token)
    return queue.index(token) + 1  
