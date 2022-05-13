RG="test"
LOCATION="eastus"
WEBAPP="sefrks"
KEYVAULT="lfkdjlf"
SQLDB="lekrjk"
SQLPASSWORD="sddjf213EFS"

az group create -n "$RG" -l "$LOCATION"

# az webapp up -g "$RG" -n "$WEBAPP" --runtime "PYTHON:3.9" --sku B1 -l "$LOCATION"
az appservice plan create -g "$RG" -n "$WEBAPP" --is-linux --sku B1 -l "$LOCATION"
az webapp create -g "$RG" -n "$WEBAPP" -p "$WEBAPP" -i "serviceconnector.azurecr.io/python-sql-sample"

az keyvault create -g "$RG" -n "$KEYVAULT" --no-self-perms -l "$LOCATION"

az sql server create -g "$RG" -n "$SQLDB" -u "$SQLDB" -p "$SQLPASSWORD" -l "$LOCATION"
sleep 5
az sql db create -g "$RG" -n "$SQLDB" -s "$SQLDB"

KEYVAULT_ID=$(az keyvault show -g "$RG" -n "$KEYVAULT" --query "id" -o tsv)
az webapp connection create sql -g "$RG" -n "$WEBAPP" --tg "$RG" --server "$SQLDB" --database "$SQLDB" --secret name="$SQLDB" secret="$SQLPASSWORD" --client-type python --vault-id "$KEYVAULT_ID"

echo "Open Browser with https://$WEBAPP.azurewebsites.net/"
