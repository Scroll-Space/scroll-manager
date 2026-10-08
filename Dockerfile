# :latest version (9.4.0) isn’t working.
FROM onlyoffice/documentserver:9.3.0

# Copying the plugin files inside the image
# {UUID} from config.json
COPY src/ /var/www/onlyoffice/documentserver/sdkjs-plugins/{CA39B178-83EF-4074-B248-108D0634A4DB}/

COPY src/ /app_copy/