import socket
import time
import random

# Ponto de Partida do cálculo do RTT
start_time = time.time()

# --- Funções Auxiliares para RSA de 4096 bits ---
def miller_rabin(n, k=40):
    if n == 2 or n == 3: return True
    if n <= 1 or n % 2 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_large_prime(keysize=2048):
    while True:
        p = random.randrange(2**(keysize-1), 2**keysize)
        if miller_rabin(p): return p

def generate_keypair(keysize=4096):
    print(f"Gerando chaves RSA do CLIENTE de {keysize} bits... (isso pode demorar)")
    p = generate_large_prime(keysize // 2)
    q = generate_large_prime(keysize // 2)
    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 65537 # Expoente público padrão
    d = pow(e, -1, phi_N)
    return (e, N), (d, N)
# ------------------------------------------------

# Configurações de Conexão
serverName = "10.1.70.35"
serverPort = 1300
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Etapas 2 e 3: Gerar par de chaves do cliente (4096 bits)
public_key, private_key = generate_keypair()
print("Chaves do cliente geradas com sucesso!\n")

clientSocket.connect((serverName, serverPort))

# Etapa 4: Troca de chaves públicas em texto puro
# Enviar Chave Pública do Cliente para o Servidor
client_pub_key_str = f"{public_key[0]},{public_key[1]}"
clientSocket.send(client_pub_key_str.encode('utf-8'))
print("Chave pública do cliente enviada.")

# Receber Chave Pública do Servidor
server_pub_key_str = clientSocket.recv(65000).decode('utf-8')
e_server, N_server = map(int, server_pub_key_str.split(','))
print("Chave pública do servidor recebida.\n")

# Frase de atividade
sentence = "the information security is of significant importance to ensure the privacy of communications"
print(f"Mensagem que será enviada: '{sentence}'\n")

# Criptografar a mensagem utilizando a Chave Pública do Servidor
message_int = int.from_bytes(sentence.encode('utf-8'), 'big')
encrypted_int = pow(message_int, e_server, N_server)
encrypted_bytes = encrypted_int.to_bytes((encrypted_int.bit_length() + 7) // 8, 'big')

# Enviar mensagem encriptada
clientSocket.send(encrypted_bytes)
print("Mensagem cifrada enviada para o servidor.")

# Receber mensagem cifrada em maiúsculo do Servidor
modifiedSentence_bytes = clientSocket.recv(65000)

# Decriptografar a resposta usando a Chave Privada do Cliente
encrypted_recv_int = int.from_bytes(modifiedSentence_bytes, 'big')
decrypted_int = pow(encrypted_recv_int, private_key[0], private_key[1])
text = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode('utf-8')

print("Received from Make Upper Case Server (Decrypted):", text)

clientSocket.close()

# Ponto de Finalização do cálculo do RTT
end_time = time.time()
rtt = end_time - start_time
print(f"\n[INFO] RTT (Round Trip Time): {rtt:.4f} segundos")