"""
Главный модуль экспертной системы
Интерактивный интерфейс для работы с ЭС
"""

import sys
from semantic_network import SemanticNetwork, create_medical_knowledge_base
from inference_engine import InferenceEngine
from explanation import ExplanationComponent


class ExpertSystem:
    """
    Оболочка экспертной системы
    Объединяет все компоненты: БЗ, МЛВ, компонент объяснения
    """
    
    def __init__(self):
        """Инициализация экспертной системы"""
        print("Инициализация экспертной системы...")
        
        # Создание базы знаний
        self.kb = create_medical_knowledge_base()
        
        # Создание механизма логического вывода
        self.engine = InferenceEngine(self.kb)
        
        # Создание компонента объяснения
        self.explainer = ExplanationComponent(self.engine)
        
        print("Экспертная система готова к работе!\n")
    
    def show_menu(self):
        """Показать главное меню"""
        print("\n" + "=" * 60)
        print("ЭКСПЕРТНАЯ СИСТЕМА - МЕДИЦИНСКАЯ ДИАГНОСТИКА")
        print("=" * 60)
        print("\nДоступные операции:")
        print("  1. Диагностика по симптомам")
        print("  2. Проверить, является ли X подтипом Y")
        print("  3. Получить симптомы заболевания")
        print("  4. Получить методы лечения")
        print("  5. Получить заболевания по категории")
        print("  6. Получить информацию о концепте")
        print("  7. Показать сводку по базе знаний")
        print("  8. Список всех заболеваний")
        print("  9. Список всех симптомов")
        print("  0. Выход")
        print("=" * 60)
    
    def diagnose_interactive(self):
        """Интерактивная диагностика"""
        print("\n--- ДИАГНОСТИКА ПО СИМПТОМАМ ---")
        print("\nДоступные симптомы:")
        
        symptoms = self.kb.get_all_nodes_by_type("symptom")
        for i, symptom in enumerate(symptoms, 1):
            print(f"  {i}. {symptom}")
        
        print("\nВведите номера симптомов через запятую (например: 1,3,5)")
        print("или введите 'все' для выбора всех симптомов:")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice.lower() == 'все':
            selected_symptoms = symptoms
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected_symptoms = [symptoms[i] for i in indices if 0 <= i < len(symptoms)]
            except (ValueError, IndexError):
                print("Ошибка: неверный ввод!")
                return
        
        if not selected_symptoms:
            print("Не выбрано ни одного симптома!")
            return
        
        print(f"\nВыбранные симптомы: {', '.join(selected_symptoms)}")
        print("\nВыполняется диагностика...\n")
        
        # Выполнить диагностику
        results = self.engine.diagnose_by_symptoms(selected_symptoms)
        
        # Показать объяснение
        print(self.explainer.explain_diagnosis(selected_symptoms, results))
    
    def check_subtype_interactive(self):
        """Интерактивная проверка подтипа"""
        print("\n--- ПРОВЕРКА ПОДТИПА ---")
        
        concept1 = input("Введите первый концепт: ").strip()
        concept2 = input("Введите второй концепт: ").strip()
        
        if not concept1 or not concept2:
            print("Ошибка: оба концепта должны быть указаны!")
            return
        
        print(f"\nПроверка: является ли '{concept1}' подтипом '{concept2}'...\n")
        
        result = self.engine.is_subtype_of(concept1, concept2)
        print(self.explainer.explain_subtype_check(concept1, concept2, result))
    
    def get_symptoms_interactive(self):
        """Интерактивное получение симптомов"""
        print("\n--- СИМПТОМЫ ЗАБОЛЕВАНИЯ ---")
        
        diseases = self.kb.get_all_nodes_by_type("disease")
        print("\nДоступные заболевания:")
        for i, disease in enumerate(diseases, 1):
            print(f"  {i}. {disease}")
        
        choice = input("\nВведите номер заболевания: ").strip()
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(diseases):
                disease = diseases[index]
            else:
                print("Ошибка: неверный номер!")
                return
        except ValueError:
            print("Ошибка: введите число!")
            return
        
        print(f"\nПолучение симптомов для '{disease}'...\n")
        
        symptoms = self.engine.get_symptoms(disease)
        
        print(f"Симптомы заболевания '{disease}':")
        if symptoms:
            for symptom in symptoms:
                print(f"  • {symptom}")
        else:
            print("  Симптомы не найдены")
        
        print("\n" + self.explainer.explain_last_inference())
    
    def get_treatment_interactive(self):
        """Интерактивное получение лечения"""
        print("\n--- МЕТОДЫ ЛЕЧЕНИЯ ---")
        
        diseases = self.kb.get_all_nodes_by_type("disease")
        print("\nДоступные заболевания:")
        for i, disease in enumerate(diseases, 1):
            print(f"  {i}. {disease}")
        
        choice = input("\nВведите номер заболевания: ").strip()
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(diseases):
                disease = diseases[index]
            else:
                print("Ошибка: неверный номер!")
                return
        except ValueError:
            print("Ошибка: введите число!")
            return
        
        print(f"\nПолучение методов лечения для '{disease}'...\n")
        
        treatments = self.engine.get_treatment(disease)
        
        print(f"Методы лечения заболевания '{disease}':")
        if treatments:
            for treatment in treatments:
                print(f"  • {treatment}")
        else:
            print("  Методы лечения не найдены")
        
        print("\n" + self.explainer.explain_last_inference())
    
    def get_diseases_by_category_interactive(self):
        """Интерактивное получение заболеваний по категории"""
        print("\n--- ЗАБОЛЕВАНИЯ ПО КАТЕГОРИИ ---")
        
        categories = self.kb.get_all_nodes_by_type("category")
        print("\nДоступные категории:")
        for i, category in enumerate(categories, 1):
            print(f"  {i}. {category}")
        
        choice = input("\nВведите номер категории: ").strip()
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(categories):
                category = categories[index]
            else:
                print("Ошибка: неверный номер!")
                return
        except ValueError:
            print("Ошибка: введите число!")
            return
        
        print(f"\nПолучение заболеваний категории '{category}'...\n")
        
        diseases = self.engine.get_diseases_by_category(category)
        
        print(f"Заболевания категории '{category}':")
        if diseases:
            for disease in diseases:
                print(f"  • {disease}")
        else:
            print("  Заболевания не найдены")
    
    def get_concept_info_interactive(self):
        """Интерактивное получение информации о концепте"""
        print("\n--- ИНФОРМАЦИЯ О КОНЦЕПТЕ ---")
        
        concept = input("Введите название концепта: ").strip()
        
        if not concept:
            print("Ошибка: название концепта не может быть пустым!")
            return
        
        print(f"\nПолучение информации о '{concept}'...\n")
        
        info = self.engine.get_all_related_info(concept)
        print(self.explainer.explain_concept_info(concept, info))
    
    def show_summary(self):
        """Показать сводку по базе знаний"""
        print(self.explainer.generate_summary(self.kb))
    
    def list_diseases(self):
        """Показать список всех заболеваний"""
        print("\n--- СПИСОК ЗАБОЛЕВАНИЙ ---")
        diseases = self.kb.get_all_nodes_by_type("disease")
        
        for disease in sorted(diseases):
            node_info = self.kb.get_node(disease)
            print(f"\n{disease}")
            if "description" in node_info:
                print(f"  Описание: {node_info['description']}")
            if "severity" in node_info:
                print(f"  Тяжесть: {node_info['severity']}")
    
    def list_symptoms(self):
        """Показать список всех симптомов"""
        print("\n--- СПИСОК СИМПТОМОВ ---")
        symptoms = self.kb.get_all_nodes_by_type("symptom")
        
        for symptom in sorted(symptoms):
            node_info = self.kb.get_node(symptom)
            print(f"\n{symptom}")
            if "description" in node_info:
                print(f"  Описание: {node_info['description']}")
    
    def run(self):
        """Запустить экспертную систему"""
        while True:
            self.show_menu()
            choice = input("\nВыберите операцию (0-9): ").strip()
            
            if choice == '0':
                print("\nЗавершение работы экспертной системы...")
                print("До свидания!")
                break
            elif choice == '1':
                self.diagnose_interactive()
            elif choice == '2':
                self.check_subtype_interactive()
            elif choice == '3':
                self.get_symptoms_interactive()
            elif choice == '4':
                self.get_treatment_interactive()
            elif choice == '5':
                self.get_diseases_by_category_interactive()
            elif choice == '6':
                self.get_concept_info_interactive()
            elif choice == '7':
                self.show_summary()
            elif choice == '8':
                self.list_diseases()
            elif choice == '9':
                self.list_symptoms()
            else:
                print("\nОшибка: неверный выбор! Попробуйте снова.")
            
            input("\nНажмите Enter для продолжения...")


def main():
    """Точка входа в программу"""
    try:
        es = ExpertSystem()
        es.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

