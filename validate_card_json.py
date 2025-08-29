import json
import os

def validate_card_json(card_json_path, images_dir):
    with open(card_json_path, 'r', encoding='utf-8') as f:
        cards = json.load(f)
    image_files = set(os.listdir(images_dir))
    errors = []
    duplicates = set()
    seen = set()
    rare_errors = []
    for card in cards:
        src = card.get('src', '')
        filename = src.split('/')[-1]
        # Verifica duplicidade
        if filename in seen:
            duplicates.add(filename)
        seen.add(filename)
        # Verifica existência
        if filename not in image_files:
            errors.append(filename)
        # Verifica rareza
        is_rare = card.get('rare', False)
        should_be_rare = '-rare' in filename
        if is_rare != should_be_rare:
            rare_errors.append((filename, is_rare, should_be_rare))
    if errors:
        print(f"Imagens não encontradas na pasta: {errors}")
    if duplicates:
        print(f"Imagens duplicadas no card.json: {sorted(list(duplicates))}")
    if rare_errors:
        print("Inconsistência no campo 'rare':")
        for filename, is_rare, should_be_rare in rare_errors:
            print(f"  {filename}: rare={is_rare}, deveria ser {should_be_rare}")
    if not errors and not duplicates and not rare_errors:
        print("Todos os nomes, duplicidades e rareza estão corretos!")

if __name__ == "__main__":
    validate_card_json(
        "./card.json",
        "./images"
    )
