# Comparação de Visualização de Grafos em Streamlit

Este projeto é uma aplicação baseada em Streamlit projetada para comparar e avaliar diferentes bibliotecas de visualização de grafos baseadas em Python e JavaScript. Ele fornece uma visão lado a lado dos mesmos dados de rede em várias ferramentas populares.

## 🚀 Funcionalidades

- **Controles Interativos**: Personalize cores, tamanhos e rótulos dos nós dinamicamente via barra lateral.
- **Filtragem**: Alterne a visibilidade para diferentes tipos de nós (ex: Person, Movie).
- **Múltiplos Motores de Visualização**:
  - **PyVis**: Redes interativas poderosas baseadas em Python.
  - **st_link_analysis**: Componente Streamlit especializado para análise de links.
  - **Cytoscape**: Visualização baseada em JS altamente personalizável com layouts especializados e arestas curvas.
  - **NVL (neo4j-viz)**: Integração usando a biblioteca `neo4j-viz` para visualizações padrão no estilo Neo4j.

## 🛠️ Stack Tecnológica & Dependências

O projeto utiliza as seguintes bibliotecas:

- **Streamlit**: framework da aplicação.
- **NetworkX**: Estrutura de dados de grafo e gerenciamento.
- **PyVis**: Visualização de rede interativa.
- **st-link-analysis**: Componente Streamlit para análise de grafos.
- **st-cytoscape**: Componente Streamlit para Cytoscape.js.
- **neo4j-viz**: Biblioteca Python para renderizar grafos no estilo Neo4j.

## 📦 Instalação

Antes de executar a aplicação, certifique-se de ter as dependências necessárias instaladas:

```bash
pip install streamlit networkx pyvis st-link-analysis st-cytoscape neo4j-viz
```

## 🏃 Como Executar

Navegue até o diretório do projeto e execute o seguinte comando:

```bash
streamlit run app.py
```

## ⚙️ Configuração

Use a **Barra Lateral (Sidebar)** para:
- Ajustar **Cor** e **Tamanho** para diferentes categorias de nós.
- Filtrar nós por **Tipo** (ex: Mostrar/Esconder Movie).
- Escolher o campo de **Legenda do Nó (Caption)** (ex: name, id ou type).

## 📄 Licença

Este projeto é para fins educacionais e de teste.
