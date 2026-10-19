from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'pedido-eventos',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='notification-group',
    api_version=(2, 5, 0),  # <--- Forzamos la versión para evitar el bug de Python 3.13
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(" [*] Notification Service (Kafka) escuchando eventos...")

for message in consumer:
    evento = message.value
    print(f" [Notification] Pedido {evento['order_id']} cambió a estado: {evento['status']}")
    if evento['status'] == 'CONFIRMED':
        print(f"   📧 Enviando email de confirmación a {evento['customer_email']}")
    elif evento['status'] == 'SHIPPED':
        print(f"   📦 Enviando email de 'Tu pedido va en camino' a {evento['customer_email']}")