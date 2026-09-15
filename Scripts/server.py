import socket
import random

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
    # Se quiser usar o 'PrimoHyper' do professor, você pode importá-lo aqui.
    while True:
        p = random.randrange(2**(keysize-1), 2**keysize)
        if miller_rabin(p): return p

def generate_keypair(keysize=4096):
    print(f"Gerando chaves RSA do SERVIDOR de {keysize} bits... (isso pode demorar)")
    p = generate_large_prime(keysize // 2)
    q = generate_large_prime(keysize // 2)
    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 65537 # Expoente público padrão
    d = pow(e, -1, phi_N)
    return (e, N), (d, N)
# ------------------------------------------------

serverPort = 1300
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("TCP Server Inicializado\n")

# Etapas 2 e 3: Gerar par de chaves de 4096 bits para o servidor
public_key, private_key = generate_keypair()
print("Chaves do servidor geradas com sucesso!\n")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Conexão recebida de {addr}")
   
    # Etapa 4: Troca de chaves públicas em texto puro
    # Receber Chave Pública do Cliente
    client_pub_key_str = connectionSocket.recv(65000).decode('utf-8')
    e_client, N_client = map(int, client_pub_key_str.split(','))
    print("Chave pública do cliente recebida.")
   
    # Enviar Chave Pública do Servidor
    server_pub_key_str = f"{public_key[0]},{public_key[1]}"
    connectionSocket.send(server_pub_key_str.encode('utf-8'))
    print("Chave pública do servidor enviada.\n")
   
    # Receber Mensagem Cifrada
    encrypted_sentence_bytes = connectionSocket.recv(65000)
    encrypted_sentence_int = int.from_bytes(encrypted_sentence_bytes, 'big')
   
    # Decriptar usando a Chave Privada do Servidor
    decrypted_int = pow(encrypted_sentence_int, private_key[0], private_key[1])
    received_sentence = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode('utf-8')
    print("Mensagem decifrada do Cliente: ", received_sentence)
   
    # Processamento: deixar a mensagem em maiúsculo
    capitalizedSentence = received_sentence.upper()
   
    # Criptografar a resposta com a Chave Pública do Cliente
    message_int = int.from_bytes(capitalizedSentence.encode('utf-8'), 'big')
    encrypted_capitalized_int = pow(message_int, e_client, N_client)
    encrypted_capitalized_bytes = encrypted_capitalized_int.to_bytes((encrypted_capitalized_int.bit_length() + 7) // 8, 'big')
   
    # Enviar de volta ao Cliente
    connectionSocket.send(encrypted_capitalized_bytes)
    print("Mensagem processada e cifrada enviada de volta ao Cliente.\n")
   
    connectionSocket.close()

