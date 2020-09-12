# Ansible MC Hub

This project is meant to provision, configure and deploy [MC Hub](https://github.com/ComputeCanada/mc-hub) on the cloud with minimal manual intervention. This is done through an Ansible playbook. The playbook sets up the MC Hub Docker container, configures a SAML service provider to enable single sign-on authentication and generates a _Let's Encrypt_ HTTPS certificate.

To deploy Ansible MC Hub on your own, read the [documentation](./docs/README.md).
