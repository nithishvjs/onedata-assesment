Simulated Incident & RCA Report

Incident Summary: 

Symptom: The new application service (my-app-service) deployed to the local Kind Kubernetes cluster is inaccessible and unresponsive when attempting to connect via the standard localhost:NodePort URL.

Impact: Complete service unavailability for all local development and testing.

The Investigation Timeline:

10:00 AM: Deployment completed; service failed health check.

10:05 AM: Logs Captured: Confirmed the service Pods were Running and logs showed the application started correctly on port 8000. This ruled out an application code bug.

10:10 AM: Issue Reproduced: Tested connection from inside the Kind cluster (using a temporary kubectl exec Pod) and verified the application was reachable. The failure was confirmed to be related to external access only.

Root Cause Analysis (RCA):

Problem: The Kubernetes NodePort service was correctly exposing the application on the cluster's internal network node (the Kind container), but this internal port was not being forwarded to the host machine's external network.

Root Cause: The cluster runs inside a Docker container (Kind), creating a network isolation barrier. The NodePort mapping was functional internally but not externally published to the host machine, requiring a manual tunneling step.

Solution:

Ran the kubectl port-forward command to tunnel the service port to the host machine's localhost:

kubectl port-forward svc/my-app-service 8000:8000
Result: Service was immediately accessible via http://localhost:8000.

Preventative Action:
To prevent this confusion and manual step in the future:

Standardize Documentation: Update the service deployment Readme/docs to explicitly state that the kubectl port-forward command is mandatory for local access due to the use of the Kind cluster containerization.
