from fastapi import FastAPI, Body
import pika
import json

app = FastAPI(title="Orders Service (Async)")

def publish_order_created(order_data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='orders_queue', durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key='orders_queue',
        body=json.dumps(order_data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()

@app.post("/orders")
def create_order(customer_email: str, product_name: str):
    order = {
        "customer_email": customer_email,
        "product_name": product_name,
        "status": "CREATED"
    }
    
    publish_order_created(order)
    
    return {
        "status": "SUCCESS",
        "message": "Pedido recibido y en proceso. Notificación en cola.",
        "order": order
    }