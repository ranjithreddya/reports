ChatGPT said:
Here’s the complete Python consumer script that does exactly what you asked:

Listens to a Redis queue (webhook_queue)

Pops one webhook message at a time

Processes each file in that message in parallel (using threads)

Waits for all file processing to complete before popping the next message

✅ Full Python Consumer Script
python
Copy
Edit
import redis
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = 'webhook_queue'

# Simulated file processing function
def process_file(file_name):
    print(f"🔧 Processing file: {file_name}")
    time.sleep(0.5)  # Simulate work (I/O or API call)
    print(f"✅ Finished: {file_name}")
    return file_name

# Process one webhook message: all files in parallel
def process_webhook_message(message):
    data = json.loads(message)
    files = data.get("files", [])
    webhook_id = data.get("id", "unknown")

    print(f"📦 Webhook ID: {webhook_id}, {len(files)} files to process")

    # Run file processing in parallel threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_file, f) for f in files]

        # Wait for all files to finish
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(f"❌ Error processing file: {e}")

    print(f"✅ All files processed for webhook {webhook_id}\n")

# Main loop to consume messages
print("🟢 Consumer started. Waiting for webhook messages...\n")

while True:
    try:
        queue_name, message = r.brpop(QUEUE_NAME)
        print(f"\n📥 New webhook message received from {queue_name.decode()}")
        process_webhook_message(message)
    except Exception as e:
        print(f"❌ Error in consumer loop: {e}")
        time.sleep(2)
🧪 Example Webhook Payload (Producer Side)
Push this into Redis to test:

python
Copy
Edit
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

webhook_payload = {
    "id": "webhook-001",
    "files": [f"file_{i}.txt" for i in range(1, 101)]
}

r.lpush("webhook_queue", json.dumps(webhook_payload))
✅ Notes
max_workers=10: Change this to control concurrency per message.

You can simulate file downloads, uploads, API calls, etc. inside process_file().

The message structure can be adapted — just ensure it includes the file list.

Would you like me to package this into a Dockerfile, a systemd service, or generate a test load script with 10+ webhook messages?
#######################

✅ Requirements
Install redis (>=4.2):

bash
Copy
Edit
pip install redis>=4.5
✅ Full Code: async_webhook_consumer.py
python
Copy
Edit
import asyncio
import json
import redis.asyncio as redis

QUEUE_NAME = 'webhook_queue'

# ✅ Simulate file processing (replace with real logic)
async def process_file(file_name):
    print(f"🔧 Processing file: {file_name}")
    await asyncio.sleep(0.5)  # Simulate async work (e.g., I/O, HTTP, DB)
    print(f"✅ Finished: {file_name}")
    return file_name

# ✅ Process one webhook message (all files concurrently)
async def process_webhook_message(message):
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print("❌ Invalid JSON message")
        return

    files = data.get("files", [])
    webhook_id = data.get("id", "unknown")

    print(f"\n📦 Webhook ID: {webhook_id} | {len(files)} files to process")

    # Create file-processing tasks
    tasks = [process_file(f) for f in files]
    
    # Run all file tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle errors gracefully
    for res in results:
        if isinstance(res, Exception):
            print(f"❌ Error during file processing: {res}")

    print(f"✅ All files processed for webhook {webhook_id}\n")

# ✅ Main consumer loop
async def consumer_loop():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    print("🟢 Async Consumer started. Waiting for webhook messages...\n")

    while True:
        try:
            result = await r.brpop(QUEUE_NAME)
            if result:
                _, message = result
                await process_webhook_message(message)
        except Exception as e:
            print(f"❌ Error in consumer loop: {e}")
            await asyncio.sleep(2)

# ✅ Entry point
if __name__ == "__main__":
    asyncio.run(consumer_loop())
🧪 Optional: Test Producer Script
To push test data into Redis:

python
Copy
Edit
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

payload = {
    "id": "webhook-001",
    "files": [f"file_{i}.txt" for i in range(1, 101)]  # 100 files
}

r.lpush("webhook_queue", json.dumps(payload))
✅ Features Included
Async Redis consumer (brpop)

Concurrent file processing (asyncio.gather)

Error handling for bad files

Sequential message consumption

Clean output/logging

Would you like a Docker setup or service wrapper (systemd, PM2, etc.) to run this as a background worker?




