// spectral_t.cpp
// C++17 — builds T[n] for odd primes (o_n = 2n+1) via several methods:
//  - T_from_formula: direct progression/floor test per-index
//  - progression_marking_T: mark composites using progressions n_p(m)
//  - T_via_sieve: exact odd-only sieve (recommended)
//
// Compile: g++ -O2 -std=c++17 spectral_t.cpp -o spectral_t

#include <bits/stdc++.h>
using namespace std;

// -------------------------
// Sieve primes up to limit
// -------------------------
vector<int> primes_upto(int limit) {
    if (limit < 2) return {};
    int n = limit;
    vector<char> is_prime(n+1, true);
    is_prime[0] = is_prime[1] = false;
    int r = (int)floor(sqrt((double)n));
    for (int p = 2; p <= r; ++p) {
        if (is_prime[p]) {
            for (int q = p*p; q <= n; q += p) is_prime[q] = false;
        }
    }
    vector<int> primes;
    primes.reserve(n / 10);
    for (int i = 2; i <= n; ++i) if (is_prime[i]) primes.push_back(i);
    return primes;
}

// -------------------------
// T_from_formula: test single n
// -------------------------
int T_from_formula(long long n, const vector<int>* primes_opt = nullptr) {
    if (n < 1) return 0;
    long long o = 2*n + 1;
    if (o == 3) return 1;
    vector<int> local_primes;
    const vector<int>* primes = primes_opt;
    if (!primes) {
        // to be safe, generate primes up to sqrt(o)
        int lim = (int)floor(sqrt((long double)o)) + 1;
        local_primes = primes_upto(max(lim, 3));
        primes = &local_primes;
    }
    for (int p : *primes) {
        if (p < 3) continue;
        long long base = (3LL * p - 1) / 2;
        if (base > n) break;
        long long diff = n - base;
        if (diff >= 0 && (diff % p) == 0) {
            // n is in progression for prime p => composite form
            return 0;
        }
    }
    return 1;
}

// -------------------------
// progression_marking_T: build T[0..N] by marking progressions
// -------------------------
vector<char> progression_marking_T(int N, int p_max = -1) {
    // T[n] as char (0/1)
    vector<char> T(N+1, 1);
    T[0] = 0; // o_0 = 1
    if (p_max < 0) p_max = 2 * N + 1;
    vector<int> primes = primes_upto(p_max);
    for (int p : primes) {
        if (p < 3) continue;
        long long base = (3LL * p - 1) / 2;
        if (base > N) break;
        for (long long n = base; n <= N; n += p) {
            T[(size_t)n] = 0;
        }
    }
    return T;
}

// -------------------------
// T_via_sieve: exact odd-only sieve
// -------------------------
vector<char> T_via_sieve(int N) {
    // limit = 2N + 1
    long long limit = 2LL * N + 1;
    if (limit < 2) return vector<char>(N+1, 0);
    // only store odd indices: index i represents number (2*i + 1)
    int size = (int)((limit + 1) / 2); // number of odd numbers up to limit
    vector<char> is_prime_odd(size, 1);
    is_prime_odd[0] = 0; // 1 is not prime
    int max_i = (int)(floor(sqrt((long double)limit)) / 2);
    for (int i = 1; i <= max_i; ++i) {
        if (!is_prime_odd[i]) continue;
        int p = 2*i + 1;
        int start = (p * p - 1) / 2;
        for (int j = start; j < size; j += p) is_prime_odd[j] = 0;
    }
    vector<char> T(N+1, 0);
    for (int n = 0; n <= N; ++n) {
        if (n < size && is_prime_odd[n]) T[n] = 1;
        else T[n] = 0;
    }
    return T;
}

// -------------------------
// utility: show sample
// -------------------------
void show_T_sample(const vector<char>& T, int max_show = 40) {
    cout << " n   o_n   T[n]\n";
    int limit = min((int)T.size()-1, max_show-1);
    for (int n = 0; n <= limit; ++n) {
        cout << setw(2) << n << "  " << setw(5) << (2*n+1) << "   " << (int)T[n] << "\n";
    }
}

// -------------------------
// Demo main
// -------------------------
int main(int argc, char** argv) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "spectral_t C++ demo\n";

    int N = 50;
    cout << "\nExact sieve T_via_sieve (N=" << N << ")\n";
    auto T_exact = T_via_sieve(N);
    show_T_sample(T_exact);

    cout << "\nProgression marking (p_max=200) T_prog\n";
    auto T_prog = progression_marking_T(N, 200);
    show_T_sample(T_prog);

    cout << "\nSingle-index T_from_formula tests\n";
    vector<int> tests = {1, 5, 10, 20};
    auto primes_sample = primes_upto(1000);
    for (int n : tests) {
        cout << "n=" << n << ", o_n=" << (2*n+1)
             << ", T_from_formula=" << T_from_formula(n, &primes_sample)
             << ", T_exact=" << (int)T_exact[n] << "\n";
    }

    return 0;
}
