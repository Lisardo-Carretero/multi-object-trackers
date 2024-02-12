import cv2
from confluent_kafka import Producer
import time


def delivery_report(err, msg):
    if err is not None:
        print(f'Mensaje enviado fallido: {err}')
    else:
        print(f'Mensaje enviado: {msg}')


def produce_video_frames(video_path, topic, bootstrap_servers='localhost:9092'):
    # Configurar el productor de Kafka
    conf = {'bootstrap.servers': bootstrap_servers}
    producer = Producer(conf)

    # Leer el video
    cap = cv2.VideoCapture(video_path)

    # Capturar frames y enviarlos como mensajes a Kafka
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Codificar el frame como JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)

        # Enviar el frame como mensaje a Kafka
        producer.produce(topic, key=str(frame_count), value=img_encoded.tostring(), callback=delivery_report)
        frame_count += 1

        # Esperar un breve período de tiempo para simular transmisión en tiempo real
        time.sleep(0.03)  # Aproximadamente 30 fps

    # Cerrar el productor y liberar recursos
    producer.flush()
    producer.close()
    cap.release()


if __name__ == "__main__":
    video_path = 'video.mp4'  # Ruta del video
    kafka_topic = 'video_frames'  # Tema de Kafka
    kafka_bootstrap_servers = 'localhost:9092'  # Servidores de Kafka

    produce_video_frames(video_path, kafka_topic, kafka_bootstrap_servers)
