from kubernetes import client, config, utils
from kubernetes.client.exceptions import ApiException
import time
import yaml
import json
import pytest

# Load kubeconfig
config.load_kube_config()

# Kubernetes API clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

def apply_yaml(file_path):
    """Applies a YAML configuration file."""
    try:
        with open(file_path) as f:
            result = utils.create_from_yaml(v1.api_client, file_path, namespace="default")
            deployment_name = result[0][0].metadata.name
            print(f"Applied YAML configuration from {file_path}.")
            return deployment_name
    except utils.FailToCreateError as e:
        status = json.loads(e.api_exceptions[0].body)
        if status['reason'] == "AlreadyExists":
            print(f"{file_path} arleady deployed")
            return status['details']['name']
    except ApiException as e:
        print(f"Error applying YAML: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def check_pod_ready(pod_name, retries=10, delay=5):
    """Checks if the specified pod is ready."""
    for attempt in range(retries):
        try:
            pod = v1.read_namespaced_pod(name=pod_name, namespace="default")
            if pod.status.phase == "Running" and all(c.ready for c in pod.status.container_statuses):
                print(f"Pod {pod_name} is ready.")
                return True
            else:
                print(f"Waiting for pod {pod_name} to be ready... (Attempt {attempt+1}/{retries})")
        except ApiException as e:
            print(f"Error checking pod status: {e}")
        time.sleep(delay)
    print(f"Pod {pod_name} is not ready after {retries} attempts.")
    return False

def check_deployment_ready(deployment_name, retries=10, delay=5):
    """Checks if the specified deployment is ready."""
    for attempt in range(retries):
        try:
            deployment = apps_v1.read_namespaced_deployment_status(deployment_name, namespace="default")
            ready_replicas = deployment.status.ready_replicas or 0
            desired_replicas = deployment.spec.replicas

            if ready_replicas == desired_replicas:
                print(f"Deployment {deployment_name} is ready.")
                return True
            else:
                print(f"Waiting for deployment {deployment_name} to be ready... "
                      f"({ready_replicas}/{desired_replicas} replicas ready) (Attempt {attempt+1}/{retries})")
        except ApiException as e:
            print(f"Error checking deployment status: {e}")
        time.sleep(delay)
    print(f"Deployment {deployment_name} is not ready after {retries} attempts.")
    return False

def deploy_chrome_nodes(node_count, chrome_node_yaml_path):
    """Deploys Chrome Node Pods from a YAML file based on node count."""

    # TODO implement node_count
    deployment_name = apply_yaml(chrome_node_yaml_path)
    return check_deployment_ready(deployment_name)

def deploy_test_controller(test_controller_yaml_path):
    """Deploys the Test Controller Pod from a YAML file."""
    deployment_name = apply_yaml(test_controller_yaml_path)
    return check_deployment_ready(deployment_name)

def deploy_svc_controller(svc_controller_yaml_path):
    """Deploys the Test Controller Pod from a YAML file."""
    apply_yaml(svc_controller_yaml_path)
    return True

def run_pytest():
    """Run pytest on the test directory."""
    result = pytest.main(["-n", "2", "tests"])
    return result

if __name__ == "__main__":
    node_count = 2
    chrome_node_yaml_path = "./k8s/selenium-node-chrome-deployment.yaml"
    test_controller_yaml_path = "./k8s/selenium-hub-deployment.yaml"
    svc_controller_yaml_path = "./k8s/selenium-hub-svc.yaml"
    
    deploy_test_controller(test_controller_yaml_path)
    deploy_chrome_nodes(node_count, chrome_node_yaml_path)
    deploy_svc_controller(svc_controller_yaml_path)

    result = run_pytest()
    if result == 0:
        print("Tests passed successfully!")
    else:
        print(f"Tests failed with exit code {result}")