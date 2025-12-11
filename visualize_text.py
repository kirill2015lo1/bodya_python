"""
Модуль текстовой визуализации семантической сети
Создает текстовое представление базы знаний для отчета
"""

from semantic_network import SemanticNetwork, create_medical_knowledge_base
from typing import Dict, List, Set


class TextVisualizer:
    """
    Текстовый визуализатор семантической сети
    """
    
    def __init__(self, knowledge_base: SemanticNetwork):
        """
        Инициализация визуализатора
        
        Args:
            knowledge_base: База знаний для визуализации
        """
        self.kb = knowledge_base
    
    def visualize_hierarchy(self) -> str:
        """
        Визуализировать иерархию в виде дерева
        
        Returns:
            Текстовое представление иерархии
        """
        lines = []
        lines.append("=" * 70)
        lines.append("ИЕРАРХИЯ КАТЕГОРИЙ И ЗАБОЛЕВАНИЙ")
        lines.append("=" * 70)
        lines.append("")
        
        # Найти корневой узел
        root = "Заболевание"
        
        def print_tree(node: str, prefix: str = "", is_last: bool = True):
            """Рекурсивная печать дерева"""
            # Символы для рисования дерева
            connector = "└── " if is_last else "├── "
            
            # Получить информацию об узле
            node_info = self.kb.get_node(node)
            node_type = node_info.get('type', 'unknown')
            
            # Форматирование узла
            if node_type == 'category':
                node_str = f"[Категория] {node}"
            elif node_type == 'disease':
                severity = node_info.get('severity', 'неизвестно')
                node_str = f"[Заболевание] {node} (тяжесть: {severity})"
            else:
                node_str = f"{node}"
            
            lines.append(prefix + connector + node_str)
            
            # Найти дочерние узлы
            children = []
            for rel in self.kb.get_relations_to(node):
                if rel[1] == "является_подтипом":
                    children.append(rel[0])
            
            # Рекурсивно обработать детей
            for i, child in enumerate(sorted(children)):
                is_last_child = (i == len(children) - 1)
                extension = "    " if is_last else "│   "
                print_tree(child, prefix + extension, is_last_child)
        
        print_tree(root)
        lines.append("")
        
        return "\n".join(lines)
    
    def visualize_disease_symptoms(self) -> str:
        """
        Визуализировать связи заболеваний и симптомов
        
        Returns:
            Текстовое представление связей
        """
        lines = []
        lines.append("=" * 70)
        lines.append("СВЯЗИ: ЗАБОЛЕВАНИЯ → СИМПТОМЫ")
        lines.append("=" * 70)
        lines.append("")
        
        diseases = sorted(self.kb.get_all_nodes_by_type("disease"))
        
        for disease in diseases:
            lines.append(f"┌─ {disease}")
            
            # Получить симптомы
            symptoms = []
            for rel in self.kb.get_relations_from(disease):
                if rel[1] == "имеет_симптом":
                    symptoms.append(rel[2])
            
            symptoms = sorted(symptoms)
            for i, symptom in enumerate(symptoms):
                is_last = (i == len(symptoms) - 1)
                connector = "└──" if is_last else "├──"
                lines.append(f"│  {connector} {symptom}")
            
            lines.append("│")
        
        lines.append("")
        return "\n".join(lines)
    
    def visualize_disease_treatment(self) -> str:
        """
        Визуализировать связи заболеваний и методов лечения
        
        Returns:
            Текстовое представление связей
        """
        lines = []
        lines.append("=" * 70)
        lines.append("СВЯЗИ: ЗАБОЛЕВАНИЯ → МЕТОДЫ ЛЕЧЕНИЯ")
        lines.append("=" * 70)
        lines.append("")
        
        diseases = sorted(self.kb.get_all_nodes_by_type("disease"))
        
        for disease in diseases:
            lines.append(f"┌─ {disease}")
            
            # Получить методы лечения
            treatments = []
            for rel in self.kb.get_relations_from(disease):
                if rel[1] == "лечится":
                    treatments.append(rel[2])
            
            if treatments:
                treatments = sorted(treatments)
                for i, treatment in enumerate(treatments):
                    is_last = (i == len(treatments) - 1)
                    connector = "└──" if is_last else "├──"
                    lines.append(f"│  {connector} {treatment}")
            else:
                lines.append(f"│  └── (нет данных)")
            
            lines.append("│")
        
        lines.append("")
        return "\n".join(lines)
    
    def visualize_statistics(self) -> str:
        """
        Визуализировать статистику по базе знаний
        
        Returns:
            Текстовое представление статистики
        """
        lines = []
        lines.append("=" * 70)
        lines.append("СТАТИСТИКА БАЗЫ ЗНАНИЙ")
        lines.append("=" * 70)
        lines.append("")
        
        # Статистика по узлам
        node_types = {}
        for node_name, node_attrs in self.kb.nodes.items():
            node_type = node_attrs.get("type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        lines.append(f"Всего узлов: {len(self.kb.nodes)}")
        lines.append("")
        lines.append("Распределение по типам узлов:")
        for node_type in sorted(node_types.keys()):
            count = node_types[node_type]
            bar = "█" * (count * 2)
            lines.append(f"  {node_type:20s} │ {bar} {count}")
        
        lines.append("")
        
        # Статистика по связям
        relation_types = {}
        for rel in self.kb.relations:
            rel_type = rel[1]
            relation_types[rel_type] = relation_types.get(rel_type, 0) + 1
        
        lines.append(f"Всего связей: {len(self.kb.relations)}")
        lines.append("")
        lines.append("Распределение по типам связей:")
        for rel_type in sorted(relation_types.keys()):
            count = relation_types[rel_type]
            bar = "█" * (count // 2)
            lines.append(f"  {rel_type:25s} │ {bar} {count}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def visualize_nodes_list(self) -> str:
        """
        Визуализировать список всех узлов с описаниями
        
        Returns:
            Текстовое представление узлов
        """
        lines = []
        lines.append("=" * 70)
        lines.append("СПИСОК УЗЛОВ СЕМАНТИЧЕСКОЙ СЕТИ")
        lines.append("=" * 70)
        lines.append("")
        
        # Группировка по типам
        node_types = {}
        for node_name, node_attrs in self.kb.nodes.items():
            node_type = node_attrs.get("type", "unknown")
            if node_type not in node_types:
                node_types[node_type] = []
            node_types[node_type].append((node_name, node_attrs))
        
        # Вывод по типам
        type_names = {
            'category': 'КАТЕГОРИИ',
            'disease': 'ЗАБОЛЕВАНИЯ',
            'symptom': 'СИМПТОМЫ',
            'treatment': 'МЕТОДЫ ЛЕЧЕНИЯ'
        }
        
        for node_type in ['category', 'disease', 'symptom', 'treatment']:
            if node_type in node_types:
                lines.append(f"\n{type_names[node_type]}:")
                lines.append("-" * 70)
                
                for node_name, node_attrs in sorted(node_types[node_type]):
                    lines.append(f"\n• {node_name}")
                    
                    # Описание
                    if 'description' in node_attrs:
                        lines.append(f"  Описание: {node_attrs['description']}")
                    
                    # Дополнительные атрибуты
                    for key, value in node_attrs.items():
                        if key not in ['type', 'description']:
                            lines.append(f"  {key}: {value}")
        
        lines.append("")
        return "\n".join(lines)
    
    def visualize_graph_structure(self) -> str:
        """
        Визуализировать структуру графа в псевдографическом виде
        
        Returns:
            Текстовое представление графа
        """
        lines = []
        lines.append("=" * 70)
        lines.append("СТРУКТУРА СЕМАНТИЧЕСКОЙ СЕТИ (ГРАФ)")
        lines.append("=" * 70)
        lines.append("")
        lines.append("Легенда:")
        lines.append("  ───> является_подтипом")
        lines.append("  ···> имеет_симптом")
        lines.append("  ═══> лечится")
        lines.append("")
        
        # Группировка связей по типам
        relation_groups = {}
        for source, relation, target in self.kb.relations:
            if relation not in relation_groups:
                relation_groups[relation] = []
            relation_groups[relation].append((source, target))
        
        # Вывод по типам отношений
        relation_symbols = {
            'является_подтипом': '───>',
            'имеет_симптом': '···>',
            'лечится': '═══>'
        }
        
        for relation_type in ['является_подтипом', 'имеет_симптом', 'лечится']:
            if relation_type in relation_groups:
                lines.append(f"\n{relation_type.upper()}:")
                lines.append("-" * 70)
                
                for source, target in sorted(relation_groups[relation_type]):
                    symbol = relation_symbols.get(relation_type, '--->')
                    lines.append(f"  {source:30s} {symbol} {target}")
        
        lines.append("")
        return "\n".join(lines)
    
    def create_full_report(self, output_file: str = "semantic_network_report.txt"):
        """
        Создать полный отчет по семантической сети
        
        Args:
            output_file: Имя файла для сохранения
        """
        report = []
        
        report.append("╔" + "═" * 68 + "╗")
        report.append("║" + " " * 68 + "║")
        report.append("║" + "  ОТЧЕТ ПО СЕМАНТИЧЕСКОЙ СЕТИ".center(68) + "║")
        report.append("║" + "  Экспертная система медицинской диагностики".center(68) + "║")
        report.append("║" + "  Лабораторная работа №3".center(68) + "║")
        report.append("║" + " " * 68 + "║")
        report.append("╚" + "═" * 68 + "╝")
        report.append("\n\n")
        
        report.append(self.visualize_statistics())
        report.append("\n\n")
        report.append(self.visualize_hierarchy())
        report.append("\n\n")
        report.append(self.visualize_disease_symptoms())
        report.append("\n\n")
        report.append(self.visualize_disease_treatment())
        report.append("\n\n")
        report.append(self.visualize_nodes_list())
        report.append("\n\n")
        report.append(self.visualize_graph_structure())
        
        # Сохранить в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("".join(report))
        
        print(f"Отчет сохранен в {output_file}")
        
        return "".join(report)


def main():
    """Создать текстовую визуализацию"""
    print("=" * 70)
    print("СОЗДАНИЕ ТЕКСТОВОЙ ВИЗУАЛИЗАЦИИ СЕМАНТИЧЕСКОЙ СЕТИ")
    print("=" * 70)
    print()
    
    # Создать базу знаний
    kb = create_medical_knowledge_base()
    
    # Создать визуализатор
    visualizer = TextVisualizer(kb)
    
    # Вывести на экран
    print(visualizer.visualize_statistics())
    print(visualizer.visualize_hierarchy())
    print(visualizer.visualize_disease_symptoms())
    
    # Создать полный отчет
    print("\nСоздание полного отчета...")
    visualizer.create_full_report()
    print("\nГотово!")


if __name__ == "__main__":
    main()

