"""
Модуль базы знаний на основе семантических сетей
Представляет знания в виде графа с узлами (концептами) и связями (отношениями)
"""

from typing import Dict, List, Set, Tuple, Any
import json


class SemanticNetwork:
    """
    Класс для представления семантической сети
    """
    
    def __init__(self):
        """Инициализация пустой семантической сети"""
        # Словарь узлов: {имя_узла: {атрибуты}}
        self.nodes: Dict[str, Dict[str, Any]] = {}
        # Список связей: [(узел1, отношение, узел2)]
        self.relations: List[Tuple[str, str, str]] = []
        
    def add_node(self, node_name: str, node_type: str = "concept", **attributes):
        """
        Добавить узел в семантическую сеть
        
        Args:
            node_name: Имя узла
            node_type: Тип узла (concept, symptom, disease, etc.)
            **attributes: Дополнительные атрибуты узла
        """
        self.nodes[node_name] = {
            "type": node_type,
            **attributes
        }
        
    def add_relation(self, source: str, relation: str, target: str):
        """
        Добавить связь между узлами
        
        Args:
            source: Исходный узел
            relation: Тип отношения
            target: Целевой узел
        """
        if source not in self.nodes:
            raise ValueError(f"Узел '{source}' не существует")
        if target not in self.nodes:
            raise ValueError(f"Узел '{target}' не существует")
            
        self.relations.append((source, relation, target))
        
    def get_node(self, node_name: str) -> Dict[str, Any]:
        """Получить узел по имени"""
        return self.nodes.get(node_name, {})
    
    def get_relations_from(self, node_name: str) -> List[Tuple[str, str, str]]:
        """Получить все связи, исходящие из узла"""
        return [r for r in self.relations if r[0] == node_name]
    
    def get_relations_to(self, node_name: str) -> List[Tuple[str, str, str]]:
        """Получить все связи, входящие в узел"""
        return [r for r in self.relations if r[2] == node_name]
    
    def get_relations_by_type(self, relation_type: str) -> List[Tuple[str, str, str]]:
        """Получить все связи определенного типа"""
        return [r for r in self.relations if r[1] == relation_type]
    
    def find_path(self, start: str, end: str, max_depth: int = 5) -> List[List[Tuple[str, str, str]]]:
        """
        Найти все пути между двумя узлами
        
        Args:
            start: Начальный узел
            end: Конечный узел
            max_depth: Максимальная глубина поиска
            
        Returns:
            Список путей, где каждый путь - список связей
        """
        paths = []
        visited = set()
        
        def dfs(current: str, path: List[Tuple[str, str, str]], depth: int):
            if depth > max_depth:
                return
            
            if current == end and path:
                paths.append(path.copy())
                return
            
            if current in visited:
                return
                
            visited.add(current)
            
            for relation in self.get_relations_from(current):
                _, rel_type, target = relation
                path.append(relation)
                dfs(target, path, depth + 1)
                path.pop()
            
            visited.remove(current)
        
        dfs(start, [], 0)
        return paths
    
    def get_all_nodes_by_type(self, node_type: str) -> List[str]:
        """Получить все узлы определенного типа"""
        return [name for name, attrs in self.nodes.items() 
                if attrs.get("type") == node_type]
    
    def export_to_dict(self) -> Dict:
        """Экспортировать сеть в словарь"""
        return {
            "nodes": self.nodes,
            "relations": self.relations
        }
    
    def import_from_dict(self, data: Dict):
        """Импортировать сеть из словаря"""
        self.nodes = data.get("nodes", {})
        self.relations = [tuple(r) for r in data.get("relations", [])]
    
    def save_to_file(self, filename: str):
        """Сохранить сеть в JSON файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.export_to_dict(), f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str):
        """Загрузить сеть из JSON файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.import_from_dict(data)


def create_medical_knowledge_base() -> SemanticNetwork:
    """
    Создать базу знаний для медицинской диагностики
    Предметная область: диагностика заболеваний
    """
    kb = SemanticNetwork()
    
    # Добавляем категории заболеваний
    kb.add_node("Заболевание", node_type="category", 
                description="Корневая категория заболеваний")
    kb.add_node("Инфекционное_заболевание", node_type="category",
                description="Заболевания, вызванные инфекцией")
    kb.add_node("Респираторное_заболевание", node_type="category",
                description="Заболевания дыхательной системы")
    kb.add_node("Желудочно-кишечное_заболевание", node_type="category",
                description="Заболевания ЖКТ")
    
    # Связи между категориями (иерархия)
    kb.add_relation("Инфекционное_заболевание", "является_подтипом", "Заболевание")
    kb.add_relation("Респираторное_заболевание", "является_подтипом", "Заболевание")
    kb.add_relation("Желудочно-кишечное_заболевание", "является_подтипом", "Заболевание")
    
    # Конкретные заболевания
    kb.add_node("Грипп", node_type="disease", 
                severity="средняя", contagious=True,
                description="Острое инфекционное заболевание дыхательных путей")
    kb.add_node("ОРВИ", node_type="disease",
                severity="легкая", contagious=True,
                description="Острая респираторная вирусная инфекция")
    kb.add_node("Пневмония", node_type="disease",
                severity="высокая", contagious=False,
                description="Воспаление легких")
    kb.add_node("Гастрит", node_type="disease",
                severity="средняя", contagious=False,
                description="Воспаление слизистой оболочки желудка")
    kb.add_node("Пищевое_отравление", node_type="disease",
                severity="средняя", contagious=False,
                description="Острое расстройство пищеварения")
    
    # Связи заболеваний с категориями
    kb.add_relation("Грипп", "является_подтипом", "Инфекционное_заболевание")
    kb.add_relation("Грипп", "является_подтипом", "Респираторное_заболевание")
    kb.add_relation("ОРВИ", "является_подтипом", "Инфекционное_заболевание")
    kb.add_relation("ОРВИ", "является_подтипом", "Респираторное_заболевание")
    kb.add_relation("Пневмония", "является_подтипом", "Респираторное_заболевание")
    kb.add_relation("Гастрит", "является_подтипом", "Желудочно-кишечное_заболевание")
    kb.add_relation("Пищевое_отравление", "является_подтипом", "Желудочно-кишечное_заболевание")
    
    # Симптомы
    kb.add_node("Высокая_температура", node_type="symptom",
                description="Температура тела выше 38°C")
    kb.add_node("Кашель", node_type="symptom",
                description="Рефлекторное действие для очистки дыхательных путей")
    kb.add_node("Насморк", node_type="symptom",
                description="Выделения из носа")
    kb.add_node("Боль_в_горле", node_type="symptom",
                description="Дискомфорт в области горла")
    kb.add_node("Головная_боль", node_type="symptom",
                description="Боль в области головы")
    kb.add_node("Слабость", node_type="symptom",
                description="Общее недомогание и усталость")
    kb.add_node("Боль_в_груди", node_type="symptom",
                description="Боль в области грудной клетки")
    kb.add_node("Одышка", node_type="symptom",
                description="Затрудненное дыхание")
    kb.add_node("Тошнота", node_type="symptom",
                description="Позывы к рвоте")
    kb.add_node("Рвота", node_type="symptom",
                description="Извержение содержимого желудка")
    kb.add_node("Боль_в_животе", node_type="symptom",
                description="Боль в области живота")
    kb.add_node("Диарея", node_type="symptom",
                description="Жидкий стул")
    
    # Связи заболеваний с симптомами
    kb.add_relation("Грипп", "имеет_симптом", "Высокая_температура")
    kb.add_relation("Грипп", "имеет_симптом", "Кашель")
    kb.add_relation("Грипп", "имеет_симптом", "Головная_боль")
    kb.add_relation("Грипп", "имеет_симптом", "Слабость")
    kb.add_relation("Грипп", "имеет_симптом", "Боль_в_горле")
    
    kb.add_relation("ОРВИ", "имеет_симптом", "Насморк")
    kb.add_relation("ОРВИ", "имеет_симптом", "Кашель")
    kb.add_relation("ОРВИ", "имеет_симптом", "Боль_в_горле")
    kb.add_relation("ОРВИ", "имеет_симптом", "Слабость")
    
    kb.add_relation("Пневмония", "имеет_симптом", "Высокая_температура")
    kb.add_relation("Пневмония", "имеет_симптом", "Кашель")
    kb.add_relation("Пневмония", "имеет_симптом", "Боль_в_груди")
    kb.add_relation("Пневмония", "имеет_симптом", "Одышка")
    kb.add_relation("Пневмония", "имеет_симптом", "Слабость")
    
    kb.add_relation("Гастрит", "имеет_симптом", "Боль_в_животе")
    kb.add_relation("Гастрит", "имеет_симптом", "Тошнота")
    
    kb.add_relation("Пищевое_отравление", "имеет_симптом", "Тошнота")
    kb.add_relation("Пищевое_отравление", "имеет_симптом", "Рвота")
    kb.add_relation("Пищевое_отравление", "имеет_симптом", "Диарея")
    kb.add_relation("Пищевое_отравление", "имеет_симптом", "Боль_в_животе")
    
    # Методы лечения
    kb.add_node("Противовирусные", node_type="treatment",
                description="Препараты против вирусов")
    kb.add_node("Антибиотики", node_type="treatment",
                description="Препараты против бактерий")
    kb.add_node("Жаропонижающие", node_type="treatment",
                description="Препараты для снижения температуры")
    kb.add_node("Сорбенты", node_type="treatment",
                description="Препараты для выведения токсинов")
    kb.add_node("Постельный_режим", node_type="treatment",
                description="Покой и отдых")
    
    # Связи заболеваний с лечением
    kb.add_relation("Грипп", "лечится", "Противовирусные")
    kb.add_relation("Грипп", "лечится", "Жаропонижающие")
    kb.add_relation("Грипп", "лечится", "Постельный_режим")
    
    kb.add_relation("ОРВИ", "лечится", "Постельный_режим")
    kb.add_relation("ОРВИ", "лечится", "Жаропонижающие")
    
    kb.add_relation("Пневмония", "лечится", "Антибиотики")
    kb.add_relation("Пневмония", "лечится", "Постельный_режим")
    
    kb.add_relation("Пищевое_отравление", "лечится", "Сорбенты")
    
    return kb


if __name__ == "__main__":
    # Тестирование модуля
    kb = create_medical_knowledge_base()
    
    print("=== Тест базы знаний ===")
    print(f"Всего узлов: {len(kb.nodes)}")
    print(f"Всего связей: {len(kb.relations)}")
    
    print("\nЗаболевания:")
    for disease in kb.get_all_nodes_by_type("disease"):
        print(f"  - {disease}")
    
    print("\nСимптомы гриппа:")
    for rel in kb.get_relations_from("Грипп"):
        if rel[1] == "имеет_симптом":
            print(f"  - {rel[2]}")
    
    # Сохранение в файл
    kb.save_to_file("knowledge_base.json")
    print("\nБаза знаний сохранена в knowledge_base.json")

