#include <iostream>
#include <vector>
#include <cmath>
#include <complex>

bool is_prime(unsigned long long n) {
    if (n < 2) return false;
    if (n % 2 == 0) return (n == 2);
    for (unsigned long long i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// Generate the T sequence up to limit
std::vector<int> generate_T(size_t limit) {
    std::vector<int> T;
    T.reserve(limit);
    for (size_t n = 0; n < limit; ++n) {
        unsigned long long odd_val = 2 * n + 1;
        T.push_back(is_prime(odd_val) ? 1 : 0);
    }
    return T;
}

int main() {
    size_t limit = 1000; // example
    auto T = generate_T(limit);

    for (size_t i = 0; i < T.size(); ++i) {
        std::cout << (2 * i + 1) << ": " << T[i] << "\n";
    }

    return 0;
}
