# Atividade RSA - FESA

Implementação de uma comunicação entre cliente e servidor utilizando **RSA** para troca de mensagens, desenvolvida como atividade acadêmica da FESA.

O projeto utiliza Python, sockets TCP e uma implementação própria das operações necessárias para geração das chaves e criptografia/descriptografia das mensagens.

## Estrutura

```text
Atividade-RSA-FESA/
├── Scripts/
│   ├── Client.py
│   └── server.py
└── README.md
```

### Client.py

Responsável por:

* Gerar o par de chaves RSA do cliente;
* Conectar ao servidor utilizando TCP;
* Enviar a chave pública para o servidor;
* Receber a chave pública do servidor;
* Criptografar a mensagem utilizando a chave pública do servidor;
* Enviar a mensagem cifrada;
* Receber a resposta do servidor;
* Descriptografar a resposta utilizando sua chave privada;
* Calcular o RTT (Round Trip Time) da comunicação.

O cliente utiliza a mensagem definida na atividade:

```text
the information security is of significant importance to ensure the privacy of communications
```

A mensagem é convertida para um inteiro antes da operação RSA e depois convertida novamente para bytes para ser enviada pelo socket.

### server.py

Responsável por:

* Inicializar o servidor TCP na porta `1300`;
* Gerar o par de chaves RSA do servidor;
* Receber a chave pública do cliente;
* Enviar sua própria chave pública;
* Receber e descriptografar a mensagem;
* Converter a mensagem para letras maiúsculas;
* Criptografar a resposta utilizando a chave pública do cliente;
* Enviar a resposta de volta ao cliente.

O processamento da mensagem é feito convertendo os dados recebidos para inteiro e utilizando a operação de exponenciação modular do RSA.

## RSA

A geração das chaves utiliza dois números primos e calcula `N` e `φ(N)`:

```text
N = p * q

φ(N) = (p - 1) * (q - 1)
```

O expoente público utilizado é `65537`. A chave privada é obtida através do inverso modular desse valor em relação a `φ(N)`.

Para encontrar números primos grandes, o projeto utiliza o teste de primalidade de **Miller-Rabin**, executado com 40 iterações.

As chaves utilizadas pelo cliente e pelo servidor possuem 4096 bits, sendo gerados dois primos de aproximadamente 2048 bits para cada par de chaves.

## Comunicação

O funcionamento da comunicação pode ser resumido da seguinte forma:

```text
Cliente                              Servidor
   |                                    |
   |------ Chave pública -------------->|
   |<----- Chave pública ---------------|
   |                                    |
   |------ Mensagem cifrada ----------->|
   |                                    |
   |                 Descriptografa      |
   |                 e coloca em         |
   |                 maiúsculo           |
   |                                    |
   |<----- Resposta cifrada ------------|
   |                                    |
   | Descriptografa                     |
   |                                    |
```

As chaves públicas são trocadas diretamente através da conexão TCP antes do envio da mensagem.

## Requisitos

* Python 3
* Conexão de rede entre cliente e servidor

O projeto utiliza apenas módulos da biblioteca padrão do Python, como `socket`, `random` e `time`.

## Como executar

Primeiro, é necessário iniciar o servidor:

```bash
python server.py
```

Depois, executar o cliente:

```bash
python Client.py
```

O cliente está configurado para se conectar ao endereço:

```text
10.1.70.35
```

e à porta:

```text
1300
```

Esses valores estão definidos diretamente no código do cliente.

Caso o servidor esteja sendo executado em outro computador, o endereço configurado em `Client.py` deve ser alterado para o endereço IP correspondente.

## Exemplo do fluxo

O cliente envia a mensagem:

```text
the information security is of significant importance to ensure the privacy of communications
```

O servidor descriptografa a mensagem, transforma o conteúdo para letras maiúsculas e envia o resultado novamente de forma cifrada.

Ao final, o cliente descriptografa a resposta e exibe o resultado recebido, além do tempo total de ida e volta da comunicação (RTT).

## Observação

A implementação foi desenvolvida para fins acadêmicos e para demonstrar o funcionamento do RSA em uma comunicação cliente-servidor.

A implementação utiliza RSA diretamente sobre os dados convertidos para inteiros e não implementa mecanismos de padding utilizados em aplicações criptográficas reais. Portanto, o código não deve ser utilizado como solução de segurança para sistemas reais.

## Autor

Evandro Ijanques, Heytor Kyoshi, Kelvin Fernandes e William Galvonas

[GitHub](https://github.com/Ijanques)
