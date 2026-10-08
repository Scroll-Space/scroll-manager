# :latest version (9.4.0) isn’t working.
FROM onlyoffice/documentserver:9.3.0

# Copying the plugin files inside the image
# {UUID} from config.json
COPY . /var/www/onlyoffice/documentserver/sdkjs-plugins/{ca39b178-83ef-4074-b248-108d0634a4db}/

COPY . /app_copy