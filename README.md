# Central de Risco 💰
![Bacen](./images/bacen.jpeg)
## 1. Problema de negócio
O Sistema Financeiro Nacional faz a ligação entre o cliente que precisa de crédito e o cliente que tem capital a oferecer. As operações de Crédito são registradas na Central de Risco do Banco Central do Brasil (SCR).
O Mercado de Crédito precisa reduzir o risco de inadimplência e para alcançar esse objetivo é preciso conhecer o cliente/devedor. 

## 2. Premissas do negócio
Premissa 1 - Inadimplência:
Calcula-se pela divisão do valor da carteira das operações de crédito com alguma parcela em atraso acima de 90 dias pelo valor da carteira de todas as operações.

Premissa 2 - São registrados no SCR:
* Empréstimos e financiamentos;
* Adiantamentos;
* Operações de arrendamento mercantil;
* Coobrigações e garantias prestadas;
* Compromissos de crédito não canceláveis;
* Operações com instrumentos de pagamento pós-pagos;
* Outras operações ou contratos com características de crédito reconhecidas pelo BC.

Premissa 3 - A empresa é um agente financeiro de crédito.

## 3. Estratégia da solução
Foi criado um Painel com a demonstração gráfica das segmentações dos dados.
Os dados utilizados na solução possuem 4 meses (Janeiro, Fevereiro, Março, Abril e Maio de 2023) de informações disponibilizados na Central de Dados abertos do Banco Central do Brasil e correspondem a toda a carteira de crédito do SFN (foi utilizada a biblioteca pandas com a função sample para gerar uma amostra a partir dos dados e permitir a hospedagem no GitHub).
As informações são enviadas mensalmente pelos agentes financeiros registrados.  No conjunto foram separadas as visões do Cliente Pessoa Física e Cliente Pessoa Jurídica pois cada um tem suas especificidades. Ambos segmentados em Categorias (ou Dimensões) como uma visão do mês escolhido além de analisados ao longo do período disponível:
#### 1 - Indicadores % por Estado (UF) de Maior, Menor Inadimplência e a Média Nacional
#### 2 - Comparativo das Carteiras Ativa e de Inadimplência por Modalidade de Crédito
#### 3 - Comparativo das Carteiras Ativa e de Inadimplência por Ocupação do Cliente ou Atividade Principal em caso de pessoa Jurídica
#### 4 - Visualização da inadimplência média em todos os Estados do país
#### 5 - Comparativo da Inadimplência média dos estados de GO / RJ / SP ao longo dos 5 meses
#### 6 - Comparativo da Inadimplência média dos estados de GO / RJ / SP ao longo dos 5 meses segmentada por ocupação

## 4. Top Insights de dados
* Os dados demonstraram que a Carteira de Crédito do Cliente pessoa física é substancial quando a modalidade é Habitacional mas a inadimplência relativa é mais relevante na Modalidade Cartão de Crédito.

* A carteira do Cliente Pessoa Jurídica tem maior representatividade na modalidade Capital de Giro no entanto a inadimplência relativa de maior volume é na modalidade Financiamento de Infraestrutura/desenvolvimento e outros créditos.

* O Estado de maior inadimplência no mês de Maio foi RJ com 8,21% (Foram somados os valores da Carteira inadimplida e divididos pela soma dos valores da Carteira Ativa e pelo total de clientes, daquele estado ), enquanto o de menor inadimplência no mesmo período foi MT com 1,68%

## 5. O produto final do projeto
O painel está disponível no endereço: 
https://centralderisco.streamlit.app/

## 6. Conclusão
O objetivo desse projeto foi demonstrar de forma gráfica a carteira de crédito, traçando um perfil de cliente tomador de crédito. 

## 7. Próximos passos:
1- Inclusão de Filtro por UF

2- Inclusão de visualizações usando outras dimensões (porte)

3- Separação das visualizações em Abas:
 - Aba Gráficos por Modalidade Ocupação Porte considerando o mês filtrado;
 - Aba Gráficos com Evolução mês a mês da Inadimplência, Média, Desvio Padrão, considerar dimensão com até 5 categorias
 - Aba com Filtros por Estado com inadimplência Média.
