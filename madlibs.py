# Mad Libs Game
# My first python project :)

import random

# list of stories to pick from
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


def get_word_from_user(word_type):
    # keep asking until user types something
    while True:
        user_input = input(f"  Enter a {word_type}: ").strip()
        if user_input == "":
            print("  please dont leave it empty!")
        else:
            return user_input


def play_game():
    print("=" * 40)
    print("   Welcome to Mad Libs!")
    print("=" * 40)
    print()

    # pick a random story
    story = random.choice(stories)

    print(f"Story: {story['title']}")
    print()
    print("Fill in the blanks to create your story!")
    print("-" * 40)

    # collect all the words from user
    user_words = []
    seen = {}  # to avoid asking for same type twice in a row

    for word_type in story["words"]:
        word = get_word_from_user(word_type)
        user_words.append(word)

    # now fill the story
    filled_story = story["story"]
    for word in user_words:
        # replace only the first {} found
        filled_story = filled_story.replace("{" + filled_story.split("{")[1].split("}")[0] + "}", word, 1)

    print()
    print("=" * 40)
    print("   Here is your story!")
    print("=" * 40)
    print()
    print(filled_story)
    print()


def main():
    while True:
        play_game()

        print("-" * 40)
        again = input("Play again? (yes / no): ").strip().lower()
        if again != "yes" and again != "y":
            print()
            print("Thanks for playing, bye!")
            break
        print()


# this makes sure main() only runs when we run this file directly
if __name__ == "__main__":
    main()