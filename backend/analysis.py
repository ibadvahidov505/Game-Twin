GENRE_MAP = {
    "fps": ("Soldier", ["competitive", "action", "reflexes"]),
    "moba": ("Strategist", ["competitive", "tactical", "teamwork"]),
    "battle royale": ("Survivor", ["competitive", "survival", "adaptable"]),
    "fighting": ("Combat Master", ["competitive", "melee", "precision"]),
    "rts": ("Commander", ["competitive", "tactical", "resourceful"]),
    "rpg": ("Story Knight", ["rpg", "narrative", "adventurous"]),
    "adventure": ("Explorer", ["story", "curious", "discovery"]),
    "visual novel": ("Story Reader", ["story", "narrative", "immersive"]),
    "interactive drama": ("Narrative Seeker", ["story", "narrative", "cinematic"]),
    "stealth": ("Shadow Ninja", ["stealth", "tactical", "patient"]),
    "ninja": ("Silent Blade", ["stealth", "agile", "precise"]),
    "racing": ("Auto Master", ["racing", "speed", "competitive"]),
    "driving": ("Speed Racer", ["racing", "speed", "exploration"]),
}


def analyze_player(genres, hours_played=None, achievements=None):
    genres_lower = [g.lower() for g in genres]

    archetype_counts = {}
    matched_tags = {}

    for g in genres_lower:
        entry = GENRE_MAP.get(g)
        if entry:
            archetype, tags = entry
            archetype_counts[archetype] = archetype_counts.get(archetype, 0) + 1
            if archetype not in matched_tags:
                matched_tags[archetype] = []
            matched_tags[archetype].extend(tags)

    if not archetype_counts:
        return {
            "archetype": "Wanderer",
            "confidence": 50,
            "tags": ["undefined", "uncategorized", "free-spirit"],
        }

    best_archetype = max(archetype_counts, key=lambda a: (archetype_counts[a], a))
    match_count = archetype_counts[best_archetype]

    confidence = 50 + int((match_count / len(genres_lower)) * 50)

    tags = list(dict.fromkeys(matched_tags[best_archetype]))[:5]

    return {
        "archetype": best_archetype,
        "confidence": confidence,
        "tags": tags,
    }
