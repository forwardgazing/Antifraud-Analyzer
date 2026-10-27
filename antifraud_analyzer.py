import csv
from datetime import datetime

def analyze_transactions(file_path):
    print(f"--- Анализ транзакций: {file_path} ---")
    suspicious_count = 0

    try:
        # Открываем файл. encoding='utf-8-sig' убирает невидимые символы Excel в начале файла.
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            # Читаем первую строку, чтобы понять, какой разделитель используется (запятая или точка с запятой)
            first_line = file.readline()
            delimiter = ';' if ';' in first_line else ','
            file.seek(0) # Возвращаемся в начало файла
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            print("🚨 Подозрительные транзакции:")
            for row in reader:
                # Преобразуем строку времени в объект datetime
                # Убираем лишние пробелы по краям с помощью .strip()
                time_str = row['time'].strip()
                tx_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                amount = int(row['amount'])
                
                # Правило антифрода: Сумма > 100 000 И время между 00:00 и 06:00
                if amount > 100000 and 0 <= tx_time.hour < 6:
                    print(f" -> ID: {row['transaction_id']} | Клиент: {row['user_name']} | "
                          f"Сумма: {amount} руб. | Город: {row['city']} | Время: {time_str}")
                    suspicious_count += 1
                    
        print(f"\nВсего найдено подозрительных транзакций: {suspicious_count}")
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")

if __name__ == "__main__":
    analyze_transactions("transactions.csv")
