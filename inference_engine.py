"""
Модуль механизма логического вывода (МЛВ)
Реализует различные типы запросов к базе знаний
"""

from typing import List, Dict, Set, Tuple, Any
from semantic_network import SemanticNetwork


class InferenceEngine:
    """
    Механизм логического вывода для семантической сети
    Поддерживает различные типы запросов
    """
    
    def __init__(self, knowledge_base: SemanticNetwork):
        """
        Инициализация механизма вывода
        
        Args:
            knowledge_base: База знаний (семантическая сеть)
        """
        self.kb = knowledge_base
        self.inference_trace = []  # Трассировка вывода для объяснений
        
    def clear_trace(self):
        """Очистить трассировку вывода"""
        self.inference_trace = []
        
    def add_trace(self, step: str, details: Any):
        """
        Добавить шаг в трассировку вывода
        
        Args:
            step: Описание шага
            details: Детали шага
        """
        self.inference_trace.append({
            "step": step,
            "details": details
        })
    
    def get_trace(self) -> List[Dict]:
        """Получить трассировку вывода"""
        return self.inference_trace
    
    # ========== Тип запроса 1: "Является ли X подтипом Y?" ==========
    
    def is_subtype_of(self, concept1: str, concept2: str) -> bool:
        """
        Проверить, является ли concept1 подтипом concept2
        
        Args:
            concept1: Проверяемый концепт
            concept2: Родительский концепт
            
        Returns:
            True, если concept1 является подтипом concept2
        """
        self.clear_trace()
        self.add_trace("Начало проверки", 
                      f"Является ли '{concept1}' подтипом '{concept2}'?")
        
        if concept1 not in self.kb.nodes:
            self.add_trace("Ошибка", f"Узел '{concept1}' не найден")
            return False
        
        if concept2 not in self.kb.nodes:
            self.add_trace("Ошибка", f"Узел '{concept2}' не найден")
            return False
        
        # Поиск в ширину по отношениям "является_подтипом"
        visited = set()
        queue = [concept1]
        
        while queue:
            current = queue.pop(0)
            
            if current in visited:
                continue
                
            visited.add(current)
            self.add_trace("Проверка узла", current)
            
            if current == concept2:
                self.add_trace("Результат", f"'{concept1}' ЯВЛЯЕТСЯ подтипом '{concept2}'")
                return True
            
            # Ищем родительские узлы
            for rel in self.kb.get_relations_from(current):
                if rel[1] == "является_подтипом":
                    queue.append(rel[2])
                    self.add_trace("Найдена связь", f"{rel[0]} -> {rel[1]} -> {rel[2]}")
        
        self.add_trace("Результат", f"'{concept1}' НЕ ЯВЛЯЕТСЯ подтипом '{concept2}'")
        return False
    
    # ========== Тип запроса 2: "Какие симптомы имеет заболевание X?" ==========
    
    def get_symptoms(self, disease: str) -> List[str]:
        """
        Получить все симптомы заболевания
        
        Args:
            disease: Название заболевания
            
        Returns:
            Список симптомов
        """
        self.clear_trace()
        self.add_trace("Начало запроса", f"Поиск симптомов для '{disease}'")
        
        if disease not in self.kb.nodes:
            self.add_trace("Ошибка", f"Заболевание '{disease}' не найдено")
            return []
        
        symptoms = []
        
        # Прямые симптомы
        for rel in self.kb.get_relations_from(disease):
            if rel[1] == "имеет_симптом":
                symptoms.append(rel[2])
                self.add_trace("Найден симптом", rel[2])
        
        self.add_trace("Результат", f"Найдено симптомов: {len(symptoms)}")
        return symptoms
    
    # ========== Тип запроса 3: "Какие заболевания имеют симптомы X?" ==========
    
    def diagnose_by_symptoms(self, symptoms: List[str]) -> List[Tuple[str, float, List[str]]]:
        """
        Диагностировать заболевания по симптомам
        
        Args:
            symptoms: Список наблюдаемых симптомов
            
        Returns:
            Список кортежей (заболевание, уверенность, совпавшие_симптомы)
            отсортированный по убыванию уверенности
        """
        self.clear_trace()
        self.add_trace("Начало диагностики", f"Симптомы: {symptoms}")
        
        # Найти все заболевания
        diseases = self.kb.get_all_nodes_by_type("disease")
        self.add_trace("Найдены заболевания", diseases)
        
        results = []
        
        for disease in diseases:
            # Получить симптомы заболевания
            disease_symptoms = self.get_symptoms(disease)
            
            # Найти совпадающие симптомы
            matching_symptoms = [s for s in symptoms if s in disease_symptoms]
            
            if matching_symptoms:
                # Вычислить уверенность (процент совпадения)
                confidence = len(matching_symptoms) / len(disease_symptoms) if disease_symptoms else 0
                results.append((disease, confidence, matching_symptoms))
                
                self.add_trace("Совпадение", {
                    "заболевание": disease,
                    "уверенность": f"{confidence:.2%}",
                    "совпавшие_симптомы": matching_symptoms
                })
        
        # Сортировка по убыванию уверенности
        results.sort(key=lambda x: x[1], reverse=True)
        
        self.add_trace("Результат диагностики", 
                      f"Найдено возможных заболеваний: {len(results)}")
        
        return results
    
    # ========== Тип запроса 4: "Как лечить заболевание X?" ==========
    
    def get_treatment(self, disease: str) -> List[str]:
        """
        Получить методы лечения заболевания
        
        Args:
            disease: Название заболевания
            
        Returns:
            Список методов лечения
        """
        self.clear_trace()
        self.add_trace("Начало запроса", f"Поиск лечения для '{disease}'")
        
        if disease not in self.kb.nodes:
            self.add_trace("Ошибка", f"Заболевание '{disease}' не найдено")
            return []
        
        treatments = []
        
        for rel in self.kb.get_relations_from(disease):
            if rel[1] == "лечится":
                treatments.append(rel[2])
                self.add_trace("Найден метод лечения", rel[2])
        
        self.add_trace("Результат", f"Найдено методов лечения: {len(treatments)}")
        return treatments
    
    # ========== Тип запроса 5: "Какие заболевания относятся к категории X?" ==========
    
    def get_diseases_by_category(self, category: str) -> List[str]:
        """
        Получить все заболевания определенной категории
        
        Args:
            category: Категория заболеваний
            
        Returns:
            Список заболеваний
        """
        self.clear_trace()
        self.add_trace("Начало запроса", f"Поиск заболеваний категории '{category}'")
        
        if category not in self.kb.nodes:
            self.add_trace("Ошибка", f"Категория '{category}' не найдена")
            return []
        
        diseases = []
        
        # Найти все узлы, которые являются подтипами данной категории
        all_diseases = self.kb.get_all_nodes_by_type("disease")
        
        for disease in all_diseases:
            if self.is_subtype_of(disease, category):
                diseases.append(disease)
                self.add_trace("Найдено заболевание", disease)
        
        self.add_trace("Результат", f"Найдено заболеваний: {len(diseases)}")
        return diseases
    
    # ========== Дополнительные методы вывода ==========
    
    def get_all_related_info(self, concept: str) -> Dict[str, Any]:
        """
        Получить всю информацию, связанную с концептом
        
        Args:
            concept: Название концепта
            
        Returns:
            Словарь со всей информацией
        """
        self.clear_trace()
        self.add_trace("Начало запроса", f"Сбор информации о '{concept}'")
        
        if concept not in self.kb.nodes:
            self.add_trace("Ошибка", f"Концепт '{concept}' не найден")
            return {}
        
        info = {
            "узел": concept,
            "атрибуты": self.kb.get_node(concept),
            "исходящие_связи": {},
            "входящие_связи": {}
        }
        
        # Группировка исходящих связей по типу
        for rel in self.kb.get_relations_from(concept):
            rel_type = rel[1]
            if rel_type not in info["исходящие_связи"]:
                info["исходящие_связи"][rel_type] = []
            info["исходящие_связи"][rel_type].append(rel[2])
        
        # Группировка входящих связей по типу
        for rel in self.kb.get_relations_to(concept):
            rel_type = rel[1]
            if rel_type not in info["входящие_связи"]:
                info["входящие_связи"][rel_type] = []
            info["входящие_связи"][rel_type].append(rel[0])
        
        self.add_trace("Результат", "Информация собрана")
        return info
    
    def find_connection(self, concept1: str, concept2: str) -> List[List[Tuple[str, str, str]]]:
        """
        Найти связь между двумя концептами
        
        Args:
            concept1: Первый концепт
            concept2: Второй концепт
            
        Returns:
            Список путей между концептами
        """
        self.clear_trace()
        self.add_trace("Начало поиска", f"Поиск связи между '{concept1}' и '{concept2}'")
        
        paths = self.kb.find_path(concept1, concept2)
        
        self.add_trace("Результат", f"Найдено путей: {len(paths)}")
        
        return paths


if __name__ == "__main__":
    # Тестирование модуля
    from semantic_network import create_medical_knowledge_base
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    
    print("=== Тест механизма логического вывода ===\n")
    
    # Тест 1: Проверка подтипа
    print("1. Является ли Грипп подтипом Инфекционного_заболевания?")
    result = engine.is_subtype_of("Грипп", "Инфекционное_заболевание")
    print(f"   Результат: {result}\n")
    
    # Тест 2: Получение симптомов
    print("2. Какие симптомы у Гриппа?")
    symptoms = engine.get_symptoms("Грипп")
    print(f"   Симптомы: {symptoms}\n")
    
    # Тест 3: Диагностика по симптомам
    print("3. Диагностика по симптомам [Высокая_температура, Кашель, Слабость]")
    diagnosis = engine.diagnose_by_symptoms(["Высокая_температура", "Кашель", "Слабость"])
    for disease, confidence, matched in diagnosis:
        print(f"   {disease}: {confidence:.2%} (симптомы: {matched})")
    print()
    
    # Тест 4: Получение лечения
    print("4. Как лечить Грипп?")
    treatment = engine.get_treatment("Грипп")
    print(f"   Лечение: {treatment}\n")
    
    # Тест 5: Заболевания по категории
    print("5. Какие заболевания относятся к Респираторным?")
    diseases = engine.get_diseases_by_category("Респираторное_заболевание")
    print(f"   Заболевания: {diseases}\n")

