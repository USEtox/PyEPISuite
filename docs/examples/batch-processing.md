# Batch Processing

This guide covers efficient processing of large chemical datasets with PyEPISuite.

## Overview

When working with hundreds or thousands of chemicals, proper batch processing becomes essential for:

- **Performance**: Minimizing API overhead
- **Reliability**: Handling failures gracefully  
- **Memory Management**: Processing data in manageable chunks
- **Progress Tracking**: Monitoring long-running operations

## Basic Batch Processing

### Simple Batch Function

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import episuite_to_dataframe, ecosar_to_dataframe
import time

def process_chemical_batch(cas_list, batch_size=50, delay=1.0):
    """
    Process chemicals in batches with rate limiting.
    
    Args:
        cas_list: List of CAS numbers
        batch_size: Number of chemicals per batch
        delay: Delay between batches (seconds)
    
    Returns:
        tuple: (epi_results, ecosar_results, failed_chemicals)
    """
    all_epi_results = []
    all_ecosar_results = []
    failed_chemicals = []
    
    total_batches = (len(cas_list) + batch_size - 1) // batch_size
    
    for i in range(0, len(cas_list), batch_size):
        batch_num = i // batch_size + 1
        batch = cas_list[i:i + batch_size]
        
        print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} chemicals)")
        
        try:
            # Search for chemicals in this batch
            ids = search_episuite_by_cas(batch)
            
            if ids:
                # Submit for predictions
                epi_batch, ecosar_batch = submit_to_episuite(ids)
                
                all_epi_results.extend(epi_batch)
                all_ecosar_results.extend(ecosar_batch)
                
                print(f"  Successfully processed {len(epi_batch)} chemicals")
            else:
                print(f"  No valid chemicals found in batch")
                failed_chemicals.extend(batch)
                
        except Exception as e:
            print(f"  Error processing batch: {e}")
            failed_chemicals.extend(batch)
        
        # Rate limiting
        if delay > 0 and batch_num < total_batches:
            time.sleep(delay)
    
    return all_epi_results, all_ecosar_results, failed_chemicals
```

### Usage Example

```python
# Large dataset of chemicals
chemical_cas_numbers = [
    "50-00-0", "67-56-1", "64-17-5", "67-64-1", "100-41-4",
    "108-88-3", "71-43-2", "100-42-5", "106-42-3", "95-47-6",
    # ... many more chemicals
]

# Process in batches
epi_results, ecosar_results, failed = process_chemical_batch(
    chemical_cas_numbers, 
    batch_size=25,
    delay=2.0
)

print(f"\\nBatch Processing Summary:")
print(f"Total chemicals: {len(chemical_cas_numbers)}")
print(f"Successfully processed: {len(epi_results)}")
print(f"Failed: {len(failed)}")
print(f"Success rate: {len(epi_results)/len(chemical_cas_numbers)*100:.1f}%")
```

## Advanced Batch Processing

### Progress Tracking with tqdm

```python
from tqdm import tqdm
import pandas as pd

def process_with_progress(cas_list, batch_size=50):
    """Process chemicals with progress bar."""
    all_results = []
    failed_chemicals = []
    
    # Create progress bar
    pbar = tqdm(total=len(cas_list), desc="Processing chemicals")
    
    for i in range(0, len(cas_list), batch_size):
        batch = cas_list[i:i + batch_size]
        
        try:
            ids = search_episuite_by_cas(batch)
            
            if ids:
                epi_batch, _ = submit_to_episuite(ids)
                all_results.extend(epi_batch)
            else:
                failed_chemicals.extend(batch)
                
        except Exception as e:
            tqdm.write(f"Error in batch {i//batch_size + 1}: {e}")
            failed_chemicals.extend(batch)
        
        # Update progress
        pbar.update(len(batch))
        
        # Update description with current stats
        success_count = len(all_results)
        pbar.set_postfix({
            'success': success_count,
            'failed': len(failed_chemicals)
        })
    
    pbar.close()
    return all_results, failed_chemicals

# Usage
# pip install tqdm  # Install if needed
results, failed = process_with_progress(chemical_cas_numbers)
```

### Concurrent Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class BatchProcessor:
    """Thread-safe batch processor for EPISuite data."""
    
    def __init__(self, max_workers=3, batch_size=20):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.results_lock = threading.Lock()
        self.all_results = []
        self.failed_chemicals = []
    
    def process_single_batch(self, batch, batch_id):
        """Process a single batch of chemicals."""
        try:
            ids = search_episuite_by_cas(batch)
            
            if ids:
                epi_results, ecosar_results = submit_to_episuite(ids)
                
                # Thread-safe result storage
                with self.results_lock:
                    self.all_results.extend(epi_results)
                
                return {
                    'batch_id': batch_id,
                    'success_count': len(epi_results),
                    'failed_count': 0
                }
            else:
                with self.results_lock:
                    self.failed_chemicals.extend(batch)
                
                return {
                    'batch_id': batch_id,
                    'success_count': 0,
                    'failed_count': len(batch)
                }
                
        except Exception as e:
            with self.results_lock:
                self.failed_chemicals.extend(batch)
            
            return {
                'batch_id': batch_id,
                'success_count': 0,
                'failed_count': len(batch),
                'error': str(e)
            }
    
    def process_concurrent(self, cas_list):
        """Process chemicals using multiple threads."""
        # Split into batches
        batches = [
            cas_list[i:i + self.batch_size] 
            for i in range(0, len(cas_list), self.batch_size)
        ]
        
        # Process batches concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all batches
            future_to_batch = {
                executor.submit(self.process_single_batch, batch, i): i
                for i, batch in enumerate(batches)
            }
            
            # Collect results as they complete
            for future in tqdm(as_completed(future_to_batch), 
                             total=len(batches), 
                             desc="Processing batches"):
                
                batch_result = future.result()
                
                if 'error' in batch_result:
                    tqdm.write(f"Batch {batch_result['batch_id']} failed: {batch_result['error']}")
        
        return self.all_results, self.failed_chemicals

# Usage
processor = BatchProcessor(max_workers=3, batch_size=15)
results, failed = processor.process_concurrent(chemical_cas_numbers)

print(f"Concurrent processing completed:")
print(f"  Successful: {len(results)}")
print(f"  Failed: {len(failed)}")
```

## Memory-Efficient Processing

### Streaming Results to File

```python
import json
import csv
from datetime import datetime

class StreamingProcessor:
    """Process chemicals and stream results to files."""
    
    def __init__(self, output_prefix="episuite_batch"):
        self.output_prefix = output_prefix
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def process_and_save(self, cas_list, batch_size=50):
        """Process chemicals and save results incrementally."""
        
        # Prepare output files
        epi_filename = f"{self.output_prefix}_epi_{self.timestamp}.csv"
        ecosar_filename = f"{self.output_prefix}_ecosar_{self.timestamp}.csv"
        failed_filename = f"{self.output_prefix}_failed_{self.timestamp}.txt"
        
        epi_file_initialized = False
        ecosar_file_initialized = False
        
        processed_count = 0
        failed_count = 0
        
        for i in range(0, len(cas_list), batch_size):
            batch = cas_list[i:i + batch_size]
            
            try:
                ids = search_episuite_by_cas(batch)
                
                if ids:
                    epi_results, ecosar_results = submit_to_episuite(ids)
                    
                    # Convert to DataFrames
                    if epi_results:
                        epi_df = episuite_to_dataframe(epi_results)
                        
                        # Write to CSV (append mode)
                        if not epi_file_initialized:
                            epi_df.to_csv(epi_filename, index=False)
                            epi_file_initialized = True
                        else:
                            epi_df.to_csv(epi_filename, mode='a', header=False, index=False)
                    
                    if ecosar_results:
                        ecosar_df = ecosar_to_dataframe(ecosar_results)
                        
                        if not ecosar_file_initialized:
                            ecosar_df.to_csv(ecosar_filename, index=False)
                            ecosar_file_initialized = True
                        else:
                            ecosar_df.to_csv(ecosar_filename, mode='a', header=False, index=False)
                    
                    processed_count += len(epi_results)
                
            except Exception as e:
                # Log failed chemicals
                with open(failed_filename, 'a') as f:
                    for cas in batch:
                        f.write(f"{cas}: {str(e)}\\n")
                
                failed_count += len(batch)
            
            # Progress update
            print(f"Processed {min(i + batch_size, len(cas_list))}/{len(cas_list)} chemicals")
        
        return {
            'processed': processed_count,
            'failed': failed_count,
            'epi_file': epi_filename if epi_file_initialized else None,
            'ecosar_file': ecosar_filename if ecosar_file_initialized else None,
            'failed_file': failed_filename if failed_count > 0 else None
        }

# Usage
processor = StreamingProcessor("my_analysis")
results = processor.process_and_save(chemical_cas_numbers, batch_size=30)

print("Streaming processing completed:")
for key, value in results.items():
    print(f"  {key}: {value}")
```

## Error Recovery and Resumption

### Checkpointing for Large Datasets

```python
import pickle
import os

class CheckpointProcessor:
    """Processor with checkpoint/resume capability."""
    
    def __init__(self, checkpoint_file="episuite_checkpoint.pkl"):
        self.checkpoint_file = checkpoint_file
        self.processed_cas = set()
        self.all_results = []
        self.failed_chemicals = []
        
        # Load existing checkpoint
        self.load_checkpoint()
    
    def load_checkpoint(self):
        """Load previous progress from checkpoint file."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'rb') as f:
                    checkpoint = pickle.load(f)
                
                self.processed_cas = checkpoint.get('processed_cas', set())
                self.all_results = checkpoint.get('results', [])
                self.failed_chemicals = checkpoint.get('failed', [])
                
                print(f"Resumed from checkpoint: {len(self.processed_cas)} chemicals already processed")
                
            except Exception as e:
                print(f"Error loading checkpoint: {e}")
                print("Starting fresh...")
    
    def save_checkpoint(self):
        """Save current progress to checkpoint file."""
        checkpoint = {
            'processed_cas': self.processed_cas,
            'results': self.all_results,
            'failed': self.failed_chemicals
        }
        
        with open(self.checkpoint_file, 'wb') as f:
            pickle.dump(checkpoint, f)
    
    def process_with_checkpoints(self, cas_list, batch_size=50, checkpoint_interval=5):
        """Process with regular checkpointing."""
        
        # Filter out already processed chemicals
        remaining_cas = [cas for cas in cas_list if cas not in self.processed_cas]
        
        if not remaining_cas:
            print("All chemicals already processed!")
            return self.all_results, self.failed_chemicals
        
        print(f"Processing {len(remaining_cas)} remaining chemicals...")
        
        batch_count = 0
        
        for i in range(0, len(remaining_cas), batch_size):
            batch = remaining_cas[i:i + batch_size]
            batch_count += 1
            
            try:
                ids = search_episuite_by_cas(batch)
                
                if ids:
                    epi_results, _ = submit_to_episuite(ids)
                    self.all_results.extend(epi_results)
                    
                    # Mark as processed
                    for result in epi_results:
                        self.processed_cas.add(result.chemicalProperties.cas)
                else:
                    self.failed_chemicals.extend(batch)
                    self.processed_cas.update(batch)
                
            except Exception as e:
                print(f"Error in batch {batch_count}: {e}")
                self.failed_chemicals.extend(batch)
                self.processed_cas.update(batch)
            
            # Save checkpoint periodically
            if batch_count % checkpoint_interval == 0:
                self.save_checkpoint()
                print(f"Checkpoint saved after batch {batch_count}")
        
        # Final checkpoint
        self.save_checkpoint()
        
        return self.all_results, self.failed_chemicals

# Usage
processor = CheckpointProcessor("my_large_analysis.pkl")
results, failed = processor.process_with_checkpoints(
    chemical_cas_numbers, 
    batch_size=25,
    checkpoint_interval=3
)

# Clean up checkpoint file when done
# os.remove("my_large_analysis.pkl")
```

## Performance Optimization

### Optimized Batch Sizes

```python
import time

def find_optimal_batch_size(test_cas_list, max_batch_size=100):
    """Find optimal batch size for your setup."""
    
    batch_sizes = [10, 25, 50, 75, 100]
    test_chemicals = test_cas_list[:50]  # Use subset for testing
    
    results = {}
    
    for batch_size in batch_sizes:
        if batch_size > len(test_chemicals):
            continue
            
        print(f"Testing batch size: {batch_size}")
        
        start_time = time.time()
        
        try:
            # Test processing
            ids = search_episuite_by_cas(test_chemicals[:batch_size])
            if ids:
                epi_results, _ = submit_to_episuite(ids)
                success_count = len(epi_results)
            else:
                success_count = 0
            
            end_time = time.time()
            duration = end_time - start_time
            
            results[batch_size] = {
                'duration': duration,
                'chemicals_per_second': success_count / duration if duration > 0 else 0,
                'success_count': success_count
            }
            
            print(f"  Duration: {duration:.2f}s, Rate: {results[batch_size]['chemicals_per_second']:.2f} chemicals/s")
            
        except Exception as e:
            print(f"  Failed: {e}")
            results[batch_size] = {'error': str(e)}
        
        time.sleep(1)  # Brief pause between tests
    
    # Find optimal batch size
    valid_results = {k: v for k, v in results.items() if 'error' not in v}
    
    if valid_results:
        optimal_batch = max(valid_results.keys(), 
                          key=lambda k: valid_results[k]['chemicals_per_second'])
        print(f"\\nOptimal batch size: {optimal_batch}")
        return optimal_batch
    else:
        print("\\nNo successful batches found")
        return 10  # Conservative default

# Usage
# optimal_size = find_optimal_batch_size(chemical_cas_numbers[:100])
```

## Best Practices Summary

1. **Start Small**: Test with small batches first
2. **Handle Errors**: Always include exception handling
3. **Rate Limiting**: Add delays to avoid overwhelming the API
4. **Progress Tracking**: Use progress bars for long operations
5. **Checkpointing**: Save progress for very large datasets
6. **Memory Management**: Stream results to files for huge datasets
7. **Concurrent Processing**: Use threading carefully (3-5 threads max)
8. **Monitoring**: Log errors and track success rates

## Troubleshooting

### Common Issues

- **Timeout Errors**: Increase batch delay or reduce batch size
- **Memory Issues**: Use streaming processors for large datasets
- **API Rate Limits**: Implement exponential backoff
- **Network Issues**: Add retry logic with increasing delays

### Recovery Strategies

```python
def robust_batch_process(cas_list, max_retries=3):
    """Batch processing with retry logic."""
    
    for attempt in range(max_retries):
        try:
            return process_chemical_batch(cas_list)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print("All retry attempts failed")
                raise
```

This comprehensive guide should help you efficiently process large chemical datasets with PyEPISuite while maintaining reliability and performance.
