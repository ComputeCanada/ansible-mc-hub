# Ansible Magic Castle UI

This project is meant to provision, configure and deploy [Magic Castle UI](https://github.com/ComputeCanada/magic_castle-ui) on the cloud with minimal manual intervention. This is done through an Ansible playbook. The playbook sets up the Magic Castle UI Docker container, configures a SAML service provider to enable single sign-on authentication and generates a _Let's Encrypt_ HTTPS certificate.

## Controller requirements

* [Ansible >= 2.9.11](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

## Cloud requirements

* 1 keypair
* 1 CentOS 7 instance
* 1 static public IP
* Write access to the DNS records of a domain to host the server

## Cloud configuration

These steps assume you are using OpenStack as your cloud service provider but the configuration will be similar on public clouds.

1. Create a keypair (you can use an existing public key).

2. Create a security group with the following inbound rules. For port 22 (SSH) access, you can choose which IP address range you want to allow.

    | Port        | CIDR      |
    |-------------|-----------|
    | 22 (SSH)    |  depends  |
    | 80 (HTTP)   | 0.0.0.0/0 |
    | 443 (HTTPS) | 0.0.0.0/0 |

3. Create a CentOS 7 instance configured with the keypair and the security group created previously. It is also recommended to create a 30 GB volume which can be recovered if your instance fails.

4. Launch the instance.

5. Associate a floating IP to the instance.

6. Create an `A` DNS record pointing to the floating IP. For instance, you can create a record for `mc.computecanada.dev` pointing to the previously created floating IP. This is required to generate an HTTPS certificate.

## Magic Castle UI configuration

1. Clone this repository.
    ````
    git clone https://github.com/ComputeCanada/ansible-mcui
    ````

2. In order to use Google Cloud as a DNS provider, do the following steps.

    1. Create a service account that has permissions to manage the DNS settings (if you don't already have one). The account should have the _DNS Administrator_ role.
    2. Create a new key for this account and download it, in JSON format.
    3. Copy the JSON key file to the root of the repository in a file named `gcloud-key.json`.
        ```
        cp <JSON key file location> gcloud-key.json
        ```

3. Download or create a `clouds.yaml` file with your OpenStack cloud credentials. The cloud entry you want to use needs to be named `openstack`. It will be used to allocate the resources for the clusters. Copy the `clouds.yaml` file to the root of the repository.
   ```
   cp <clouds.yaml location> .
   ```

4. If you have already created a SAML service provider on a different server but with the same FQDN, you can use the same certificates and keys. If this is a new setup, skip this step.

    Simply copy the `.pem` files from the `/etc/shibboleth` directory of the server into `files/etc/shibboleth` in the current directory. You should now have the following files added in this directory:

    ````
    sp-encrypt-cert.pem
    sp-encrypt-key.pem
    sp-signing-cert.pem
    sp-signing-key.pem
    ````

5. Create a `configuration.json` file in the current directory according to [Magic Castle UI configuration documentation](https://github.com/ComputeCanada/magic_castle-ui/blob/master/docs/configuration.md). Make sure to set `auth_type` to `"SAML"`.

6. Create a `hosts.yml` file with the proper configuration.

    ````yaml
    all:
      hosts:
        mc.computecanada.dev:
          ansible_user: centos
          fqdn: mc.computecanada.dev
          saml_identity_provider_metadata_url: https://idp.computecanada.ca/idp/shibboleth
          saml_identity_provider_entity_id: https://idp.computecanada.ca/idp/shibboleth
          saml_service_provider_entity_id: mc.computecanada.dev
          server_admin_email: admin@example.com
          magic_castle_ui_version: "v5.0.2"
    ````

    `mc.computecanada.dev`: Should correspond to the public IP or FQDN of the instance. This will be used by Ansible to connect to your instance.

    `anisble_user`: The username used by Ansible to connect via SSH to your instance.

    `saml_identity_provider_metadata_url`: The metadata URL of your identity provider. This URL should correspond to a SAML file.

    `saml_identity_provider_entity_id`: The entity ID of your identity provider. This can be found in the metadata SAML file of the identity provider.

    `saml_service_provider_entity_id`: Your already existing SAML service provider entity ID, or a new one. It needs to be unique. We recommend using the FQDN as the entity ID.

    `server_admin_email`: This email will be notified by _Let's Encrypt_ for important messages related to the HTTPS certificate. It is also displayed as the support contact in some SAML and Apache error messages.

    `magic_castle_ui_version`: The version tag of the [Magic Castle UI](https://github.com/ComputeCanada/magic_castle-ui) Docker image.


## Running the playbook

1. Start an SSH agent and add the private key of the host CentOS instance.

    ````bash
    eval `ssh-agent`
    ssh-add <SSH_PRIVATE_KEY_FILE>
    ````

2. Run the Ansible playbook.

    ````bash
    ansible-playbook -i hosts.yml site.yml
    ````

3. If you created a new SAML service provider, you need to register it with your identity provider. Simply send to the identity provider manager your metadata URL: `http://mc.computecanada.dev/Shibboleth.sso/Metadata` (where `mc.computecanada.dev` corresponds to your FQDN).

4. Once your service provider is registered, you can navigate to the URL of Magic Castle UI and start building clusters.

> If you ever need to make changes to a configuration file, make the modification and run the Ansible playbook again.
