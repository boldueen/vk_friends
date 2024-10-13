import json
import random
import time

from pyvis.network import Network
import networkx as nx


def generate_visual_graph(data: list[dict]) -> str:
    # with open("graph.json", "r") as f:
    #     data = json.load(f)

    G = nx.Graph()

    # Добавляем узлы и ребра
    for user in data:
        user_id = user["id"]
        full_name = f"{user['first_name']} {user['last_name']}"
        G.add_node(
            user_id, label=full_name, title=full_name
        )  # Добавляем узел с меткой и заголовком

        parent_id = user["parent_friend_id"]
        if parent_id:
            G.add_edge(
                user_id, parent_id
            )  # Добавляем ребро между пользователем и родительским другом

    # Добавляем центральный узел, если он не был добавлен ранее
    central_id = 396854328
    if central_id not in G:
        G.add_node(central_id, label="Центральный Друг", title="Центральный Друг")

    # Лепестки — узлы с степенью 1
    leaf_nodes = [node for node, degree in G.degree() if degree == 1]

    # Функция для генерации случайного цвета в HEX формате
    def generate_random_color():
        """Генерирует случайный цвет в формате HEX."""
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # Назначаем цвет и размер каждому узлу
    for node in G.nodes():
        if node in leaf_nodes:
            G.nodes[node]["color"] = "lightblue"  # Лепестки окрашены в голубой
        else:
            G.nodes[node]["color"] = (
                generate_random_color()
            )  # Остальные узлы случайные цвета

        G.nodes[node]["size"] = 15  # Можно настроить размер узлов по необходимости
        G.nodes[node]["title"] = (
            f"Имя: {G.nodes[node]['label']}<br>ID: {node}"  # Всплывающая подсказка
        )

    # Создаем объект Network из Pyvis
    net = Network(
        height="750px",
        width="100%",
        notebook=True,
        bgcolor="#ffffff",
        font_color="black",
    )

    # Настройки визуализации (можно настроить по желанию)
    net.barnes_hut()
    net.set_options("""
    var options = {
    "nodes": {
        "font": {
        "size": 14
        },
        "shape": "dot",
        "scaling": {
        "min": 10,
        "max": 30
        }
    },
    "edges": {
        "color": {
        "inherit": true
        },
        "smooth": false
    },
    "physics": {
        "barnesHut": {
        "gravitationalConstant": -8000,
        "centralGravity": 0.3,
        "springLength": 250,
        "springConstant": 0.001,
        "damping": 0.09,
        "avoidOverlap": 0
        },
        "minVelocity": 0.75
    }
    }
    """)

    # Передаем NetworkX граф в Pyvis Network
    net.from_nx(G)

    output_path = f"{int(time.time())}_friend_graph.html"
    net.show(output_path)
    print(f"Граф сохранен как {output_path}")
    return output_path
