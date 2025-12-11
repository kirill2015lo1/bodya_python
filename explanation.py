"""
Модуль компонента объяснения
Предоставляет объяснения логического вывода в понятной форме
"""

from typing import List, Dict, Any
from inference_engine import InferenceEngine


class ExplanationComponent:
    """
    Компонент объяснения для экспертной системы
    Генерирует понятные объяснения на основе трассировки вывода
    """
    
    def __init__(self, inference_engine: InferenceEngine):
        """
        Инициализация компонента объяснения
        
        Args:
            inference_engine: Механизм логического вывода
        """
        self.engine = inference_engine
        
    def explain_last_inference(self) -> str:
        """
        Объяснить последний логический вывод
        
        Returns:
            Текстовое объяснение
        """
        trace = self.engine.get_trace()
        
        if not trace:
            return "Нет данных о последнем выводе."
        
        explanation = []
        explanation.append("=" * 60)
        explanation.append("ОБЪЯСНЕНИЕ ЛОГИЧЕСКОГО ВЫВОДА")
        explanation.append("=" * 60)
        
        for i, step in enumerate(trace, 1):
            explanation.append(f"\nШаг {i}: {step['step']}")
            
            details = step['details']
            if isinstance(details, str):
                explanation.append(f"  {details}")
            elif isinstance(details, list):
                for item in details:
                    explanation.append(f"  - {item}")
            elif isinstance(details, dict):
                for key, value in details.items():
                    explanation.append(f"  {key}: {value}")
            else:
                explanation.append(f"  {details}")
        
        explanation.append("\n" + "=" * 60)
        
        return "\n".join(explanation)
    
    def explain_diagnosis(self, symptoms: List[str], 
                         diagnosis_results: List[tuple]) -> str:
        """
        Объяснить результаты диагностики
        
        Args:
            symptoms: Список симптомов
            diagnosis_results: Результаты диагностики
            
        Returns:
            Подробное объяснение
        """
        explanation = []
        explanation.append("=" * 60)
        explanation.append("ОБЪЯСНЕНИЕ ДИАГНОСТИКИ")
        explanation.append("=" * 60)
        
        explanation.append(f"\nНаблюдаемые симптомы ({len(symptoms)}):")
        for symptom in symptoms:
            explanation.append(f"  • {symptom}")
        
        if not diagnosis_results:
            explanation.append("\nРезультат: Не найдено заболеваний с указанными симптомами.")
            explanation.append("\nВозможные причины:")
            explanation.append("  - Симптомы не соответствуют ни одному заболеванию в базе знаний")
            explanation.append("  - Необходимо дополнительное обследование")
        else:
            explanation.append(f"\nНайдено возможных заболеваний: {len(diagnosis_results)}")
            explanation.append("\nАнализ по каждому заболеванию:\n")
            
            for i, (disease, confidence, matched_symptoms) in enumerate(diagnosis_results, 1):
                explanation.append(f"{i}. {disease}")
                explanation.append(f"   Уверенность: {confidence:.1%}")
                explanation.append(f"   Совпавшие симптомы ({len(matched_symptoms)}):")
                for symptom in matched_symptoms:
                    explanation.append(f"     ✓ {symptom}")
                
                # Получить все симптомы заболевания
                all_symptoms = self.engine.get_symptoms(disease)
                missing_symptoms = [s for s in all_symptoms if s not in matched_symptoms]
                
                if missing_symptoms:
                    explanation.append(f"   Отсутствующие симптомы ({len(missing_symptoms)}):")
                    for symptom in missing_symptoms:
                        explanation.append(f"     ✗ {symptom}")
                
                # Получить методы лечения
                treatments = self.engine.get_treatment(disease)
                if treatments:
                    explanation.append(f"   Рекомендуемое лечение:")
                    for treatment in treatments:
                        explanation.append(f"     → {treatment}")
                
                explanation.append("")
            
            # Рекомендации
            explanation.append("РЕКОМЕНДАЦИИ:")
            best_match = diagnosis_results[0]
            if best_match[1] >= 0.8:
                explanation.append(f"  Высокая вероятность: {best_match[0]}")
                explanation.append(f"  Рекомендуется начать соответствующее лечение.")
            elif best_match[1] >= 0.5:
                explanation.append(f"  Средняя вероятность: {best_match[0]}")
                explanation.append(f"  Рекомендуется дополнительное обследование.")
            else:
                explanation.append(f"  Низкая уверенность в диагнозе.")
                explanation.append(f"  Необходима консультация специалиста.")
        
        explanation.append("\n" + "=" * 60)
        
        return "\n".join(explanation)
    
    def explain_subtype_check(self, concept1: str, concept2: str, 
                             result: bool) -> str:
        """
        Объяснить проверку подтипа
        
        Args:
            concept1: Проверяемый концепт
            concept2: Родительский концепт
            result: Результат проверки
            
        Returns:
            Объяснение
        """
        explanation = []
        explanation.append("=" * 60)
        explanation.append("ОБЪЯСНЕНИЕ ПРОВЕРКИ ПОДТИПА")
        explanation.append("=" * 60)
        
        explanation.append(f"\nВопрос: Является ли '{concept1}' подтипом '{concept2}'?")
        explanation.append(f"Ответ: {'ДА' if result else 'НЕТ'}")
        
        trace = self.engine.get_trace()
        
        if result:
            explanation.append("\nОбоснование:")
            explanation.append(f"  Найдена цепочка отношений 'является_подтипом',")
            explanation.append(f"  связывающая '{concept1}' с '{concept2}':")
            
            # Извлечь цепочку связей из трассировки
            for step in trace:
                if step['step'] == "Найдена связь":
                    explanation.append(f"    • {step['details']}")
        else:
            explanation.append("\nОбоснование:")
            explanation.append(f"  Не найдено цепочки отношений 'является_подтипом',")
            explanation.append(f"  связывающей '{concept1}' с '{concept2}'.")
        
        explanation.append("\n" + "=" * 60)
        
        return "\n".join(explanation)
    
    def explain_concept_info(self, concept: str, info: Dict[str, Any]) -> str:
        """
        Объяснить информацию о концепте
        
        Args:
            concept: Название концепта
            info: Информация о концепте
            
        Returns:
            Объяснение
        """
        explanation = []
        explanation.append("=" * 60)
        explanation.append(f"ИНФОРМАЦИЯ О КОНЦЕПТЕ: {concept}")
        explanation.append("=" * 60)
        
        if not info:
            explanation.append("\nКонцепт не найден в базе знаний.")
            return "\n".join(explanation)
        
        # Атрибуты
        if "атрибуты" in info and info["атрибуты"]:
            explanation.append("\nАтрибуты:")
            for key, value in info["атрибуты"].items():
                explanation.append(f"  {key}: {value}")
        
        # Исходящие связи
        if "исходящие_связи" in info and info["исходящие_связи"]:
            explanation.append("\nИсходящие связи:")
            for rel_type, targets in info["исходящие_связи"].items():
                explanation.append(f"  {rel_type}:")
                for target in targets:
                    explanation.append(f"    → {target}")
        
        # Входящие связи
        if "входящие_связи" in info and info["входящие_связи"]:
            explanation.append("\nВходящие связи:")
            for rel_type, sources in info["входящие_связи"].items():
                explanation.append(f"  {rel_type}:")
                for source in sources:
                    explanation.append(f"    ← {source}")
        
        explanation.append("\n" + "=" * 60)
        
        return "\n".join(explanation)
    
    def generate_summary(self, kb) -> str:
        """
        Сгенерировать общую сводку по базе знаний
        
        Args:
            kb: База знаний
            
        Returns:
            Сводка
        """
        summary = []
        summary.append("=" * 60)
        summary.append("СВОДКА ПО БАЗЕ ЗНАНИЙ")
        summary.append("=" * 60)
        
        # Статистика по узлам
        node_types = {}
        for node_name, node_attrs in kb.nodes.items():
            node_type = node_attrs.get("type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        summary.append(f"\nВсего узлов: {len(kb.nodes)}")
        summary.append("Распределение по типам:")
        for node_type, count in sorted(node_types.items()):
            summary.append(f"  {node_type}: {count}")
        
        # Статистика по связям
        relation_types = {}
        for rel in kb.relations:
            rel_type = rel[1]
            relation_types[rel_type] = relation_types.get(rel_type, 0) + 1
        
        summary.append(f"\nВсего связей: {len(kb.relations)}")
        summary.append("Распределение по типам:")
        for rel_type, count in sorted(relation_types.items()):
            summary.append(f"  {rel_type}: {count}")
        
        # Заболевания
        diseases = kb.get_all_nodes_by_type("disease")
        if diseases:
            summary.append(f"\nЗаболевания в базе ({len(diseases)}):")
            for disease in sorted(diseases):
                summary.append(f"  • {disease}")
        
        # Симптомы
        symptoms = kb.get_all_nodes_by_type("symptom")
        if symptoms:
            summary.append(f"\nСимптомы в базе ({len(symptoms)}):")
            for symptom in sorted(symptoms):
                summary.append(f"  • {symptom}")
        
        summary.append("\n" + "=" * 60)
        
        return "\n".join(summary)
    
    def explain_why_question(self, question: str, answer: Any) -> str:
        """
        Объяснить ответ на вопрос "Почему?"
        
        Args:
            question: Вопрос
            answer: Ответ
            
        Returns:
            Объяснение
        """
        explanation = []
        explanation.append("=" * 60)
        explanation.append("ОБЪЯСНЕНИЕ")
        explanation.append("=" * 60)
        
        explanation.append(f"\nВопрос: {question}")
        explanation.append(f"Ответ: {answer}")
        
        explanation.append("\nОбоснование:")
        trace = self.engine.get_trace()
        
        if trace:
            explanation.append("  Логический вывод основан на следующих шагах:")
            for i, step in enumerate(trace, 1):
                if step['step'] not in ["Начало запроса", "Результат"]:
                    explanation.append(f"  {i}. {step['step']}: {step['details']}")
        else:
            explanation.append("  Ответ получен напрямую из базы знаний.")
        
        explanation.append("\n" + "=" * 60)
        
        return "\n".join(explanation)


if __name__ == "__main__":
    # Тестирование модуля
    from semantic_network import create_medical_knowledge_base
    from inference_engine import InferenceEngine
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    explainer = ExplanationComponent(engine)
    
    print("=== Тест компонента объяснения ===\n")
    
    # Тест 1: Объяснение диагностики
    symptoms = ["Высокая_температура", "Кашель", "Головная_боль"]
    diagnosis = engine.diagnose_by_symptoms(symptoms)
    print(explainer.explain_diagnosis(symptoms, diagnosis))
    print("\n")
    
    # Тест 2: Объяснение проверки подтипа
    result = engine.is_subtype_of("Грипп", "Инфекционное_заболевание")
    print(explainer.explain_subtype_check("Грипп", "Инфекционное_заболевание", result))
    print("\n")
    
    # Тест 3: Сводка по базе знаний
    print(explainer.generate_summary(kb))

