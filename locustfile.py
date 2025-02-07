from locust import HttpUser, TaskSet, task, between

class APITasks(TaskSet):
    @task(2)
    def list_pipelines(self):
        # Предполагается, что API для пайплайнов доступно по /api/pipelines/
        self.client.get("/api/pipelines/")

    @task(1)
    def trigger_build(self):
        # Пример POST запроса для запуска сборки
        self.client.post("/api/trigger-build", json={"jobName": "TestJob"})

class WebsiteUser(HttpUser):
    tasks = [APITasks]
    wait_time = between(1, 5) 