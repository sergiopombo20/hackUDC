from denodo_wrapper import DenodoAPI

api = DenodoAPI(base_url="http://localhost:9992", username="admin", password="admin")
print(api.health_check())