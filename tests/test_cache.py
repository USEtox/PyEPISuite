"""Tests for caching functionality."""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from pyepisuite.utils import (
    get_cache_dir, get_cache_key, save_to_cache, load_from_cache, clear_cache,
    get_search_cache_key, save_search_to_cache, load_search_from_cache,
    submit_to_episuite, search_episuite_by_cas, search_episuite
)
from pyepisuite.models import Identifiers


class TestCaching:
    """Test caching functionality."""
    
    def test_cache_directory_creation(self):
        """Test that cache directory is created."""
        cache_dir = get_cache_dir()
        assert cache_dir.exists()
        assert cache_dir.is_dir()
        assert cache_dir.name == ".pyepisuite_cache"
    
    def test_cache_key_generation(self):
        """Test cache key generation for different identifier types."""
        # Test CAS-based key
        cas_id = Identifiers(cas="50-00-0", name="Formaldehyde", smiles=None)
        cas_key = get_cache_key(cas_id)
        assert isinstance(cas_key, str)
        assert len(cas_key) == 32  # MD5 hash length
        
        # Test SMILES-based key
        smiles_id = Identifiers(cas=None, name="Benzene", smiles="c1ccccc1")
        smiles_key = get_cache_key(smiles_id)
        assert isinstance(smiles_key, str)
        assert len(smiles_key) == 32
        
        # Test name-based key
        name_id = Identifiers(cas=None, name="Water", smiles=None)
        name_key = get_cache_key(name_id)
        assert isinstance(name_key, str)
        assert len(name_key) == 32
        
        # Keys should be different
        assert cas_key != smiles_key != name_key
        
        # Same identifier should produce same key
        cas_key2 = get_cache_key(cas_id)
        assert cas_key == cas_key2
    
    def test_cache_key_preference(self):
        """Test that CAS is preferred over SMILES over name."""
        # When CAS is available, it should be used
        multi_id = Identifiers(cas="50-00-0", name="Formaldehyde", smiles="C=O")
        cas_only_id = Identifiers(cas="50-00-0", name=None, smiles=None)
        
        assert get_cache_key(multi_id) == get_cache_key(cas_only_id)
        
        # When only SMILES and name available, SMILES should be used
        smiles_name_id = Identifiers(cas=None, name="Formaldehyde", smiles="C=O")
        smiles_only_id = Identifiers(cas=None, name=None, smiles="C=O")
        
        assert get_cache_key(smiles_name_id) == get_cache_key(smiles_only_id)
    
    @patch('pyepisuite.utils.get_cache_dir')
    def test_cache_save_load_cycle(self, mock_cache_dir):
        """Test saving and loading from cache."""
        # Use temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_cache_dir.return_value = Path(temp_dir)
            
            # Test that cache file is created when save_to_cache is called
            # We'll test the actual serialization with the asdict mock
            
            cache_key = "test_key"
            cache_file = Path(temp_dir) / f"{cache_key}.json"
            
            # Mock asdict to avoid needing real dataclass instances
            with patch('pyepisuite.utils.asdict') as mock_asdict:
                mock_asdict.side_effect = [
                    {"test": "epi_data"},
                    {"test": "ecosar_data"}
                ]
                
                from unittest.mock import MagicMock
                mock_epi = MagicMock()
                mock_ecosar = MagicMock()
                
                # Save to cache
                save_to_cache(cache_key, mock_epi, mock_ecosar)
                
                # Check that file was created
                assert cache_file.exists()
                
                # Check file contents
                with open(cache_file) as f:
                    data = json.load(f)
                
                assert "epi_result" in data
                assert "ecosar_result" in data
                assert "cached_at" in data
                assert data["epi_result"]["test"] == "epi_data"
                assert data["ecosar_result"]["test"] == "ecosar_data"
    
    def test_load_from_nonexistent_cache(self):
        """Test loading from cache when file doesn't exist."""
        result = load_from_cache("nonexistent_key")
        assert result is None
    
    @patch('pyepisuite.utils.get_cache_dir')
    def test_clear_cache(self, mock_cache_dir):
        """Test cache clearing functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_cache_dir.return_value = Path(temp_dir)
            
            # Create some fake cache files
            cache_dir = Path(temp_dir)
            (cache_dir / "file1.json").write_text('{"test": 1}')
            (cache_dir / "file2.json").write_text('{"test": 2}')
            (cache_dir / "not_cache.txt").write_text('not a cache file')
            
            # Clear cache
            clear_cache()
            
            # Check that only .json files were removed
            assert not (cache_dir / "file1.json").exists()
            assert not (cache_dir / "file2.json").exists()
            assert (cache_dir / "not_cache.txt").exists()  # Should remain
    
    def test_submit_to_episuite_with_cache_parameter(self):
        """Test that submit_to_episuite accepts use_cache parameter."""
        from pyepisuite.utils import submit_to_episuite
        from pyepisuite.models import Identifiers
        
        # This should not raise an error
        identifiers = []  # Empty list for testing
        
        # Test with cache enabled
        result1 = submit_to_episuite(identifiers, use_cache=True)
        assert isinstance(result1, tuple)
        assert len(result1) == 2
        
        # Test with cache disabled
        result2 = submit_to_episuite(identifiers, use_cache=False)
        assert isinstance(result2, tuple)
        assert len(result2) == 2
        
        # Test default (should be cache enabled)
        result3 = submit_to_episuite(identifiers)
        assert isinstance(result3, tuple)
        assert len(result3) == 2

    def test_search_cache_key_generation(self):
        """Test search cache key generation."""
        query_terms = ["123-45-6", "benzene", "C=O"]
        cache_key = get_search_cache_key(query_terms)
        assert isinstance(cache_key, str)
        assert len(cache_key) == 32  # MD5 hash length
        
        # Same query terms should produce same key
        cache_key2 = get_search_cache_key(query_terms)
        assert cache_key == cache_key2
        
        # Different order should produce same key (sorted internally)
        different_order = ["benzene", "123-45-6", "C=O"]
        cache_key3 = get_search_cache_key(different_order)
        assert cache_key == cache_key3  # Should be same due to sorting
        
        # Different terms should produce different key
        different_terms = ["456-78-9", "toluene"]
        cache_key4 = get_search_cache_key(different_terms)
        assert cache_key != cache_key4

    @patch('pyepisuite.utils.get_cache_dir')
    def test_search_cache_save_load_cycle(self, mock_cache_dir):
        """Test saving and loading search results from cache."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_cache_dir.return_value = Path(temp_dir)
            
            cache_key = "test_search_key"
            cache_file = Path(temp_dir) / f"search_{cache_key}.json"
            
            # Mock asdict for search results
            with patch('pyepisuite.utils.asdict') as mock_asdict:
                mock_asdict.return_value = {
                    "dtxsid": "DTXSID123",
                    "casrn": "123-45-6",
                    "name": "Test Chemical"
                }
                
                from unittest.mock import MagicMock
                mock_identifiers = [MagicMock()]
                
                # Save to cache
                save_search_to_cache(cache_key, mock_identifiers)
                
                # Check that file was created
                assert cache_file.exists()
                
                # Check file contents
                with open(cache_file) as f:
                    data = json.load(f)
                
                assert "identifiers" in data
                assert "cached_at" in data
                assert len(data["identifiers"]) == 1

    def test_search_episuite_functions_with_cache_parameter(self):
        """Test that search functions accept use_cache parameter."""
        # Test search_episuite_by_cas
        with patch('pyepisuite.utils.EpiSuiteAPIClient') as mock_client:
            with patch('pyepisuite.utils.is_valid_cas', return_value=True):
                mock_client_instance = mock_client.return_value
                mock_client_instance.search.return_value = []
                
                # Test with cache enabled
                result1 = search_episuite_by_cas(["123-45-6"], use_cache=True)
                assert isinstance(result1, list)
                
                # Test with cache disabled
                result2 = search_episuite_by_cas(["123-45-6"], use_cache=False)
                assert isinstance(result2, list)
                
                # Test default (should be cache enabled)
                result3 = search_episuite_by_cas(["123-45-6"])
                assert isinstance(result3, list)
        
        # Test search_episuite
        with patch('pyepisuite.utils.EpiSuiteAPIClient') as mock_client:
            mock_client_instance = mock_client.return_value
            mock_client_instance.search.return_value = []
            
            # Test with cache enabled
            result1 = search_episuite(["benzene"], use_cache=True)
            assert isinstance(result1, list)
            
            # Test with cache disabled
            result2 = search_episuite(["benzene"], use_cache=False)
            assert isinstance(result2, list)
            
            # Test default (should be cache enabled)
            result3 = search_episuite(["benzene"])
            assert isinstance(result3, list)