from locust import HttpUser, task, between

class MyUser(HttpUser):
    host = "http://web:80"

    urls = [
        "https://luccabarroso.com.br/",
        "https://luccabarroso.com.br/pt/animations",
        "https://www.fontshare.com/",
        "https://www.unifor.br/",
        "https://www.apple.com/br/",
        "https://www.baratocoletivo.com.br/",
        "https://www.bbc.com/portuguese",
        "https://www.cnnbrasil.com.br/",
        "https://www.youtube.com/",
        "https://hemocentrosunidos.org.br/"
    ]

    @task
    def my_task(self):
        for url in self.urls:
            self.client.get(f"/?url={url}")
