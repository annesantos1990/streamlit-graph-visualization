import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from st_link_analysis import NodeStyle, EdgeStyle, st_link_analysis
from st_cytoscape import cytoscape
from neo4j_viz import Node, Relationship, VisualizationGraph

st.set_page_config(layout="wide")
st.title("Comparação de Visualizações de Grafos")

# ---------------------------
# CRIANDO GRAFO
# ---------------------------

G = nx.Graph()

G.add_node(1, name="Alice", type="Person")
G.add_node(2, name="Matrix", type="Movie")
G.add_node(3, name="Bob", type="Person")

G.add_edge(1, 2, type="ACTED_IN")
G.add_edge(3, 2, type="DIRECTED")

# ---------------------------
# TIPOS DE NÓS E ARESTAS
# ---------------------------

node_types = sorted(set(data["type"] for _, data in G.nodes(data=True)))
edge_types = sorted(set(data["type"] for _, _, data in G.edges(data=True)))

# ---------------------------
# SIDEBAR – TABS
# ---------------------------

# Criar uma lista de nomes para busca antecipadamente para usar em ambas as abas
node_names = {data["name"]: str(node) for node, data in G.nodes(data=True)}

def set_search(name):
    st.session_state.node_search = name

def resetar_busca():
    st.session_state.node_search = ""

tab_estilos, tab_lista = st.sidebar.tabs(["Estilos", "Lista de Nós"])

with tab_estilos:
    st.header("Estilo dos Nós")

    node_style_map = {}

    # Ajustado para usar colunas dentro da tab
    cols_node = st.columns(len(node_types))

    for i, node_type in enumerate(node_types):
        with cols_node[i]:
            with st.popover(f"**{node_type}**"):
                color = st.color_picker(
                    "Cor",
                    "#FF5733" if node_type == "Person" else "#33C3FF",
                    key=f"{node_type}_color"
                )
                size = st.slider(
                    "Tamanho",
                    5,
                    50,
                    25,
                    key=f"{node_type}_size"
                )
            node_style_map[node_type] = {
                "color": st.session_state[f"{node_type}_color"],
                "size": st.session_state[f"{node_type}_size"]
            }

    # ---------------------------
    # ESTILO DOS VÍNCULOS
    # ---------------------------
    st.subheader("Estilo dos Vínculos")

    edge_style_map = {}
    cols_edge = st.columns(len(edge_types))

    for i, edge_type in enumerate(edge_types):
        with cols_edge[i]:
            with st.popover(f"**{edge_type}**"):
                color = st.color_picker(
                    "Cor",
                    "#AAAAAA",
                    key=f"{edge_type}_color"
                )
                width = st.slider(
                    "Espessura",
                    1,
                    10,
                    3,
                    key=f"{edge_type}_width"
                )
            edge_style_map[edge_type] = {
                "color": st.session_state[f"{edge_type}_color"],
                "width": st.session_state[f"{edge_type}_width"]
            }

    # -------------------------------------
    # Navegação
    # -------------------------------------
    st.markdown("---")
    st.subheader("Navegação")
    
    target_node_name = st.selectbox(
        "Pular para o nó:",
        [""] + list(node_names.keys()),
        key="node_search"
    )

    # Botão para limpar o foco
    st.button(
        "Limpar Foco",
        on_click=resetar_busca
    )

with tab_lista:
    st.header("Lista de Nós")
    
    # Busca rápida na lista
    search_term = st.text_input("Filtrar nós:", key="list_search_term")
    
    st.markdown("---")
    
    for node, data in G.nodes(data=True):
        if search_term.lower() in data["name"].lower() or search_term.lower() in data["type"].lower():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{data['name']}**")
                st.caption(f"Tipo: {data['type']}")
            with col2:
                # Usar on_click para evitar erro de modificação de session_state
                st.button("Jump", key=f"jump_{node}", on_click=set_search, args=(data["name"],))
            st.markdown("---")


target_id = node_names.get(target_node_name)

# =========================================================
# PYVIS
# =========================================================

st.header("1 - Visualização PyVis")

net = Network(height="450px", width="100%")

for node, data in G.nodes(data=True):

    label = data["name"]
    style = node_style_map[data["type"]]

    net.add_node(
        node,
        label=label,
        color=style["color"],
        size=style["size"]
    )

for source, target, data in G.edges(data=True):

    style = edge_style_map[data["type"]]

    net.add_edge(
        source,
        target,
        color=style["color"],
        width=style["width"],
        title=data["type"]
    )

net.save_graph("graph.html")

HtmlFile = open("graph.html", "r", encoding="utf-8")
components.html(HtmlFile.read(), height=450)

# =========================================================
# ST_LINK_ANALYSIS
# =========================================================

st.header("2 - Visualização st_link_analysis")

elements_sla = {
    "nodes": [],
    "edges": []
}

for node, data in G.nodes(data=True):

    elements_sla["nodes"].append({
        "data": {
            "id": str(node),
            "label": data["type"],
            "name": data["name"]
        }
    })

for source, target, data in G.edges(data=True):

    style = edge_style_map[data["type"]]

    elements_sla["edges"].append({
        "data": {
            "id": f"{source}-{target}",
            "label": data["type"],
            "source": str(source),
            "target": str(target),
            "color": style["color"],
            "width": style["width"]
        }
    })

node_styles_sla = [
    NodeStyle(node_type, node_style_map[node_type]["color"], "name", node_type.lower())
    for node_type in node_style_map
]

edge_styles_sla = [
    EdgeStyle(edge_type, caption="label", directed=True)
    for edge_type in edge_style_map
]

st_link_analysis(
    elements_sla,
    "cose",
    node_styles_sla,
    edge_styles_sla
)

# =========================================================
# CYTOSCAPE
# =========================================================

st.header("3 - Visualização Cytoscape")

elements_cy = []

for node, data in G.nodes(data=True):

    elements_cy.append({
        "data": {
            "id": str(node),
            "label": data["name"]
        },
        "classes": data["type"]
    })

for source, target, data in G.edges(data=True):

    elements_cy.append({
        "data": {
            "id": f"e{source}-{target}",
            "source": str(source),
            "target": str(target)
        },
        "classes": data["type"]
    })

stylesheet = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "text-valign": "bottom",
            "text-halign": "center",
            "color": "#fff"
        }
    }
]
for node_type in node_style_map:

    style = node_style_map[node_type]

    stylesheet.append({
        "selector": f"node.{node_type}",
        "style": {
            "background-color": style["color"],
            "width": style["size"],
            "height": style["size"]
        }
    })


if target_id:
    stylesheet.append({
        "selector": f"node[id = '{target_id}']",
        "style": {
            "background-color": style["color"],
            "width": style["size"] * 2,
            "height": style["size"] * 2,
            "border-width": 3,
            "border-color": "#000"
        }
    })





for edge_type in edge_style_map:

    style = edge_style_map[edge_type]

    stylesheet.append({
        "selector": f"edge.{edge_type}",
        "style": {
            "line-color": style["color"],
            "target-arrow-color": style["color"],
            "width": style["width"],
            "target-arrow-shape": "triangle",
            "curve-style": "bezier"
        }
    })

selected_cy = cytoscape(
    elements=elements_cy,
    stylesheet=stylesheet,
    layout={"name": "cose", "fit": True},
    key="graph_cy"
)

# =========================================================
# NVL
# =========================================================

st.header("4 - NVL Neo4j")

nodes_nvl = [
    Node(
        id=str(node),
        caption=data["name"],
        size=node_style_map[data["type"]]["size"]
    )
    for node, data in G.nodes(data=True)
]

relationships_nvl = [
    Relationship(
        source=str(source),
        target=str(target),
        caption=data["type"]
    )
    for source, target, data in G.edges(data=True)
]

VG = VisualizationGraph(nodes=nodes_nvl, relationships=relationships_nvl)

html = VG.render().data
components.html(str(html), height=500)