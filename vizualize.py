# Шаг 1: Установка необходимых библиотек
# Если у вас еще не установлены pyvis и networkx, раскомментируйте и выполните следующую строку:
# !pip install pyvis networkx

# Шаг 2: Импорт библиотек
import json
from pyvis.network import Network
import networkx as nx
import random


def create_graph(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    # Шаг 4: Создание графа с использованием NetworkX
    G = nx.Graph()

    # Добавляем узлы и ребра
    for user in data:
        user_id = user["id"]
        full_name = f"{user['first_name']} {user['last_name']}"

        # Проверяем, существует ли узел уже, чтобы избежать перезаписи атрибутов
        if user_id not in G:
            G.add_node(
                user_id, label=full_name, title=full_name
            )  # Добавляем узел с меткой и заголовком
        else:
            # Если узел уже существует, обновляем метку и заголовок
            G.nodes[user_id]["label"] = full_name
            G.nodes[user_id]["title"] = full_name

        parent_id = user["parent_friend_id"]
        if parent_id:
            # Добавляем центральный узел, если его еще нет
            if parent_id not in G:
                G.add_node(
                    parent_id, label="Центральный Друг", title="Центральный Друг"
                )
            # Добавляем ребро между пользователем и родительским другом
            G.add_edge(user_id, parent_id)

    # Шаг 5: Определение лепестков и назначение цветов
    # Лепестки — узлы с степенью 1
    leaf_nodes = [node for node, degree in G.degree() if degree == 1]

    # Функция для генерации случайного цвета в HEX формате
    def generate_random_color():
        """Генерирует случайный цвет в формате HEX."""
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # Назначаем цвет и размер каждому узлу
    for node in G.nodes():
        if node in leaf_nodes:
            G.nodes[node]["color"] = "blue"  # Лепестки окрашены в голубой
        else:
            G.nodes[node]["color"] = (
                generate_random_color()
            )  # Остальные узлы случайные цвета

        G.nodes[node]["size"] = 15  # Можно настроить размер узлов по необходимости
        # Добавляем всплывающую подсказку с дополнительной информацией
        G.nodes[node]["title"] = (
            f"Имя: {G.nodes[node].get('label', 'Неизвестно')}<br>ID: {node}"
        )

    # Шаг 6: Создание интерактивного графа с использованием Pyvis
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

    # Шаг 7: Сохранение графа как HTML-файла
    output_path = "friend_graph.html"
    net.show(output_path)
    print(f"Граф сохранен как {output_path}")


if __name__ == "__main__":
    import sys

    filepath = sys.argv[1]
    create_graph(filepath)
