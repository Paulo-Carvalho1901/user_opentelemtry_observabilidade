from locust import HttpUser, task, between
import random
import string


def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


class PessoaLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_pessoa(self):
        fake_name = random_string()
        json_body = {
            "nome": fake_name.capitalize(),
            "email": f"{fake_name}@teste.com",
            "senha": random_string(10),
            "cidade": "São Paulo"
        }

        with self.client.post("/pessoas/", json=json_body, catch_response=True) as res:
            if res.status_code not in (200, 201):
                res.failure(f"Erro: {res.status_code} - {res.text}")


# locust -f locustfile.py --host http://localhost:8000
