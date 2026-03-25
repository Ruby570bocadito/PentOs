import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import validate_target, get_timestamp
from config import Config


class TestUtils:
    def test_validate_target_ip_valid(self):
        assert validate_target("192.168.1.1") is True
        assert validate_target("10.0.0.1") is True
        assert validate_target("127.0.0.1") is True
    
    def test_validate_target_ip_invalid(self):
        assert validate_target("999.999.999.999") is False
        assert validate_target("256.0.0.1") is False
    
    def test_validate_target_domain_valid(self):
        assert validate_target("example.com") is True
        assert validate_target("test.example.com") is True
        assert validate_target("sub.domain.org") is True
    
    def test_validate_target_empty(self):
        assert validate_target("") is False
        assert validate_target(None) is False
    
    def test_get_timestamp_format(self):
        ts = get_timestamp()
        assert isinstance(ts, str)
        assert len(ts) > 0


class TestConfig:
    def test_config_initialized(self):
        assert Config.VERBOSE is False
        assert hasattr(Config, 'NMAP_CONFIG')
        assert hasattr(Config, 'GOBUSTER_CONFIG')
    
    def test_output_dir_format(self):
        target = "192.168.1.1"
        output = Config.get_output_dir(target)
        assert target in output
        assert output.endswith("results/" + target) or output.endswith(target)


class TestCLI:
    def test_import_main(self):
        import pentops
        assert pentops.__version__ == "1.0.0"
    
    def test_modules_import(self):
        from modules import recon, enumeration, vulnscan, exploit, postexploit
        assert recon is not None
        assert enumeration is not None
        assert vulnscan is not None
        assert exploit is not None
        assert postexploit is not None
