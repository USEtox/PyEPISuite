"""
Comprehensive example demonstrating PyEPISuite caching functionality.

This example shows how the caching system works for both submit_to_episuite
and search functions, comparing performance between cached and non-cached runs.
"""

import time
from pyepisuite.utils import (
    submit_to_episuite, clear_cache, search_episuite_by_cas, search_episuite,
    get_cache_dir
)
from pyepisuite.models import Identifiers
import logging

# Enable logging to see cache activity
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demonstrate_submit_caching():
    """Demonstrate caching for submit_to_episuite function."""
    print("=== Submit to EPI Suite Caching Demo ===")
    
    # Create sample identifiers for testing
    identifiers = [
        Identifiers(cas="50-00-0", name="Formaldehyde", smiles="C=O"),
        Identifiers(cas="71-43-2", name="Benzene", smiles="c1ccccc1")
    ]
    
    # Clear cache to start fresh
    clear_cache()
    print("Cache cleared.")
    
    # First run - will fetch from API and cache the results
    print("\n1. First run (no cache, will fetch from API):")
    start_time = time.time()
    try:
        epi_results, ecosar_results = submit_to_episuite(identifiers, use_cache=True)
        first_run_time = time.time() - start_time
        print(f"   Time taken: {first_run_time:.2f} seconds")
        print(f"   EPI Suite results: {len(epi_results)} compounds")
        print(f"   EcoSAR results: {len(ecosar_results)} compounds")
    except Exception as e:
        print(f"   Error: {e}")
        print("   (This is expected if API is not accessible)")
        return
    
    # Second run - will load from cache (much faster)
    print("\n2. Second run (cached results):")
    start_time = time.time()
    try:
        epi_results, ecosar_results = submit_to_episuite(identifiers, use_cache=True)
        second_run_time = time.time() - start_time
        print(f"   Time taken: {second_run_time:.2f} seconds")
        print(f"   EPI Suite results: {len(epi_results)} compounds")
        print(f"   EcoSAR results: {len(ecosar_results)} compounds")
        
        speedup = first_run_time / second_run_time if second_run_time > 0 else float('inf')
        print(f"   Speedup: {speedup:.1f}x faster")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Third run - bypass cache
    print("\n3. Third run (cache bypassed):")
    start_time = time.time()
    try:
        epi_results, ecosar_results = submit_to_episuite(identifiers, use_cache=False)
        third_run_time = time.time() - start_time
        print(f"   Time taken: {third_run_time:.2f} seconds")
        print(f"   EPI Suite results: {len(epi_results)} compounds")
        print(f"   EcoSAR results: {len(ecosar_results)} compounds")
    except Exception as e:
        print(f"   Error: {e}")

def demonstrate_search_caching():
    """Demonstrate caching for search functions."""
    print("\n=== Search Function Caching Demo ===")
    
    # Test search by CAS
    cas_numbers = ["50-00-0", "71-43-2"]
    
    print("\n1. Search by CAS numbers (first run):")
    start_time = time.time()
    try:
        results = search_episuite_by_cas(cas_numbers, use_cache=True)
        first_search_time = time.time() - start_time
        print(f"   Time taken: {first_search_time:.2f} seconds")
        print(f"   Results found: {len(results)} identifiers")
        for result in results[:3]:  # Show first 3 results
            print(f"   - {result.name}: {result.cas}")
    except Exception as e:
        print(f"   Error: {e}")
        print("   (This is expected if API is not accessible)")
        return
    
    print("\n2. Search by CAS numbers (cached run):")
    start_time = time.time()
    try:
        results = search_episuite_by_cas(cas_numbers, use_cache=True)
        second_search_time = time.time() - start_time
        print(f"   Time taken: {second_search_time:.2f} seconds")
        print(f"   Results found: {len(results)} identifiers")
        
        speedup = first_search_time / second_search_time if second_search_time > 0 else float('inf')
        print(f"   Speedup: {speedup:.1f}x faster")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test general search
    search_terms = ["benzene", "formaldehyde"]
    
    print("\n3. General search (first run):")
    start_time = time.time()
    try:
        results = search_episuite(search_terms, use_cache=True)
        first_general_time = time.time() - start_time
        print(f"   Time taken: {first_general_time:.2f} seconds")
        print(f"   Results found: {len(results)} identifiers")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    print("\n4. General search (cached run):")
    start_time = time.time()
    try:
        results = search_episuite(search_terms, use_cache=True)
        second_general_time = time.time() - start_time
        print(f"   Time taken: {second_general_time:.2f} seconds")
        print(f"   Results found: {len(results)} identifiers")
        
        speedup = first_general_time / second_general_time if second_general_time > 0 else float('inf')
        print(f"   Speedup: {speedup:.1f}x faster")
    except Exception as e:
        print(f"   Error: {e}")

def demonstrate_cache_management():
    """Demonstrate cache management features."""
    print("\n=== Cache Management Demo ===")
    
    cache_dir = get_cache_dir()
    print(f"Cache directory: {cache_dir}")
    
    # Count cache files
    cache_files = list(cache_dir.glob("*.json"))
    print(f"Cache files before clearing: {len(cache_files)}")
    
    # Show some cache file names
    for cache_file in cache_files[:5]:  # Show first 5
        print(f"  - {cache_file.name}")
    
    # Clear cache
    clear_cache()
    print("\nCache cleared.")
    
    # Count again
    cache_files_after = list(cache_dir.glob("*.json"))
    print(f"Cache files after clearing: {len(cache_files_after)}")

def main():
    """Main demonstration function."""
    print("PyEPISuite Comprehensive Caching System Demo")
    print("=" * 50)
    
    # Demonstrate submit caching
    demonstrate_submit_caching()
    
    # Demonstrate search caching
    demonstrate_search_caching()
    
    # Demonstrate cache management
    demonstrate_cache_management()
    
    print("\n=== Demo Complete ===")
    print("Key benefits of caching:")
    print("- Dramatically faster repeated operations")
    print("- Reduced API calls and network usage")
    print("- Persistent cache across Python sessions")
    print("- Automatic cache key generation")
    print("- Easy cache management and clearing")
    print("- Works for both submit and search operations")

if __name__ == "__main__":
    main()