# prova-sistemas-distribuidos

# Prova 2 — Sistemas Distribuídos

- **Nome:** Igor Soares Da Silva
- **Professora:** Simone Tatiane do Canto
- **Data:** 18/11/2026
 
## Correções Realizadas (Etapa 3)

- **Problema A — Concorrência:** Alterei `MAXIMO_SIMULTANEO` de `3` para `2` para que o semáforo permita no máximo dois pedidos em processamento simultâneo, conforme a regra da empresa.
- **Problema B — Replicação e Consistência:** Na função `sicronizar()`, alterei `replica["estoque"] = replica["estoque"]` para `replica["estoque"] = principal["estoque"]` (dentro de `with trava:`), fazendo a réplica receber o valor atualizado do estoque principal após o processamento dos pedidos.
- **Problema C — Tolerância a Falhas:** Na função `consultar_estoque()`, corrigi a segunda condição de `if principal["online"]:` para `if replica["online"]:`, permitindo que o sistema consulte a réplica quando o servidor principal estiver indisponível.

## Análise Técnica (Etapa 5)

**Questão 1. Qual é a função do semáforo no processamento dos pedidos?**
O semáforo controla quantas threads podem executar o bloco de processamento de pedidos ao mesmo tempo, limitando a concorrência ao valor configurado (`MAXIMO_SIMULTANEO = 2`) para respeitar a capacidade definida.

**Questão 2. Por que é necessário sincronizar os dados entre o servidor principal e a réplica?**
A sincronização mantém a consistência dos dados entre os servidores. Sem ela, a réplica continua com o estoque antigo após as alterações no servidor principal, causando divergência de informações.

**Questão 3. O que significa tolerância a falhas e como ela aparece neste programa?**
Tolerância a falhas é a capacidade do sistema de continuar funcionando mesmo quando ocorre falha em algum componente. Neste programa, ela aparece quando `principal["online"]` passa a `False` na simulação de falha e `consultar_estoque()` continua retornando o estoque através da réplica.

**Questão 4. Para que serve o Lock no programa e como o controle de acesso aos recursos ajuda a prevenir problemas de concorrência?**
O `Lock` (`trava`) garante exclusão mútua, permitindo que apenas uma thread por vez leia ou altere dados compartilhados (como o estoque e a lista de pedidos confirmados). Isso evita condições de corrida e inconsistências quando várias threads rodam simultaneamente.

**Questão 5. Considerando a sequência de eventos, a sincronização do estoque deve acontecer antes ou depois do processamento dos pedidos? Explique a relação de causalidade.**
A sincronização deve acontecer **depois** do processamento dos pedidos. Pela relação de causalidade, o processamento do pedido no servidor principal é o evento que altera o estoque e *causa* o novo estado; sincronizar antes copiaria o valor antigo antes da atualização ocorrer.


Seção 1: Situação-problema
O sistema apresenta três falhas principais: limitação incorreta de concorrência permitindo três pedidos simultâneos em vez de dois (Problema A), falha na replicação em que a réplica não recebia o estoque atualizado do servidor principal (Problema B), e um erro na função de consulta que impedia a utilização da réplica quando o servidor principal ficava indisponível (Problema C).

Seção 2: Primeira execução
Na primeira execução, o sistema iniciou com o limite simultâneo incorreto de 3 pedidos, a réplica permaneceu com o valor estático de estoque após a execução e a consulta após a falha simulada falhou devido à lógica incorreta de checagem do servidor online.

Seção 3: Problema A — Concorrência
Qual problema foi identificado?
O programa estava configurado com o limite de 3 pedidos em processamento simultâneo (MAXIMO_SIMULTANEO = 3), enquanto a regra estabelecida pela empresa era de no máximo 2 pedidos simultâneos.

Qual alteração foi realizada?
A variável MAXIMO_SIMULTANEO foi alterada de 3 para 2, ajustando o semáforo para restringir corretamente o acesso simultâneo de threads.

Seção 4: Problema B — Replicação e Consistência
Qual problema foi identificado?
A função sicronizar() não atualizava o estoque da réplica com o valor atualizado do servidor principal, pois estava atribuindo o próprio valor da réplica (replica["estoque"] = replica["estoque"]).

Qual alteração foi realizada?
Na função sicronizar(), alterei a atribuição para replica["estoque"] = principal["estoque"] protegida por trava, garantindo que a réplica receba o estoque correto após o processamento.

Seção 5: Problema C — Tolerância a falhas
Qual problema foi identificado?
A função consultar_estoque() repetia a verificação if principal["online"]: em vez de verificar o estado da réplica, impedindo o redirecionamento da consulta quando o servidor principal ficava indisponível.

Qual alteração foi realizada?
Na função consultar_estoque(), corrigi a segunda condição para if replica["online"]:, permitindo que o sistema consulte e retorne os dados da réplica quando o servidor principal falhar.

Seção 6: Validação do programa
Descreva os resultados observados após as três correções.
Após as alterações, o limite de processamento respeitou o máximo de dois pedidos simultâneos, o estoque principal foi decrementado corretamente após o processamento dos três pedidos, a réplica sincronizou com sucesso o novo valor de estoque e, na simulação de falha, o sistema realizou com sucesso a consulta recorrendo à réplica.

Seção 7: Análise técnica
Questão 1
O semáforo controla quantas threads podem executar o bloco de processamento de pedidos ao mesmo tempo, limitando a concorrência ao valor configurado (MAXIMO_SIMULTANEO = 2) para respeitar a capacidade definida.

Questão 2
A sincronização mantém a consistência dos dados entre os servidores. Sem ela, a réplica continua com o estoque antigo após as alterações no servidor principal, causando divergência de informações.

Questão 3
Tolerância a falhas é a capacidade do sistema de continuar funcionando mesmo quando ocorre falha em algum componente. Neste programa, ela aparece quando principal["online"] passa a False na simulação de falha e consultar_estoque() continua retornando o estoque através da réplica.

Questão 4
O Lock (trava) garante exclusão mútua, permitindo que apenas uma thread por vez leia ou altere dados compartilhados (como o estoque e a lista de pedidos confirmados). Isso evita condições de corrida e inconsistências quando várias threads rodam simultaneamente.

Questão 5
A sincronização deve acontecer depois do processamento dos pedidos. Pela relação de causalidade, o processamento do pedido no servidor principal é o evento que altera o estoque e causa o novo estado; sincronizar antes copiaria o valor antigo antes da atualização ocorrer.

Seção 8: Conclusão
Esta atividade prática permitiu compreender na prática o funcionamento de sistemas distribuídos, aplicando conceitos essenciais como controle de concorrência com semáforos e locks, replicação e consistência de dados entre nós, e estratégias de tolerância a falhas para garantir a alta disponibilidade.
