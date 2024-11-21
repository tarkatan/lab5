import random

def is_prime_miller_rabin(p, k):
    # Базові перевірки
    if p <= 1:
        return False, 0
    if p <= 3:
        return True, 1.0
    if p % 2 == 0:
        return False, 0
    
    # Представлення n-1 у вигляді 2^s * d
    s, d = 0, p - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # Тест Міллера-Рабіна
    def check_composite(a):
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            return False  # Не складене
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                return False  # Не складене
        return True  # Складене
    
    for _ in range(k):
        a = random.randint(2, p - 2)
        if check_composite(a):
            return False, 0  # Складене
    
    # Якщо всі перевірки пройдені, число вважається простим з імовірністю
    probability = 1 - (1 / (2 ** k))
    return True, probability

# Введення даних
p = int(input("Введіть непарне натуральне число p (> 3): "))
k = int(input("Введіть кількість раундів k: "))

# Результат перевірки
is_prime, probability = is_prime_miller_rabin(p, k)
if is_prime:
    print(f"{p} є простим числом з імовірністю {probability:.10f}")
else:
    print(f"{p} є складеним числом")
