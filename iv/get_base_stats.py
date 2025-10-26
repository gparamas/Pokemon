import asyncio
import aiohttp
import json

GENERATION = 2
MAX_CONCURRENT = 10  # limit concurrent requests

semaphore = asyncio.Semaphore(MAX_CONCURRENT)

async def fetch_json(session, url):
    async with semaphore:  # ensures only MAX_CONCURRENT at once
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        # Get generation data
        pokemon = []
        with open('list_pokemon.txt', 'r') as f:
            data = json.load(f)
            pokemon = data['pokemon_species']
  
        # Get Pokémon species URLs
        species_urls = [s['url'].replace('-species', '') for s in pokemon]

        # Fetch Pokémon concurrently (but throttled)
        tasks = [fetch_json(session, url) for url in species_urls]
        results = await asyncio.gather(*tasks)

        # Print Pokémon names
        stats = {x['name'] : {y['stat']['name'] : y['base_stat'] for y in x['stats']} for x in results}
        with open('stats.txt', 'w') as f:
            json.dump(stats, f, indent=4)

asyncio.run(main())
