# prova-sistemas-distribuidos

# Prova 2 — Sistemas Distribuídos

- **Nome:** Igor Soares Da Silva

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
