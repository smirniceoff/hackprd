import requests
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.azure.metrics_exporter import new_metrics_exporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
import logging

# Connection String do Application Insights
connection_string = "InstrumentationKey=b17faf91-c686-4c08-8dc1-753123f1c72b"

# Configurações de telemetria
tracer = Tracer(
    exporter=AzureExporter(connection_string=connection_string),
    sampler=ProbabilitySampler(1.0)
)

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=connection_string))
logger.setLevel(logging.INFO)

metrics_exporter = new_metrics_exporter(connection_string=connection_string)

# URLs para testar
urls = [
    "https://www.caixa.gov.br/",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/status/502"
]

# Loop para acessar URLs e registrar telemetria
for url in urls:
    print(f"\n🔄 Acessando: {url}")
    with tracer.span(name=f"Requisicao para {url}") as span:
        try:
            response = requests.get(url, verify=False)
            status = response.status_code

            # Adiciona atributos ao span
            span.add_attribute("http.status_code", status)
            span.add_attribute("http.url", url)

            # Envia log
            logger.info(f"URL: {url} retornou status {status}")

            # Envia métrica personalizada
            metrics_exporter.export_metrics([
                {
                    'name': 'StatusHTTP',
                    'value': status,
                    'properties': {
                        'url': url,
                        'status': str(status)
                    }
                }
            ])

            # Saída no terminal
            print(f"✅ Requisição bem-sucedida. Status: {status}")
            print("📊 Métrica enviada para Application Insights.")
            print("📝 Log registrado com sucesso.")

        except Exception as e:
            span.add_attribute("error", str(e))
            logger.error(f"Erro ao acessar {url}: {str(e)}")
            print(f"❌ Erro ao acessar {url}: {str(e)}")
