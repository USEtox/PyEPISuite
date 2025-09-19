"""
Example of using PyEPISuite with caching functionality.

This example demonstrates how the caching system works:
1. First call makes API request and saves to cache
2. Subsequent calls load from cache (much faster)
"""

from pyepisuite.utils import search_episuite_by_cas, submit_to_episuite, clear_cache, get_cache_dir
import logging

# Enable logging to see cache activity
logging.basicConfig(level=logging.INFO)

def main():
    # Example CAS numbers
    cas_list = ["50-00-0", "67-56-1"]  # Formaldehyde, Methanol
    
    print("Cache directory:", get_cache_dir())
    print("\n" + "="*50)
    print("FIRST RUN - API calls will be made")
    print("="*50)
    
    # Search for chemicals
    identifiers = search_episuite_by_cas(cas_list)
    print(f"Found {len(identifiers)} chemicals")
    
    # Submit with caching enabled (default)
    epi_results, ecosar_results = submit_to_episuite(identifiers, use_cache=True)
    print(f"Retrieved {len(epi_results)} EPI results")
    
    print("\n" + "="*50)
    print("SECOND RUN - Results loaded from cache")
    print("="*50)
    
    # Run again - should load from cache
    identifiers2 = search_episuite_by_cas(cas_list)
    epi_results2, ecosar_results2 = submit_to_episuite(identifiers2, use_cache=True)
    print(f"Retrieved {len(epi_results2)} EPI results from cache")
    
    print("\n" + "="*50)
    print("CACHE MANAGEMENT")
    print("="*50)
    
    # You can disable caching if needed
    print("Running without cache...")
    epi_results3, ecosar_results3 = submit_to_episuite(identifiers, use_cache=False)
    
    # Clear cache when done
    print("\nClearing cache...")
    clear_cache()
    
    print("\nCache example completed!")

if __name__ == "__main__":
    main()