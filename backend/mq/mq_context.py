import aio_pika

from config.mq import mq_settings


class MQContext:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def __aenter__(self):
        try:
            self.connection = await aio_pika.connect_robust(mq_settings.url, timeout=30)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)
            return self
        except Exception as e:
            raise RuntimeError(f"Failed to connect to RabbitMQ: {str(e)}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            try:
                await self.connection.close()
            except Exception as e:
                print(f"Error closing RabbitMQ connection: {str(e)}")

    async def publish_result(self, task_id: str, status: str, result: dict):
        """Публикация результата в очередь результатов"""
        if not self.channel:
            raise RuntimeError("MQContext is not connected")

        result_queue = await self.channel.declare_queue(
            "image_task_result", durable=True
        )
        message = {"task_id": task_id, "status": status, "result": result}
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=str(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=result_queue.name,
        )
