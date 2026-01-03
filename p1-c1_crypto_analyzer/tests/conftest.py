import pytest
import tempfile
import os


@pytest.fixture
def sample_ciphertext():
    from crypto.caesar import CaesarCipher
    plaintext = "The Caesar cipher is one of the simplest encryption techniques"
    return CaesarCipher.encrypt(plaintext, 7)


@pytest.fixture
def temp_data_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create stopwords file
        stopwords_file = os.path.join(tmpdir, "stopwords_en.txt")
        with open(stopwords_file, "w") as f:
            f.write("the\nand\nto\nof\na\nin\nthat\nis\nwas\n")
        
        # Create dictionary file
        dict_file = os.path.join(tmpdir, "words_en.txt")
        with open(dict_file, "w") as f:
            f.write("hello\nworld\ntest\nmessage\ncipher\n")
        
        yield tmpdir