import pika
import json
import time

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f" [x] Mensaje recibido de la cola...")
    print(f" 📧 Enviando correo a: {order['customer_email']} por el producto: {order['product_name']}")
    
    # Simulamos que el envío del correo tarda unos segundos
    time.sleep(2)
    print(f" [✔] Correo enviado con éxito a {order['customer_email']}\n")
    
    # Confirma a RabbitMQ que el mensaje fue procesado correctamente (Ack)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='orders_queue', durable=True)
    
    # Configurar para que procese de a un mensaje a la vez de forma justa
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='orders_queue', on_message_callback=callback)

    print(" [*] Notification Service esperando mensajes. Para salir presiona CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    main()