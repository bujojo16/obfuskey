class PrimeCalculator:

    def is_prime(number):
        if (number%2 == 0):
            return False
        else:
            for i in range(3, number):
                if (number%i == 0):
                    return False
        return True

    def find_next_prime(number):
        found = False
        while not found:
            number+=1
            if (PrimeCalculator.is_prime(number)):
                found = True
       #print(number)
        return number

    def find_prime(number):
        if not PrimeCalculator.is_prime(number):
            return PrimeCalculator.find_next_prime(number)
        else:
            return number
        
if __name__ == '__main__':
    print(PrimeCalculator.find_next_prime(20011))
