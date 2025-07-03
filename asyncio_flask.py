import asyncio
import json
import aiofiles

# ✅ Simulate file processing with real async I/O
async def process_file(file_name):
    print(f"📂 Reading file: {file_name}")
    try:
        async with aiofiles.open(file_name, mode='r') as f:
            content = await f.read()
        print(f"✅ Finished: {file_name} ({len(content)} characters)")
        return file_name
    except Exception as e:
        print(f"❌ Error reading {file_name}: {e}")
        return e

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

    # Run file-processing tasks concurrently
    tasks = [process_file(f) for f in files]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle errors gracefully
    for res in results:
        if isinstance(res, Exception):
            print(f"❌ Error during file processing: {res}")

    print(f"✅ All files processed for webhook {webhook_id}\n")


# ✅ Simulate running the webhook handler
if __name__ == "__main__":
    test_message = json.dumps({
        "id": "abc123",
        "files": ["file1.txt", "file2.txt", "file3.txt"]
    })

    # Create dummy test files for demo
    async def create_test_files():
        for name in ["file1.txt", "file2.txt", "file3.txt"]:
            async with aiofiles.open(name, mode='w') as f:
                await f.write(f"Content of {name}\n")

    async def main():
        await create_test_files()
        await process_webhook_message(test_message)

    asyncio.run(main())
