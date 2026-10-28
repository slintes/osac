from pathlib import Path

import yaml


def test_root_disk_uses_node_registry_pull_without_changing_blank_disks():
    tasks = yaml.safe_load(
        (
            Path(__file__).resolve().parents[2]
            / "collections/ansible_collections/osac/templates/roles/ocp_virt_vm/tasks/create_resources.yaml"
        ).read_text()
    )
    root = next(t for t in tasks if t["name"] == "Create DataVolume for VM root disk")
    root_module = root["kubernetes.core.k8s"]
    assert root_module["definition"]["spec"]["source"]["registry"] == {
        "url": "docker://{{ vm_image_source }}",
        "pullMethod": "node",
    }
    assert root_module.get("apply", False) is False
    assert root_module["definition"]["metadata"]["namespace"] == "{{ compute_instance_target_namespace }}"
    assert root_module["definition"]["metadata"]["labels"] == "{{ default_vm_labels }}"
    additional = next(t for t in tasks if t["name"] == "Create DataVolumes for additional disks")
    assert additional["kubernetes.core.k8s"]["definition"]["spec"]["source"] == {"blank": {}}
