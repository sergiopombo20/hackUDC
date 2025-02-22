import requests
from requests.auth import HTTPBasicAuth

class DenodoAPI:
    """Wrapper for Denodo AI SDK API (Synchronous version)"""

    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize the API client.

        :param base_url: The base URL of the Denodo API (e.g., "http://localhost:8008")
        :param username: API username for Basic Auth
        :param password: API password for Basic Auth
        """
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        self.auth = HTTPBasicAuth(username, password)

    def _request(self, method: str, endpoint: str, params=None, json_data=None):
        """
        Internal method to make HTTP requests (synchronous).

        :param method: HTTP method (GET, POST, etc.)
        :param endpoint: API endpoint (e.g., "/answerQuestion")
        :param params: URL query parameters (for GET requests)
        :param json_data: JSON payload (for POST requests)
        :return: JSON response or raises an exception on failure
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method, url, params=params, json=json_data, auth=self.auth
            )

            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

            # Si la respuesta está vacía, devolver un mensaje de estado en lugar de intentar parsear JSON
            if not response.text.strip():
                return {"status": "healthy", "message": "Service is running"}

            return response.json()

        except requests.exceptions.JSONDecodeError:
            raise Exception(f"API did not return JSON. Response content: {response.text[:200]}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {e}")

    def health_check(self):
        """
        Calls the health check API.

        :return: API response as a dictionary.
        """
        return self._request("GET", "/health")

    def answer_question(self, question: str):
        """
        Calls the answerQuestion API.

        :param question: The natural language question to query.
        :return: API response as a dictionary.
        """
        payload = {
            "question": question,
        }
        return self._request("POST", "/answerQuestion", json_data=payload)
