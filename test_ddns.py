import unittest
from unittest.mock import patch, MagicMock
import ddns

class TestDDNS(unittest.TestCase):

    @patch('ddns.requests.get')
    def test_get_current_ip_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "203.0.113.195"}
        mock_get.return_value = mock_response

        ip = ddns.get_current_ip()
        self.assertEqual(ip, "203.0.113.195")

    def test_load_domains(self):
        # Creamos un archivo temporal para probar la carga de dominios
        test_file = "test_domains.list"
        with open(test_file, "w") as f:
            f.write("# Comentario\nsub1.example.com\n\nsub2.example.com\n")
        
        domains = ddns.load_domains(test_file)
        self.assertEqual(domains, ["sub1.example.com", "sub2.example.com"])
        
        import os
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
