from celery_app import celery_app
import time
import asyncio

@celery_app.task(name="say_hello")
def say_hello(name:str, delay_seconds: int = 5):
    print(f"starting the task for {name}, {delay_seconds} sec...")
    time.sleep(delay_seconds)
    result = f"привет, {name}"
    print (result)
    return result
@celery_app.task(name="process_data", bind=True)
def process_data(self, items_count: int):
    total = items_count
    for i in range (total):
        time.sleep(0.5)
        progress = int((i+1)/ total * 100)
        self.update_state(
            state="PROGRESS",
            meta={"current": i + 1, "total": total, "progress": progress}
        )
    return {"status": "Ready!", "processed": total}

@celery_app.task(name= "send_email")
def send_email(to_email: str, subject: str, body: str):
    print(f"sending to {to_email}")
    print(f"Theme: {subject}")
    print(f"Text: {body}")
    time.sleep(2)  
    print(f"the letter is sent {to_email}")
    return {"status": "email_sent", "to": to_email}

@celery_app.task(name="async_http_call")
def async_http_call(url: str):
    import requests
    try:
        response = requests.get(url, timeout=10)
        return {"status": "success", "url": url, "status_code": response.status_code}
    except Exception as e:
        return {"status": "error", "url": url, "error": str(e)}

