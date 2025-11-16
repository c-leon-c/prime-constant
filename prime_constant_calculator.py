import gmpy2, time
from gmpy2 import mpfr

PRECISION = 1_000_000
gmpy2.get_context().precision = PRECISION

def first_n_primes(n):
    """Generate first n primes efficiently"""
    print(f"Generating {n} primes...")
    start = time.time()
    
    # Simple sieve, eh good enough for this
    if n < 2: return []
    limit = max(100, n * 15)  # reasonable upper bound
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    
    primes = [i for i, is_p in enumerate(sieve) if is_p][:n]
    print(f"Generated {len(primes)} primes in {time.time() - start:.1f}s")
    return primes

def compute_constant_million_fixed(num_terms):
    print(f"\nComputing {num_terms} terms at {PRECISION} bit precision...")
    
    start = time.time()
    
    # Generate primes
    primes = first_n_primes(num_terms * 2)
    
    total = mpfr('1')  # Start with 1
    
    for n in range(1, num_terms + 1):
        p1 = primes[2*(n-1)]      # first prime in pair
        p2 = primes[2*(n-1) + 1]  # second prime in pair
        
        # Use gmpy2's fast square root
        sqrt_p1 = gmpy2.sqrt(mpfr(p1))
        sqrt_p2 = gmpy2.sqrt(mpfr(p2))
        term = (sqrt_p1 + sqrt_p2) / (mpfr(10) ** n)
        total += term
        
        # Progress every 1000 terms
        if n % 1000 == 0:
            elapsed = time.time() - start
            current_value = float(total)
            print(f"   Term {n} - {elapsed:.1f}s - {current_value:.10f}")
    
    total_time = time.time() - start
    print(f"Computation complete!")
    print(f"Total time: {total_time:.1f}s")
    
    # Save the result
    result_str = str(total)
    with open('prime_constant.txt', 'w') as f:
        f.write(result_str)
    
    print(f"Saved!")
    print(f"First 50 decimals: {result_str[2:52]}")
    print(f"Last 50 decimals: {result_str[-50:]}")
    
    return total_time, result_str[2:52]  # return first 50 decimals

# ========== RUN!!! ==========
print("Prime Constant Calculation")
print("="*50)
print("Target: ~300,000 decimal digits")

try:
    time_taken, first_50 = compute_constant_million_fixed(10000)
    print(f"Complete in {time_taken:.1f} seconds!")
    print(f"Prime constant to 50 decimals: {first_50}")
    
except KeyboardInterrupt:
    print("Stopped early")
except Exception as e:
    print(f"Error: {e}")
