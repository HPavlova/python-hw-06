from aiopath import AsyncPath
import argparse
import asyncio
import concurrent.futures
import logging
from shutil import copyfile
from time import time 

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('-s', '--source', help='source folder')
parser.add_argument('-o', '--output', default='dist', help='output folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')
output_folder = AsyncPath(output)


async def reader(path: AsyncPath) -> list:
    result = []
    async for item in path.iterdir():
        if await item.is_dir():
            print(f"{item} - is folder")
            if await len(reader(item)):
                result = result + reader(item)
            print(result)
        else:
            print(f"{item} - is file")
            result.append(item)
            print (result)
    return result


async def copy_file(file: AsyncPath) -> None:
    ext = file.suffix
    new_path = output_folder/ext
    new_path.mkdir(parents=True, exist_ok=True)
    await copyfile(file, new_path / file.name)
    logging.info(f'{file.name} copied')


async def start():
    path = input("Enter path to folder: ").strip()
    source_path: AsyncPath = AsyncPath(path)

    if len(path) < 1:
        print("Path is empty.Try again!")
    if await source_path.exists():
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for el in reader(source_path):
                futures.append(executor.submit(copy_file, el))
        logging.info('Done')
    else:
        print("Path is not exists.Try again!")
        await start()
        

if __name__ == '__main__':
    start_time = time()
    asyncio.run(start())
    print(f'"Completed in" {time() - start_time} seconds')
