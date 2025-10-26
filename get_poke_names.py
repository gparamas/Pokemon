import json

def main():
    pokemon = dict()
    with open('list_pokemon.txt', 'r') as f:
        data = json.load(f)
        pokemon = data['pokemon_species']
    names = []
    for p in pokemon:
        names.append(p['name'])
    with open('names.txt', 'w') as f:
        f.write(','.join(names))

main()