import json

# Charger la transcription
with open("../transcription.json", "r", encoding="utf-8") as file:
    transcription = json.load(file)


def search(query):
    query = query.lower().strip()
    results = []

    for segment in transcription["segments"]:
        text = segment["text"]

        if query in text.lower():
            results.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": text
            })

    return results


# Test
if __name__ == "__main__":
    query = input("Rechercher : ")

    results = search(query)

    print(f"\n{len(results)} résultat(s) trouvé(s)\n")

    for result in results:
        print(
            f"[{result['start']}s -> {result['end']}s] "
            f"{result['text']}"
        )