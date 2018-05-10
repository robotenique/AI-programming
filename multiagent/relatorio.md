---
title:  'Relatório do EP2 - Inteligência Artificial'
author:
- 'Juliano Garcia de Oliveira Nº USP: 9277086'
geometry: margin=3cm
date: "14 de Maio, 2018"
output:
  rmarkdown::pdf_document:
    fig_caption: yes        
    includes:  
      in_header: figure_placement.tex

---

[//]: # pandoc -s -o teste.pdf relatorio.md  && evince teste.pdf
### Questões

1. (reativo) Como é o desempenho do seu agente? É provável que muitas vezes ele morra com 2 fantasmas no tabuleiro default, a não ser que a sua função de avaliação seja muito boa.

    A função é razoávelmente boa, sendo que testando 100 vezes no layout padrão (com 2 fantasmas), ele vence 80% das vezes,
    e testando 100 vezes no layout 'trickyLayout', com 4 fantasmas, ele vence 42% das vezes.
    Os comandos que usei para fazer estes são, respectivamente:

    ```bash
    $ python pacman.py -p ReflexAgent -k 2 -f -q -n 100
    $ python pacman.py -p ReflexAgent -k 4 -l trickyClassic -f -q -n 100
    ```

2. (minimax) Por que o Pac-Man corre para o fantasma mais próximo neste caso?

    Porque neste caso, o Pac-Man começa com a pontuação 0, e a pontuação de quando ele perde é a pontuação atual -500. Portando, ao fazer o Minimax, quanto mais tempo ele ficar jogando porém morrer, menor vai ser a pontuação, mas ele precisa maximizar a pontuação, então correr para o fantasma mais próximo garante que essa pontuação que ele perderia inicialmente por ficar andando no tabuleiro seja a menor possível, para que a pontuação final seja a maior possível.


3. (minimax) Por que o agente reativo tem mais problemas para ganhar que o agente minimax?

    Porque o agente reativo só consegue levar em conta uma única configuração ação-estado, enquanto no Minimax, além de conseguir olhar vários estados e pegar o melhor (dependendo da profundidade), no Minimax também é levado em conta as ações que o jogadores adversários podem fazer (MIN), o que dá um melhor "controle" do jogo, e dá a estratégia ótima caso todos os jogadores estejam jogando otimamente. Mas isso depende bastante da função do agente reativo, no meu caso, várias vezes o agente reativo ganha mais do que o Minimax (com profundidade 2).


4. (reativo) Que mudanças poderiam ser feitas na função de avaliação (evaluationFunction) para melhorar o comportamento do agente reativo?

    Levar em conta os possíveis movimentos dos fantasmas, quantidade de comida, possivelmente caminhos entre os fantasmas de modo a minimizar a chance de ser encurralado, limpar uma parte mais "cheia" do mapa primeiro, etc.


5. (alpha e beta)  Faça uma comparação entre os agentes Minimax e AlphaBeta em termos de tempo e número de nós explorados para profundidades 2, 3 e 4.

    Abaixo estão os resultados, podemos ver que o AlphaBeta pode melhorar bastante o tempo conforme aumenta a profundidade. Os testes dos nós foram gerados modificando o código para verificar quantas vezes a função **generateSuccessor()** for chamada.

    | Profundidade | Tempo (Minimax) | Tempo (AlphaBeta)  |
    | :-------------: |:-------------:| :-----:|
    | 2      | 2.2s   | 2.09s |
    | 3      | 5.73s  | 3.74s |
    | 4      | 60.40s | 38.55s |

    | Profundidade | Nós explorados (Minimax) | Nós explorados (AlphaBeta)  |
    | :-------------: |:-------------:| :-----:|
    | 2      |  11333  | 10230 |
    | 3      |  29325 | 20332 |
    | 4      | 278350 | 180445 |

    Dividindo os resultados do Minimax pelo AlphaBeta, temos, em ambos os casos, uma razão por volta de 1.5, na maioria dos casos.


6. (expectimax) Por que o comportamento do expectimax é diferente do minimax?

    Porque o Minimax considera que os fantasmas são jogadores ótimos, enquanto no expectimax os fantasmas são considerados como jogadores aleatórios, isto é, não estão tentando minimizar a recompensa do Pac-Man, eles apenas escolhem uma de suas ações válidas aleatoriamente, e o Expectimax usa essa informação para calcular a média ponderada de cada estado, e pegar o estado que dê o maior valor (recursivamente), e é limitado pela profundidade, assim como o Minimax.
