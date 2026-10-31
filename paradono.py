import asyncio
import aiohttp
import secrets, string

counter = 0


async def test_this(emails):
    async def fetch(session, email):
        global counter
        try:
            url = "https://100067.connect.garena.com/game/account_security/swap:send_otp"
            headers = {
                'Accept': 'application/json',
                #'Accept-Encoding': 'gzip',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': "GarenaMSDK/4.0.39(PMT3748_3G ;Android 10;ko;KR;)",
            }
            data = {
                'app_id': 100067,
                'email': email,
            }

            async with session.post(url=url, headers=headers, data=data, timeout=2) as response:
                text = await response.text()
                print(f"{email} - {text}")
                if "error_no_binding_found" in text:
                    counter += 1
        except Exception as e:
            print(e)


    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, email) for email in emails]
        return await asyncio.gather(*tasks)

"""start the runtime"""
async def runner():
    global counter

    def get_emails(amount):
        emails = []
        for _ in range(amount):
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20)) + "@gmail.com"
            emails.append(password)
        return emails
    
    while True:
        try:
            emails = get_emails(50)
            await test_this(emails)
            print(counter)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(runner())
