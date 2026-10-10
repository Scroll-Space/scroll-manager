# :latest version (9.4.0) isn’t working.
FROM onlyoffice/documentserver:latest

# Copying the plugin files inside the image
# {UUID} from config.json
COPY src/ /var/www/onlyoffice/documentserver/sdkjs-plugins/{CA39B178-83EF-4074-B248-108D0634A4DB}/
