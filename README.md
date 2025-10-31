# Formula 1 Data Engineering Project

Este repositório acompanha o projeto prático do curso **Azure Databricks & Spark For Data Engineers: Hands-on Project** ministrado por Ramesh Retnasamy.  
O objetivo é aplicar habilidades de engenharia de dados em uma estrutura de lakehouse usando dados da categoria de automobilismo (Fórmula 1) como cenário de estudo, através do Azure Databricks, Delta Lake e Azure Data Factory com foco em ingestão, transformação, governança e visualização.

---

## Visão Geral  
Principais componentes 
- Arquitetura de dados moderna: desde o armazenamento em Azure Data Lake Storage Gen2 até a camada de lakehouse com Delta Lake.  
- Uso de PySpark e Spark SQL para ingestão, limpeza e transformação de dados brutos (CSV/JSON) em tabelas gerenciadas.  
- Criação de pipelines no Azure Data Factory para orquestração de notebooks e cargas incrementais.  
- Implementação de governança com Unity Catalog (metastore + segurança de acesso) para controle de dados.  
- Foco em um cenário real: dados históricos da Fórmula 1 (por piloto, corrida, equipe, etc.).  

---

## Estrutura do Repositório  
- `raw/` – Dados brutos originais importados (CSV, JSON).  
- `ingestion/` – Notebooks ou scripts responsáveis pela ingestão e upload para o Data Lake.  
- `transformation/` – Notebooks ou scripts de limpeza, transformação e criação de tabelas Delta.  
- `demo/` – Exemplos de dashboards ou relatórios finais.  
- `includes/`, `utils/` – Funções auxiliares, configurações reutilizáveis.  
- `set-up/` – Arquivos de configuração ou instruções para provisionar recursos no Azure.  
- `uc-mini-project/` – Projeto paralelo para a parte de Unity Catalog / governança. 
