# Mad Libs Game
# My first python project :)
# Update 1: Added rating system so you can see your funniest stories
# Update 2: Added multiplayer mode (2 players take turns) + code cleanup
# Update 3: Added single-player mode

import random

# ---------------------------------------------------------------------------
# STORIES
# Each story has a title, a template string with {placeholders},
# and a list of word types in the order they appear in the template.
# ---------------------------------------------------------------------------

stories = [
    {
        "title": "A Day at School",
        "story": (
            "Today at school, my {adjective} teacher asked me to bring a {noun} to class.\n"
            "I forgot it at home so I had to {verb} all the way back.\n"
            "When I came back everyone started to {verb} and it was so {adjective}.\n"
            "My best friend {name} said it was the most {adjective} thing they ever saw.\n"
            "I will never forget this {adjective} day."
        ),
        "words": ["adjective", "noun", "verb", "verb", "adjective", "name", "adjective", "adjective"]
    },
    {
        "title": "A Trip to the Supermarket",
        "story": (
            "I went to the supermarket to buy some {noun}.\n"
            "The place was so {adjective} I almost started to {verb}.\n"
            "A {adjective} old man was blocking the aisle with his {noun}.\n"
            "I said excuse me and he started to {verb} really loudly.\n"
            "I grabbed my stuff and {verb} out of there as fast as I could.\n"
            "Never going to that {adjective} supermarket again."
        ),
        "words": ["noun", "adjective", "verb", "adjective", "noun", "verb", "verb", "adjective"]
    },
    {
        "title": "My Pet",
        "story": (
            "I have a {adjective} pet {animal} named {name}.\n"
            "Every morning it likes to {verb} on my bed.\n"
            "One day it ate my {noun} and I was so {adjective}.\n"
            "I took it to the {adjective} vet and she said it was totally fine.\n"
            "My pet is honestly the most {adjective} thing in my life."
        ),
        "words": ["adjective", "animal", "name", "verb", "noun", "adjective", "adjective", "adjective"]
    }
]

# Stores every round's result for multiplayer: title, each player's rating, and the winner
all_scores = []

# Stores every round's result for single-player: title and rating
solo_scores = []


# ---------------------------------------------------------------------------
# INPUT HELPERS
# ---------------------------------------------------------------------------

def get_word(player_name, word_type):
    """Prompt a specific player for a word and keep asking until they enter one."""
    while True:
        user_input = input(f"  [{player_name}] Enter a {word_type}: ").strip()
        if user_input:
            return user_input
        print("  Please don't leave it empty — type something!")


def get_rating(player_name):
    """Ask a player to rate the story 1–5. Returns the integer rating."""
    while True:
        try:
            rating = int(input(f"  [{player_name}] Rate the story (1–5 stars): ").strip())
            if 1 <= rating <= 5:
                return rating
            print("  Please pick a number between 1 and 5.")
        except ValueError:
            print("  That's not a number — try again.")


def get_player_names():
    """Ask for two player names at the start of a multiplayer session."""
    print("  Enter names for both players (press Enter to use defaults).")
    name1 = input("  Player 1 name [Player 1]: ").strip() or "Player 1"
    name2 = input("  Player 2 name [Player 2]: ").strip() or "Player 2"
    return name1, name2


def get_single_player_name():
    """Ask for a single player's name."""
    name = input("  Your name [Player]: ").strip() or "Player"
    return name


# ---------------------------------------------------------------------------
# SCOREBOARD
# ---------------------------------------------------------------------------

def show_scoreboard(players):
    """Print a formatted scoreboard for all completed multiplayer rounds."""
    if not all_scores:
        print("  No scores yet — play a round first!")
        return

    p1, p2 = players
    print()
    print("=" * 50)
    print("   Scoreboard")
    print("=" * 50)
    print(f"  {'Round':<8} {'Story':<28} {p1:<12} {p2:<12} {'Winner'}")
    print("-" * 50)

    for i, entry in enumerate(all_scores, start=1):
        r1 = "*" * entry["p1_rating"]
        r2 = "*" * entry["p2_rating"]
        winner = entry["winner"]
        print(f"  {i:<8} {entry['title']:<28} {r1:<12} {r2:<12} {winner}")

    # Overall winner based on total stars
    total_p1 = sum(e["p1_rating"] for e in all_scores)
    total_p2 = sum(e["p2_rating"] for e in all_scores)
    avg_p1 = total_p1 / len(all_scores)
    avg_p2 = total_p2 / len(all_scores)

    print("-" * 50)
    print(f"  Avg ratings  —  {p1}: {avg_p1:.1f}/5.0   {p2}: {avg_p2:.1f}/5.0")

    if total_p1 > total_p2:
        overall = p1
    elif total_p2 > total_p1:
        overall = p2
    else:
        overall = "Tie!"

    print(f"  Overall winner: {overall}")
    print()


def show_scoreboard_single(player_name):
    """Print a formatted scoreboard for all completed single-player rounds."""
    if not solo_scores:
        print("  No scores yet — play a round first!")
        return

    print()
    print("=" * 50)
    print(f"   {player_name}'s Scoreboard")
    print("=" * 50)
    print(f"  {'Round':<8} {'Story':<28} {'Rating'}")
    print("-" * 50)

    for i, entry in enumerate(solo_scores, start=1):
        stars = "*" * entry["rating"]
        print(f"  {i:<8} {entry['title']:<28} {stars}")

    avg = sum(e["rating"] for e in solo_scores) / len(solo_scores)
    best = max(solo_scores, key=lambda e: e["rating"])

    print("-" * 50)
    print(f"  Average rating : {avg:.1f}/5.0")
    print(f"  Best story     : \"{best['title']}\" ({best['rating']}/5)")
    print()


# ---------------------------------------------------------------------------
# GAME ROUNDS
# ---------------------------------------------------------------------------

def play_round(players):
    """
    Run one full round of Mad Libs in multiplayer mode.

    How it works:
      - Player 1 fills in the blanks (without seeing the story template).
      - The completed story is revealed to both players.
      - Player 2 then fills in the blanks for the SAME story template.
      - That version is revealed too.
      - Both players rate the other's story.
      - The player whose story gets the higher combined score wins the round.
    """
    p1, p2 = players
    story = random.choice(stories)

    print()
    print(f"  Story: \"{story['title']}\"")
    print("  Fill in the blanks — no peeking at the story!")
    print("-" * 50)

    # --- Player 1's turn ---
    print(f"\n  {p1}'s turn to fill in words:")
    words_p1 = [get_word(p1, wt) for wt in story["words"]]
    story_p1 = _fill_story(story["story"], words_p1)

    print()
    print("=" * 50)
    print(f"   {p1}'s story:")
    print("=" * 50)
    print()
    print(story_p1)
    print()

    # --- Player 2's turn ---
    print(f"\n  {p2}'s turn to fill in the SAME blanks:")
    words_p2 = [get_word(p2, wt) for wt in story["words"]]
    story_p2 = _fill_story(story["story"], words_p2)

    print()
    print("=" * 50)
    print(f"   {p2}'s story:")
    print("=" * 50)
    print()
    print(story_p2)
    print()

    # --- Rating phase ---
    # Each player rates the OTHER player's story to keep it fair.
    print("-" * 50)
    print("  Time to rate each other's stories!")
    print(f"  {p2}, rate {p1}'s story:")
    rating_p1 = get_rating(p2)   # p2 rates p1's story

    print(f"  {p1}, rate {p2}'s story:")
    rating_p2 = get_rating(p1)   # p1 rates p2's story

    # Determine round winner
    if rating_p1 > rating_p2:
        winner = p1
    elif rating_p2 > rating_p1:
        winner = p2
    else:
        winner = "Tie"

    print()
    print(f"  Round result: {p1} {rating_p1}/5  vs  {p2} {rating_p2}/5  —  Winner: {winner}")
    print()

    # Save this round's results
    all_scores.append({
        "title": story["title"],
        "p1_rating": rating_p1,
        "p2_rating": rating_p2,
        "winner": winner
    })


def play_round_single(player_name):
    """
    Run one full round of Mad Libs in single-player mode.

    How it works:
      - The player fills in all the blanks without seeing the story.
      - The completed story is revealed.
      - The player rates their own story for fun.
      - The result is saved to their personal scoreboard.
    """
    story = random.choice(stories)

    print()
    print(f"  Story: \"{story['title']}\"")
    print("  Fill in the blanks — no peeking at the story!")
    print("-" * 50)

    words = [get_word(player_name, wt) for wt in story["words"]]
    completed = _fill_story(story["story"], words)

    print()
    print("=" * 50)
    print(f"   Your story:")
    print("=" * 50)
    print()
    print(completed)
    print()

    # Player rates their own story
    print("-" * 50)
    rating = get_rating(player_name)

    stars = "*" * rating
    print(f"\n  You gave it {stars} ({rating}/5) — nice!")
    print()

    # Save this round's result
    solo_scores.append({
        "title": story["title"],
        "rating": rating
    })


def _fill_story(template, words):
    """
    Replace each {placeholder} in the template with the corresponding word.
    Words are substituted in the order they appear (left to right).
    """
    result = template
    for word in words:
        # Find the next placeholder name between the first { } pair
        placeholder = result.split("{")[1].split("}")[0]
        result = result.replace("{" + placeholder + "}", word, 1)
    return result


# ---------------------------------------------------------------------------
# MODE SELECTION
# ---------------------------------------------------------------------------

def pick_mode():
    """Ask the player(s) whether they want single-player or multiplayer mode."""
    print("  How many players?")
    print("    1 — Single player")
    print("    2 — Multiplayer (2 players take turns)")
    while True:
        choice = input("  Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            return int(choice)
        print("  Please enter 1 or 2.")


# ---------------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 50)
    print("   Welcome to Mad Libs!")
    print("=" * 50)
    print()

    mode = pick_mode()
    print()

    # ── Single-player loop ──────────────────────────────────────────────────
    if mode == 1:
        player_name = get_single_player_name()
        print(f"\n  Let's go, {player_name}!\n")

        while True:
            play_round_single(player_name)

            print("-" * 50)
            again = input("  Play another round? (yes / no): ").strip().lower()

            if again in ("yes", "y"):
                see_scores = input("  See your scoreboard first? (yes / no): ").strip().lower()
                if see_scores in ("yes", "y"):
                    show_scoreboard_single(player_name)
            else:
                show_scoreboard_single(player_name)
                print("  Thanks for playing — goodbye!")
                break

    # ── Multiplayer loop ────────────────────────────────────────────────────
    else:
        players = get_player_names()
        p1, p2 = players
        print(f"\n  Let's go, {p1} vs {p2}!\n")

        while True:
            play_round(players)

            print("-" * 50)
            again = input("  Play another round? (yes / no): ").strip().lower()

            if again in ("yes", "y"):
                see_scores = input("  See the scoreboard first? (yes / no): ").strip().lower()
                if see_scores in ("yes", "y"):
                    show_scoreboard(players)
            else:
                show_scoreboard(players)
                print("  Thanks for playing — goodbye!")
                break


# Run main() only when this file is executed directly (not imported)
if __name__ == "__main__":
    main()
