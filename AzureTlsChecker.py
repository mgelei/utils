import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.apimanagement import ApiManagementClient

azure_cred = DefaultAzureCredential()
subscription_guid = os.getenv("AZURE_SUBSCRIPTION_ID") # don't forget to set this
bad_tls = ['1.0', '1.1']

# check App Services TLS settings
def check_app_services_tls():
    client = WebSiteManagementClient(azure_cred, subscription_guid)
    apps = client.web_apps.list()
    for app in apps:
        config = client.web_apps.get_configuration(app.resource_group, app.name)
        if config.min_tls_version in bad_tls:
            print(f"App Service {app.name} in RG {app.resource_group} is using deprecated TLS version: {config.min_tls_version}")

# check Azure SQL Server TLS settings
def check_sql_servers_tls():
    client = SqlManagementClient(azure_cred, subscription_guid)
    servers = client.servers.list()
    for server in servers:
        # By default, Azure SQL enforces TLS 1.2, but check if there are any old configurations
        if server.minimal_tls_version in bad_tls:
            print(f"SQL Server {server.name} in RG {server.resource_group_name} is using deprecated TLS version: {server.minimal_tls_version}")

# check Storage Account TLS settings
def check_storage_account_tls():
    client = StorageManagementClient(azure_cred, subscription_guid)
    accounts = client.storage_accounts.list()
    for account in accounts:
        if account.minimum_tls_version in ['TLS1_0', 'TLS1_1']:
            print(f"Storage Account {account.id} is using deprecated TLS version: {account.minimum_tls_version}")

# check API Management TLS settings
def check_api_management_tls():
    client = ApiManagementClient(azure_cred, subscription_guid)
    services = client.api_management_service.list()
    for service in services:
        if service.tls_client_profile and service.tls_client_profile.min_tls_version in bad_tls:
            print(f"API Management Service {service.name} in RG {service.resource_group_name} is using deprecated TLS version: {service.tls_client_profile.min_tls_version}")

if __name__ == "__main__":
    print("Checking App Services for TLS 1.0/1.1 usage...")
    check_app_services_tls()
    print("\nChecking SQL Servers for TLS 1.0/1.1 usage...")
    check_sql_servers_tls()
    print("\nChecking Storage Accounts for TLS 1.0/1.1 usage...")
    check_storage_account_tls()
    print("\nChecking API Management Services for TLS 1.0/1.1 usage...")
    check_api_management_tls()

    print("\nCompleted TLS configuration check.")
