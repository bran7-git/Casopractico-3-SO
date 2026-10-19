from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'pedido-eventos',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='analytics-group',
    api_version=(2, 5, 0),  # <--- Forzamos la versión aquí también
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(" [*] Analytics Service (Kafka) escuchando eventos...")

for message in consumer:
    evento = message.value
    print(f" [Analytics] Registrando métrica: Pedido {evento['order_id']} -> {evento['status']}")