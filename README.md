# echo-bot

Basic echo bot using Microsoft bot framework

## Prepare the development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-compile
pip-sync requirements.txt
```

## deploy to Azure 

```bash
az webapp deployment source config-zip --resource-group <resource group>  --name habot-app --src ./echo-bot.zip
```
