# TestOps Task

## System Architecture
1. **Selenium Hub (Test Controller Pod)**:

   Acts as the main orchestrator and controller of test execution. It receives test requests, manages browser nodes, and distributes test tasks to the Chrome Node Pods.
2. **Chrome Node Pods**:
   These pods run instances of the Chrome browser to execute tests. Each Chrome Node Pod is registered with the Selenium Hub and can receive test commands as directed.

## How It Works
   **Test Initialization**: Test cases (e.g., Selenium scripts) are collected and prepared for execution.

   **Selenium Hub as Controller**: The Selenium Hub functions as the Test Controller Pod, managing and assigning test tasks to available Chrome Node Pods within the Kubernetes cluster. The Test Controller Pod (Selenium Hub) keeps track of the available browser nodes and distributes test requests accordingly.

   **Test Execution by Chrome Node**s**: Upon receiving test tasks from the Selenium Hub, each Chrome Node Pod executes the test cases in an instance of the Chrome browser. The Hub facilitates communication between the test scripts and the browser nodes, enabling seamless test execution.

   **Result Collection**: After execution, the results are returned to the Test Controller (Selenium Hub) for logging, monitoring, and reporting purposes.