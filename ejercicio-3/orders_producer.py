from fastapi import FastAPI
from kafka import KafkaProducer
import json

app = FastAPI(title="Orders Service - Kafka Event Streaming")

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    api_version=(2, 5, 0),  # <--- Forzamos la versión
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'pedido-eventos'

@app.post("/orders/status")
def update_order_status(order_id: str, status: str, customer_email: str):
    evento = {
        "order_id": order_id,
        "status": status,
        "customer_email": customer_email
    }
    producer.send(TOPIC_NAME, value=evento)
    producer.flush()
    
    return {
        "status": "SUCCESS",
        "message": f"Evento '{status}' publicado en el topic de Kafka.",
        "evento": evento
    }