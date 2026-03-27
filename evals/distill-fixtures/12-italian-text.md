# Guida alla Configurazione del Sistema di Monitoraggio

## Introduzione

È importante notare che il nostro sistema di monitoraggio utilizza Prometheus e Grafana per raccogliere e visualizzare le metriche dell'applicazione. Inoltre, vale la pena menzionare che il sistema è stato progettato per essere altamente scalabile e robusto.

## Configurazione di Prometheus

Per quanto riguarda Prometheus, la configurazione si trova in `/etc/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

Va sottolineato che l'intervallo di scraping è impostato a 15 secondi. Questo valore rappresenta un buon compromesso tra granularità dei dati e utilizzo delle risorse.

## Alert

A questo punto nel tempo, gli alert configurati sono:

1. **CPU > 80%** per 5 minuti → notifica Slack `#ops-alerts`
2. **Memoria > 90%** per 2 minuti → notifica PagerDuty
3. **Error rate > 1%** per 1 minuto → notifica Slack + PagerDuty
4. **Disk > 85%** → notifica Slack `#ops-alerts`

## Dashboard

In sostanza, le dashboard Grafana sono versionizzate in `infra/grafana/dashboards/`. Attualmente abbiamo 4 dashboard:
- Application Overview (ID: 1001)
- Database Performance (ID: 1002)
- Infrastructure Health (ID: 1003)
- Business Metrics (ID: 1004)

## Conclusione

In conclusione, il sistema di monitoraggio con Prometheus e Grafana fornisce visibilità completa sullo stato dell'applicazione. Per riassumere, la configurazione include scraping a 15s, 4 regole di alert, e 4 dashboard. Nel complesso, è un setup solido e affidabile.
