# Oathbreakers---Entrega-Intermedia-V1-e-V2-

<ins>**Explicação de ambas as versões**</ins>

Existem dois diretórios apresentados neste repositório.
A versão 1 existe apenas um socket, tanto para o broadcast como para o cliente, nesta versão acontece erros tanto do lado do cliente como do lado do servidor, "WinError 10053" do lado do servidor e "WinError 10054" do lado do cliente. Pelo que foi percebido do erro, há uma mistura de informação quando é enviado o broadcast fazendo com que exista um grande número de bytes. Ao detetar isto, o sistema operativo não permite e termina o programa. Não se conseguiu corrigir este erro.


A solução arranjada está na segunda versão do programa.
A segunda versão usa dois sockets, um para o broadcast e um para o cliente, desta maneira a informação está separada e os erros não acontecem, permitindo assim que o broadcast seja feito com sucesso.


<ins>**Explicação da ideia do jogo**</ins>


**Dados**

Existirão diferentes tipos de dados que serão guardados. Inicialmente temos três ficheiros de dados:
- classes --  Classes que podem ser escolhidos pelo jogador
    Exemplo de uma classe:
      <img width="441" height="345" alt="image" src="https://github.com/user-attachments/assets/8bdee2c9-6642-44ac-a3a2-5a41b75f318e" />

- inimigos -- Inimgos que os jogadores podem lutar
    Exemplo de um inimigo:
      <img width="274" height="145" alt="image" src="https://github.com/user-attachments/assets/48c6755c-aaa2-45b6-bef3-7782f6098949" />

- itens -- Itens que os jogadores podem encontrar ou que tenham no seu inventário
    Exemplo de um item:
      <img width="637" height="352" alt="image" src="https://github.com/user-attachments/assets/582e56b0-839a-4f63-b994-5ea1a4252d07" />

Todos estes dados são guardados em ficheiros .json.


**Execução do Jogo**

Seria um jogo cooperativo de dois jogadores. Ao iniciar, ambos os jogadores colocariam o seu nome e escolheriam uma classe (Mago, Cavaleiro, Bárbaro, (..)), todas as classes teriam as suas próprias estatísticas (vida, ataque, defesa), isto não deve ser confundido com as estatísticas do jogador (ouro, experiência) que é independente da classe que este escolheu e que só é criado quando o jogador entra no jogo, como é possível ver na imagem abaixo.

<img width="608" height="400" alt="image" src="https://github.com/user-attachments/assets/be90e845-0a66-49c8-92e9-8829ed680568" />



Após, os jogadores são colocados numa sala retangular e quadriculada (matriz), podendo estes mover-se pela sala com teclas do teclado (WASD), à medida que movem-se pela sala é atualizado as posições do jogador no servidor para que ambos consigam ver tanto a sua poisção como a do seu companheiro (broadcast). Dentro desta sala existirá alguns baús, que poderão conter itens mais fortes para melhorar as estatísticas dos jogadores, bem como salas ou casas, talvez 2 ou 3 inicialmente, onde dentro existirão inimigos que os jogadores necessitam de derrotar para conseguir ouro e outros itens. Ainda mais, talvez numa fase inicial irá implementar-se uma espécie de temporizador em que indica o tempo limite que os jogadores tenham para completar a sala final com um inimigo mais forte, caso não o cumpram, os jogadores são derrotados e o jogo termina.

A luta com os inimigos será feito inicialmente de forma algorítmica, isto é, com um algoritmo em que calcula as estatísticas dos jogadores e dos inimigos (vida, ataque, defesa, itens, etc) e dependendo de quem é mais forte calculará uma probabilidade de ganhar para ambos as partes, no entanto num fase mais avançada poderá ser feito de maneira a que os jogadores possam selecionar se desejam atacar, defender, usar itens, e assim sucessivamente, de maneira a que seja mais interativo e dinâmico dando assim aos jogadores a opção de planear a melhor maneira de derrotar o inimigo. Ao derrotar o inimigo os jogadores são removidos da sala ou casa em que foi realizada a luta e colocados de volta na sala retangular inicial, ganhando a sua recompensa, podendo novamente vasculhar a sala ou ir para uma nova sala de luta, caso percam a luta o jogo termina. A sala onde previamente aconteceu a luta fica inacessível. O inimigo dentro da sala é escolhido aleatoriamente.

Finalmente, para terminar o jogo com uma vitória para os jogadores, estes têm que entrar na casa final onde existirá, como foi mencionado anteriormente, um inimigo mais forte. Aqui a luta funcionará da mesma maneira e caso os jogadores ganhem irão receber recompensas mais fortes para uso futuro numa outra sessão do jogo e o jogo é terminado.

