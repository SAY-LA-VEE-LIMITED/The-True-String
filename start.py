import os
import pickle
from sympy import isprime

class TrueStringGenerator:
    def __init__(self, state_file='true_string_state.pkl'):
        self.T = {}  # key: value, value: either number or 0 if collision
        self.max_m = -1
        self.max_n = -1
        self.state_file = state_file
        self.load_state()

    def f(self, m, n):
        return 4 + 3*m + 3*n + 2*m*n

    def save_state(self):
        with open(self.state_file, 'wb') as f:
            pickle.dump((self.T, self.max_m, self.max_n), f)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'rb') as f:
                self.T, self.max_m, self.max_n = pickle.load(f)
        else:
            self.T = {}
            self.max_m = -1
            self.max_n = -1

    def generate_up_to(self, target_m, target_n):
        for m in range(self.max_m + 1, target_m + 1):
            for n in range(0, target_n + 1):
                val = self.f(m, n)
                if val not in self.T:
                    self.T[val] = val
                else:
                    self.T[val] = 0
            self.max_n = target_n  # Update max_n fully for this m
            self.max_m = m
            self.save_state()  # Save after each m iteration

    def get_sorted_T(self):
        return [(k, self.T[k], isprime(k)) for k in sorted(self.T.keys())]

if __name__ == "__main__":
    generator = TrueStringGenerator()
    # Example: generate up to m=100, n=100
    generator.generate_up_to(100, 100)
    # Print sample output
    for k, v, prime_flag in generator.get_sorted_T()[:50]:
        print(f"{k}: {'0 (collision)' if v == 0 else 'prime' if prime_flag else 'unique non-prime'}")
