from concurrent.futures import ProcessPoolExecutor

from time import perf_counter

from multiprocessing import cpu_count

from random import randint


def factorize(number: int) -> list[int]:
    result = [1, number]
    for divider in range(2, int(number**0.5) + 1):
        if number % divider == 0:
            result.append(divider)
            result.append(number // divider)
    return sorted(result)


def factorize_all(*numbers: int) -> list[list[int]]:
    result = []
    for number in numbers:
        result.append(factorize(number))
    return result


if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    a, b, c, d = factorize_all(*numbers)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158,
                 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212,
                 2662765, 5325530, 10651060]

    for i in range(1000):
        numbers.append(randint(100, 1000000000))

    start_time = perf_counter()

    for number in numbers:
        factorize(number)

    end_time = perf_counter()

    print(f"Час синхронного виконання - {end_time - start_time :0.3f} секунд.")

    number_of_cores = cpu_count()
    print(f"Кількість ядер - {number_of_cores}.")

    for number_of_processes in range(1, number_of_cores + 1):
        start_time = perf_counter()

        with ProcessPoolExecutor(number_of_processes) as executor:
            for number, dividers in zip(numbers, executor.map(factorize, numbers)):
                pass

        end_time = perf_counter()

        print(
            f"Час виконання з {number_of_processes} процесами - {end_time - start_time :0.3f} секунд."
        )
