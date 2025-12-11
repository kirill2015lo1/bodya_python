"""
Демонстрационный скрипт для экспертной системы
Показывает основные возможности системы
"""

from semantic_network import create_medical_knowledge_base
from inference_engine import InferenceEngine
from explanation import ExplanationComponent


def print_separator(title=""):
    """Печать разделителя"""
    if title:
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    else:
        print("\n" + "-" * 60)


def demo_query_type_1():
    """Демонстрация запроса типа 1: Является ли X подтипом Y?"""
    print_separator("ЗАПРОС ТИПА 1: Является ли X подтипом Y?")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    explainer = ExplanationComponent(engine)
    
    # Пример 1
    print("\nПример 1: Является ли Грипп подтипом Инфекционного_заболевания?")
    result = engine.is_subtype_of("Грипп", "Инфекционное_заболевание")
    print(f"Результат: {'ДА' if result else 'НЕТ'}")
    
    # Пример 2
    print("\nПример 2: Является ли Гастрит подтипом Респираторного_заболевания?")
    result = engine.is_subtype_of("Гастрит", "Респираторное_заболевание")
    print(f"Результат: {'ДА' if result else 'НЕТ'}")
    
    # Пример 3
    print("\nПример 3: Является ли ОРВИ подтипом Заболевания?")
    result = engine.is_subtype_of("ОРВИ", "Заболевание")
    print(f"Результат: {'ДА' if result else 'НЕТ'}")
    print(explainer.explain_subtype_check("ОРВИ", "Заболевание", result))


def demo_query_type_2():
    """Демонстрация запроса типа 2: Какие симптомы имеет заболевание X?"""
    print_separator("ЗАПРОС ТИПА 2: Какие симптомы имеет заболевание X?")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    
    diseases = ["Грипп", "Пневмония", "Гастрит"]
    
    for disease in diseases:
        print(f"\nСимптомы заболевания '{disease}':")
        symptoms = engine.get_symptoms(disease)
        for symptom in symptoms:
            print(f"  • {symptom}")


def demo_query_type_3():
    """Демонстрация запроса типа 3: Диагностика по симптомам"""
    print_separator("ЗАПРОС ТИПА 3: Диагностика по симптомам")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    explainer = ExplanationComponent(engine)
    
    # Пример 1: Симптомы гриппа
    print("\nПример 1: Пациент с высокой температурой, кашлем и головной болью")
    symptoms = ["Высокая_температура", "Кашель", "Головная_боль"]
    diagnosis = engine.diagnose_by_symptoms(symptoms)
    
    print("\nРезультаты диагностики:")
    for disease, confidence, matched in diagnosis[:3]:  # Топ-3
        print(f"  {disease}: {confidence:.1%}")
    
    # Пример 2: Симптомы отравления
    print("\n\nПример 2: Пациент с тошнотой, рвотой и диареей")
    symptoms = ["Тошнота", "Рвота", "Диарея"]
    diagnosis = engine.diagnose_by_symptoms(symptoms)
    
    print(explainer.explain_diagnosis(symptoms, diagnosis))


def demo_query_type_4():
    """Демонстрация запроса типа 4: Как лечить заболевание X?"""
    print_separator("ЗАПРОС ТИПА 4: Как лечить заболевание X?")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    
    diseases = ["Грипп", "Пневмония", "Пищевое_отравление"]
    
    for disease in diseases:
        print(f"\nЛечение заболевания '{disease}':")
        treatments = engine.get_treatment(disease)
        if treatments:
            for treatment in treatments:
                print(f"  • {treatment}")
        else:
            print("  Методы лечения не указаны")


def demo_query_type_5():
    """Демонстрация запроса типа 5: Заболевания по категории"""
    print_separator("ЗАПРОС ТИПА 5: Заболевания по категории")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    
    categories = ["Респираторное_заболевание", "Желудочно-кишечное_заболевание"]
    
    for category in categories:
        print(f"\nЗаболевания категории '{category}':")
        diseases = engine.get_diseases_by_category(category)
        for disease in diseases:
            print(f"  • {disease}")


def demo_explanation_component():
    """Демонстрация компонента объяснения"""
    print_separator("КОМПОНЕНТ ОБЪЯСНЕНИЯ")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    explainer = ExplanationComponent(engine)
    
    print("\nСводка по базе знаний:")
    print(explainer.generate_summary(kb))
    
    print("\nПолучение информации о концепте 'Грипп':")
    info = engine.get_all_related_info("Грипп")
    print(explainer.explain_concept_info("Грипп", info))


def demo_complex_scenario():
    """Демонстрация сложного сценария использования"""
    print_separator("СЛОЖНЫЙ СЦЕНАРИЙ: Полная диагностика пациента")
    
    kb = create_medical_knowledge_base()
    engine = InferenceEngine(kb)
    explainer = ExplanationComponent(engine)
    
    print("\nСценарий: Пациент обратился с жалобами")
    print("Симптомы: Высокая температура, Кашель, Боль в груди, Одышка, Слабость")
    
    symptoms = ["Высокая_температура", "Кашель", "Боль_в_груди", "Одышка", "Слабость"]
    
    # Шаг 1: Диагностика
    print("\n--- ШАГ 1: Диагностика ---")
    diagnosis = engine.diagnose_by_symptoms(symptoms)
    
    if diagnosis:
        top_disease, confidence, matched = diagnosis[0]
        print(f"\nНаиболее вероятный диагноз: {top_disease} ({confidence:.1%})")
        
        # Шаг 2: Проверка типа заболевания
        print("\n--- ШАГ 2: Классификация заболевания ---")
        is_respiratory = engine.is_subtype_of(top_disease, "Респираторное_заболевание")
        is_infectious = engine.is_subtype_of(top_disease, "Инфекционное_заболевание")
        
        print(f"Респираторное заболевание: {'Да' if is_respiratory else 'Нет'}")
        print(f"Инфекционное заболевание: {'Да' if is_infectious else 'Нет'}")
        
        # Шаг 3: Получение полной информации
        print("\n--- ШАГ 3: Полная информация о заболевании ---")
        info = engine.get_all_related_info(top_disease)
        
        print(f"\nТип: {info['атрибуты'].get('type')}")
        print(f"Тяжесть: {info['атрибуты'].get('severity')}")
        print(f"Заразное: {info['атрибуты'].get('contagious')}")
        
        # Шаг 4: Рекомендации по лечению
        print("\n--- ШАГ 4: Рекомендации по лечению ---")
        treatments = engine.get_treatment(top_disease)
        print("\nРекомендуемое лечение:")
        for treatment in treatments:
            print(f"  • {treatment}")
        
        # Шаг 5: Объяснение
        print("\n--- ШАГ 5: Подробное объяснение ---")
        print(explainer.explain_diagnosis(symptoms, diagnosis))


def main():
    """Запуск всех демонстраций"""
    print("=" * 60)
    print("  ДЕМОНСТРАЦИЯ ЭКСПЕРТНОЙ СИСТЕМЫ")
    print("  Лабораторная работа №3")
    print("  Семантические сети")
    print("=" * 60)
    
    try:
        # Демонстрация всех типов запросов
        demo_query_type_1()
        input("\nНажмите Enter для продолжения...")
        
        demo_query_type_2()
        input("\nНажмите Enter для продолжения...")
        
        demo_query_type_3()
        input("\nНажмите Enter для продолжения...")
        
        demo_query_type_4()
        input("\nНажмите Enter для продолжения...")
        
        demo_query_type_5()
        input("\nНажмите Enter для продолжения...")
        
        demo_explanation_component()
        input("\nНажмите Enter для продолжения...")
        
        demo_complex_scenario()
        
        print("\n" + "=" * 60)
        print("  ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nДемонстрация прервана пользователем.")


if __name__ == "__main__":
    main()

