provider "azurerm" {
    subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "bot-rg" {
    name     = var.rg_name
    location = var.location
}

#Linux App Service Plan 
resource "azurerm_app_service_plan" "bot-splan" {
    name = var.splan_name
    resource_group_name = azurerm_resource_group.bot-rg.name
    location = azurerm_resource_group.bot-rg.location
    kind = "linux"
    reserved = true
    per_site_scaling = false
    
    sku {
        size = "S1"
        tier = "Standard"
        capacity = "1"
    }
}

resource "azurerm_app_service" "bot-app" {
    name = var.app_name
    resource_group_name = azurerm_resource_group.bot-rg.name
    location = azurerm_resource_group.bot-rg.location
    enabled = true
    app_service_plan_id = azurerm_app_service_plan.bot-splan.id
    https_only = false
    site_config {
        dotnet_framework_version = "v4.0"
        linux_fx_version =  "PYTHON|3.7"
        scm_type = "None"
        cors {
            allowed_origins = [
                "https://botservice.hosting.portal.azure.net",
                "https://hosting.onecloud.azure-test.net/"
            ]
        }
        app_command_line = "gunicorn --bind 0.0.0.0 --worker-class aiohttp.worker.GunicornWebWorker --timeout 600 app:app"
    }
    app_settings = {
       "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    }
}