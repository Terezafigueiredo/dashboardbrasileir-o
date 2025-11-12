📊 Dashboard do Campeonato Brasileiro (2018-2022)

Este projeto apresenta análises de Big Data com PySpark sobre o Campeonato Brasileiro - Série A (2018-2022).

👉 O dashboard interativo está disponível online:  
[🔗 Acesse aqui](https://dashboardbrasileir-o-ec4cklcnrvszlbswf6nytb.streamlit.app/)

📊 Análise de Dados do Campeonato Brasileiro (2018-2022) com PySpark
Este repositório apresenta um projeto acadêmico desenvolvido na Universidade Estácio de Sá, na disciplina Tópicos de Big Data em Python. O objetivo é aplicar conceitos de Big Data e Business Intelligence (BI) utilizando Apache Spark e Python, explorando dados do Campeonato Brasileiro - Série A (2018-2022).

🚀 Objetivos do Projeto
Demonstrar a aplicação prática de técnicas de limpeza, filtragem, agregação e redução de dados distribuídos.

Construir indicadores de desempenho esportivo (KPIs) relevantes para análises.

Integrar o pipeline de dados com ferramentas de visualização e BI.

🛠️ Ferramentas Utilizadas
Jupyter Notebook → ambiente interativo para programação e análise.

Python 3 → manipulação e transformação dos dados.

PySpark (Spark SQL) → processamento distribuído em larga escala.

Pandas → conversão dos dados tratados em Spark para análises complementares e exportação em CSV.

📂 Estrutura do Projeto
Criação da Sessão Spark

Inicialização da SparkSession para operações distribuídas.

Leitura e Inspeção do Dataset

Dataset obtido do portal Transfermarkt.

Carregado em formato CSV com inferSchema=True.

Limpeza e Redução de Dados

Exclusão de colunas irrelevantes.

Remoção de valores nulos.

Seleção Temporal (2018-2022)

Filtragem dos dados para incluir apenas as temporadas de 2018 a 2022.

Exportação dos Dados Filtrados

Conversão para Pandas e exportação em CSV.

Análises Exploratórias

Identificação dos anos disponíveis.

Contagem de partidas por temporada.

Criação de Indicador de Resultado

Coluna resultado_mandante (Vitória, Empate, Derrota).

Estrutura e Análises de Resultado

Distribuição de vitórias, empates e derrotas.

Cálculo de Médias de Gols por Time

KPIs de gols marcados e sofridos por mandante.

📈 Resultados Obtidos
Anos de campeonatos disponíveis.

Quantidade de partidas por temporada.

Proporção de vitórias, empates e derrotas.

Médias de gols marcados e sofridos por time mandante.

Essas métricas podem ser integradas em dashboards com ferramentas como Tableau ou Matplotlib.

🏁 Conclusão
O projeto demonstrou a eficiência do PySpark no processamento massivo de dados esportivos, transformando grandes volumes de informações em indicadores úteis para análise de desempenho. A integração com Python/Pandas permitiu análises complementares e exportação dos resultados, mostrando a força do pipeline implementado.



