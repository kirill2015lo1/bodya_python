"""
Модуль визуализации семантической сети
Создает графическое представление базы знаний
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import networkx as nx
from semantic_network import SemanticNetwork, create_medical_knowledge_base


class NetworkVisualizer:
    """
    Визуализатор семантической сети
    """
    
    def __init__(self, knowledge_base: SemanticNetwork):
        """
        Инициализация визуализатора
        
        Args:
            knowledge_base: База знаний для визуализации
        """
        self.kb = knowledge_base
        
        # Цвета для разных типов узлов
        self.node_colors = {
            "category": "#FFB6C1",      # Светло-розовый
            "disease": "#FF6B6B",       # Красный
            "symptom": "#4ECDC4",       # Бирюзовый
            "treatment": "#95E1D3",     # Светло-зеленый
            "concept": "#F3A683"        # Оранжевый
        }
        
        # Цвета для разных типов связей
        self.edge_colors = {
            "является_подтипом": "#2C3E50",    # Темно-синий
            "имеет_симптом": "#E74C3C",        # Красный
            "лечится": "#27AE60",              # Зеленый
            "default": "#7F8C8D"               # Серый
        }
        
        # Стили для разных типов связей
        self.edge_styles = {
            "является_подтипом": "solid",
            "имеет_симптом": "dashed",
            "лечится": "dotted",
            "default": "solid"
        }
    
    def create_graph(self) -> nx.DiGraph:
        """
        Создать граф NetworkX из семантической сети
        
        Returns:
            Направленный граф
        """
        G = nx.DiGraph()
        
        # Добавить узлы
        for node_name, node_attrs in self.kb.nodes.items():
            G.add_node(node_name, **node_attrs)
        
        # Добавить ребра
        for source, relation, target in self.kb.relations:
            G.add_edge(source, target, relation=relation)
        
        return G
    
    def visualize_full_network(self, output_file: str = "semantic_network_full.png",
                              figsize: tuple = (20, 16)):
        """
        Визуализировать полную семантическую сеть
        
        Args:
            output_file: Имя файла для сохранения
            figsize: Размер фигуры
        """
        G = self.create_graph()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Использовать иерархический layout
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # Группировка узлов по типам
        node_types = {}
        for node in G.nodes():
            node_type = G.nodes[node].get('type', 'concept')
            if node_type not in node_types:
                node_types[node_type] = []
            node_types[node_type].append(node)
        
        # Отрисовка узлов по типам
        for node_type, nodes in node_types.items():
            color = self.node_colors.get(node_type, self.node_colors['concept'])
            nx.draw_networkx_nodes(G, pos, nodelist=nodes,
                                  node_color=color,
                                  node_size=3000,
                                  alpha=0.9,
                                  ax=ax)
        
        # Группировка ребер по типам отношений
        edge_types = {}
        for u, v, data in G.edges(data=True):
            relation = data.get('relation', 'default')
            if relation not in edge_types:
                edge_types[relation] = []
            edge_types[relation].append((u, v))
        
        # Отрисовка ребер по типам
        for relation, edges in edge_types.items():
            color = self.edge_colors.get(relation, self.edge_colors['default'])
            style = self.edge_styles.get(relation, self.edge_styles['default'])
            nx.draw_networkx_edges(G, pos, edgelist=edges,
                                  edge_color=color,
                                  style=style,
                                  width=2,
                                  alpha=0.6,
                                  arrows=True,
                                  arrowsize=20,
                                  arrowstyle='->',
                                  connectionstyle='arc3,rad=0.1',
                                  ax=ax)
        
        # Подписи узлов
        nx.draw_networkx_labels(G, pos,
                               font_size=8,
                               font_weight='bold',
                               font_family='sans-serif',
                               ax=ax)
        
        # Легенда для типов узлов
        node_legend = []
        for node_type, color in self.node_colors.items():
            if node_type in node_types:
                patch = mpatches.Patch(color=color, label=node_type)
                node_legend.append(patch)
        
        # Легенда для типов связей
        edge_legend = []
        for relation, color in self.edge_colors.items():
            if relation in edge_types:
                style = self.edge_styles.get(relation, 'solid')
                patch = mpatches.Patch(color=color, label=relation, linestyle=style)
                edge_legend.append(patch)
        
        # Добавить легенды
        legend1 = ax.legend(handles=node_legend, loc='upper left', 
                          title='Типы узлов', fontsize=10)
        ax.add_artist(legend1)
        ax.legend(handles=edge_legend, loc='upper right',
                 title='Типы связей', fontsize=10)
        
        ax.set_title("Семантическая сеть: Медицинская диагностика",
                    fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Полная визуализация сохранена в {output_file}")
        plt.close()
    
    def visualize_disease_symptoms(self, output_file: str = "semantic_network_diseases.png",
                                   figsize: tuple = (16, 12)):
        """
        Визуализировать связи заболеваний и симптомов
        
        Args:
            output_file: Имя файла для сохранения
            figsize: Размер фигуры
        """
        G = self.create_graph()
        
        # Фильтровать только заболевания, симптомы и их связи
        diseases = [n for n in G.nodes() if G.nodes[n].get('type') == 'disease']
        symptoms = [n for n in G.nodes() if G.nodes[n].get('type') == 'symptom']
        
        subgraph_nodes = diseases + symptoms
        subgraph = G.subgraph(subgraph_nodes)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Двудольный layout
        pos = {}
        
        # Заболевания слева
        y_step = 1.0 / (len(diseases) + 1)
        for i, disease in enumerate(diseases):
            pos[disease] = (0, 1 - (i + 1) * y_step)
        
        # Симптомы справа
        y_step = 1.0 / (len(symptoms) + 1)
        for i, symptom in enumerate(symptoms):
            pos[symptom] = (2, 1 - (i + 1) * y_step)
        
        # Отрисовка узлов
        nx.draw_networkx_nodes(subgraph, pos, nodelist=diseases,
                              node_color=self.node_colors['disease'],
                              node_size=3000,
                              alpha=0.9,
                              ax=ax)
        
        nx.draw_networkx_nodes(subgraph, pos, nodelist=symptoms,
                              node_color=self.node_colors['symptom'],
                              node_size=3000,
                              alpha=0.9,
                              ax=ax)
        
        # Отрисовка ребер
        nx.draw_networkx_edges(subgraph, pos,
                              edge_color=self.edge_colors['имеет_симптом'],
                              style='dashed',
                              width=2,
                              alpha=0.6,
                              arrows=True,
                              arrowsize=20,
                              arrowstyle='->',
                              connectionstyle='arc3,rad=0.1',
                              ax=ax)
        
        # Подписи
        nx.draw_networkx_labels(subgraph, pos,
                               font_size=9,
                               font_weight='bold',
                               ax=ax)
        
        # Легенда
        disease_patch = mpatches.Patch(color=self.node_colors['disease'], 
                                      label='Заболевания')
        symptom_patch = mpatches.Patch(color=self.node_colors['symptom'],
                                      label='Симптомы')
        ax.legend(handles=[disease_patch, symptom_patch],
                 loc='upper center', fontsize=12)
        
        ax.set_title("Связи: Заболевания → Симптомы",
                    fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Визуализация заболеваний и симптомов сохранена в {output_file}")
        plt.close()
    
    def visualize_hierarchy(self, output_file: str = "semantic_network_hierarchy.png",
                           figsize: tuple = (14, 10)):
        """
        Визуализировать иерархию категорий и заболеваний
        
        Args:
            output_file: Имя файла для сохранения
            figsize: Размер фигуры
        """
        G = self.create_graph()
        
        # Фильтровать только категории, заболевания и связи "является_подтипом"
        categories = [n for n in G.nodes() if G.nodes[n].get('type') == 'category']
        diseases = [n for n in G.nodes() if G.nodes[n].get('type') == 'disease']
        
        # Создать подграф с иерархическими связями
        H = nx.DiGraph()
        for node in categories + diseases:
            H.add_node(node, **G.nodes[node])
        
        for u, v, data in G.edges(data=True):
            if data.get('relation') == 'является_подтипом' and u in H and v in H:
                H.add_edge(u, v, **data)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Иерархический layout
        try:
            pos = nx.nx_agraph.graphviz_layout(H, prog='dot')
        except:
            # Если graphviz не установлен, использовать spring layout
            pos = nx.spring_layout(H, k=3, iterations=50)
        
        # Отрисовка узлов
        nx.draw_networkx_nodes(H, pos, nodelist=categories,
                              node_color=self.node_colors['category'],
                              node_size=4000,
                              alpha=0.9,
                              ax=ax)
        
        nx.draw_networkx_nodes(H, pos, nodelist=diseases,
                              node_color=self.node_colors['disease'],
                              node_size=3000,
                              alpha=0.9,
                              ax=ax)
        
        # Отрисовка ребер
        nx.draw_networkx_edges(H, pos,
                              edge_color=self.edge_colors['является_подтипом'],
                              width=2.5,
                              alpha=0.7,
                              arrows=True,
                              arrowsize=25,
                              arrowstyle='->',
                              ax=ax)
        
        # Подписи
        nx.draw_networkx_labels(H, pos,
                               font_size=10,
                               font_weight='bold',
                               ax=ax)
        
        # Легенда
        category_patch = mpatches.Patch(color=self.node_colors['category'],
                                       label='Категории')
        disease_patch = mpatches.Patch(color=self.node_colors['disease'],
                                      label='Заболевания')
        ax.legend(handles=[category_patch, disease_patch],
                 loc='upper center', fontsize=12)
        
        ax.set_title("Иерархия категорий и заболеваний",
                    fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Визуализация иерархии сохранена в {output_file}")
        plt.close()
    
    def visualize_all(self):
        """Создать все визуализации"""
        print("Создание визуализаций семантической сети...")
        print()
        
        self.visualize_full_network()
        self.visualize_disease_symptoms()
        self.visualize_hierarchy()
        
        print()
        print("Все визуализации созданы успешно!")


def main():
    """Создать визуализации для медицинской базы знаний"""
    print("=" * 60)
    print("ВИЗУАЛИЗАЦИЯ СЕМАНТИЧЕСКОЙ СЕТИ")
    print("=" * 60)
    print()
    
    # Создать базу знаний
    kb = create_medical_knowledge_base()
    
    # Создать визуализатор
    visualizer = NetworkVisualizer(kb)
    
    # Создать все визуализации
    visualizer.visualize_all()


if __name__ == "__main__":
    main()

