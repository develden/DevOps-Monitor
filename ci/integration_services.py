import requests
import logging
import redis

# Инициализация Redis-клиента (настройте согласно вашим параметрам)
cache = redis.Redis(host='localhost', port=6379, db=0)

logger = logging.getLogger(__name__)

class JenkinsService:
    def __init__(self, api_endpoint, auth_token):
        self.api_endpoint = api_endpoint
        self.auth_token = auth_token

    def get_build_status(self, job_name, build_number):
        cache_key = f"jenkins:{job_name}:{build_number}"
        cached_status = cache.get(cache_key)
        if cached_status:
            return cached_status.decode('utf-8')
        url = f"{self.api_endpoint}/job/{job_name}/{build_number}/api/json"
        headers = {'Authorization': f"Bearer {self.auth_token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            status = data.get("result", "unknown")
            cache.setex(cache_key, 60, status)  # кэшируем на 60 секунд
            return status
        except requests.RequestException as e:
            logger.error(f"Error fetching Jenkins build status: {e}")
            return "error"

    def trigger_build(self, job_name):
        url = f"{self.api_endpoint}/job/{job_name}/build"
        headers = {'Authorization': f"Bearer {self.auth_token}"}
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.status_code == 201
        except requests.RequestException as e:
            logger.error(f"Error triggering Jenkins build: {e}")
            return False

class GithubActionsService:
    def __init__(self, api_endpoint, auth_token):
        self.api_endpoint = api_endpoint
        self.auth_token = auth_token

    def get_workflow_status(self, repo, workflow_id):
        url = f"{self.api_endpoint}/repos/{repo}/actions/runs"
        headers = {'Authorization': f"token {self.auth_token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data  # обработка статусов может быть расширена
        except requests.RequestException as e:
            logger.error(f"Error fetching GitHub Actions workflow status: {e}")
            return None

    def trigger_workflow_dispatch(self, repo, workflow_id, ref='main'):
        url = f"{self.api_endpoint}/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
        headers = {'Authorization': f"token {self.auth_token}"}
        payload = {"ref": ref}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.status_code == 204
        except requests.RequestException as e:
            logger.error(f"Error triggering GitHub Actions workflow: {e}")
            return False

class GitLabCIService:
    def __init__(self, api_endpoint, auth_token):
        self.api_endpoint = api_endpoint
        self.auth_token = auth_token

    def get_pipeline_status(self, project_id, pipeline_id):
        url = f"{self.api_endpoint}/projects/{project_id}/pipelines/{pipeline_id}"
        headers = {'PRIVATE-TOKEN': self.auth_token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("status", "unknown")
        except requests.RequestException as e:
            logger.error(f"Error fetching GitLab CI pipeline status: {e}")
            return "error"

    def trigger_pipeline(self, project_id, ref):
        url = f"{self.api_endpoint}/projects/{project_id}/trigger/pipeline"
        payload = {"ref": ref, "token": self.auth_token}
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            return response.status_code == 201
        except requests.RequestException as e:
            logger.error(f"Error triggering GitLab pipeline: {e}")
            return False 