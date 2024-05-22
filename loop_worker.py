from pyscript import sync, document, when
import asyncio

val = 1
modifier = 1

async def work_input():
    global val, modifier
    while True:
        val = val*modifier
        output_div = document.querySelector("#output")
        out_div.innerText = str(val)
        await asyncio.sleep(2)
@when("change", "#mod_input")
async def get_input():
    global modifier
    input_mod = document.querySelector("#mod_input")
    modifier = float(input_mod.value)

async def main():
    await asyncio.gather(
        work_input,
        get_input
        )

asyncio.create_task(work_input())
asyncio.create_task(get_input())
