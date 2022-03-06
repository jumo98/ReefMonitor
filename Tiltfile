allow_k8s_contexts('reef-testsystem')
docker_build('motzi/reefmonitor', '.')
k8s_yaml('deployment/reefmonitor.yaml')
# k8s_resource('reefmonitor-python', port_forwards=8000)