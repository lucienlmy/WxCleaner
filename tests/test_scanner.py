import os
import tempfile
import pytest
from scanner import calculate_hash, find_duplicates

def test_calculate_hash_basic():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"Hello Conductor WxCleaner")
        f_path = f.name
    
    try:
        full_hash = calculate_hash(f_path)
        assert full_hash is not None
        assert len(full_hash) == 64
        
        # calculate again to ensure determinism
        assert calculate_hash(f_path) == full_hash
        
        # partial hash should also work
        partial_hash = calculate_hash(f_path, partial=True)
        assert partial_hash is not None
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)

def test_calculate_hash_nonexistent():
    res = calculate_hash("path/does/not/exist_12345.bin")
    assert res is None

def test_calculate_hash_partial_vs_full():
    # Create file > 1024 bytes with same prefix but different suffix
    content_prefix = b"A" * 1024
    with tempfile.NamedTemporaryFile(delete=False) as f1, tempfile.NamedTemporaryFile(delete=False) as f2:
        f1.write(content_prefix + b"_file1_unique_content")
        f2.write(content_prefix + b"_file2_different_content")
        p1, p2 = f1.name, f2.name
    
    try:
        # Partial hashes must match
        assert calculate_hash(p1, partial=True) == calculate_hash(p2, partial=True)
        # Full hashes must differ
        assert calculate_hash(p1, partial=False) != calculate_hash(p2, partial=False)
    finally:
        for p in (p1, p2):
            if os.path.exists(p):
                os.remove(p)

def test_find_duplicates_empty_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        res = find_duplicates(temp_dir)
        assert res == {}

def test_find_duplicates_ignores_empty_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        f1 = os.path.join(temp_dir, "empty1.txt")
        f2 = os.path.join(temp_dir, "empty2.txt")
        open(f1, "w").close()
        open(f2, "w").close()
        
        res = find_duplicates(temp_dir)
        assert res == {}

def test_find_duplicates_with_callback_and_nested_dirs():
    callback_calls = []
    def callback(current, total, status_text):
        callback_calls.append((current, total, status_text))

    with tempfile.TemporaryDirectory() as temp_dir:
        sub_dir = os.path.join(temp_dir, "sub")
        os.makedirs(sub_dir)
        
        # Duplicate group 1 (2 files)
        d1_a = os.path.join(temp_dir, "file_a.txt")
        d1_b = os.path.join(sub_dir, "file_b.txt")
        with open(d1_a, "wb") as f: f.write(b"Duplicate Group 1 content")
        with open(d1_b, "wb") as f: f.write(b"Duplicate Group 1 content")
        
        # Unique file
        unique_file = os.path.join(temp_dir, "unique.txt")
        with open(unique_file, "wb") as f: f.write(b"Unique file content")
        
        # Same prefix different tail
        prefix = b"P" * 1024
        p_diff1 = os.path.join(temp_dir, "p1.dat")
        p_diff2 = os.path.join(temp_dir, "p2.dat")
        with open(p_diff1, "wb") as f: f.write(prefix + b"tail_1")
        with open(p_diff2, "wb") as f: f.write(prefix + b"tail_2")
        
        results = find_duplicates(temp_dir, progress_callback=callback)
        
        assert len(results) == 1
        paths = list(results.values())[0]
        assert len(paths) == 2
        assert os.path.abspath(d1_a) in [os.path.abspath(p) for p in paths]
        assert os.path.abspath(d1_b) in [os.path.abspath(p) for p in paths]
        
        # Verify callback was called
        assert len(callback_calls) > 0
