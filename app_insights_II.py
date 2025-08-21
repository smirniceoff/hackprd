import requests
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Connection String do Application Insights
connection_string = "InstrumentationKey=24d4b622-db85-4c0e-a731-0676dc9078a6"

# Configurações
tracer = Tracer(
    exporter=AzureExporter(connection_string=connection_string),
    sampler=ProbabilitySampler(1.0)
)

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=connection_string))
logger.setLevel(logging.INFO)

# URLs para testar
urls = [
    "https://httpstat.us/200",
    "https://httpstat.us/404",
    "https://httpstat.us/500",
    "https://httpstat.us/502"
]

# Loop com rastreamento manual
for url in urls:
    with tracer.span(name=f"Requisicao para {url}") as span:
        try:
            response = requests.get(url)
            status = response.status_code
            span.add_attribute("http.status_code", status)
            span.add_attribute("http.url", url)
            logger.info(f"URL: {url} retornou status {status}")
        except Exception as e:
            span.add_attribute("error", str(e))
            logger.error(f"Erro ao acessar {url}: {str(e)}")
