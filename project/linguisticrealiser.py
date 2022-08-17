# Linguistic Realiser takes a list of sentence plans as input
# and produces the final text.

import re
from typing import List
from project.data import SentencePlan


def generate_sentences(sentenceplans: List[SentencePlan]) -> str:
    # Create empty list of sentences
    sentences = []

    # Iterate through the sentence plans
    for plan in sentenceplans:
        # Bring in the subject and verb from the plan & make lowercase
        subject = plan.subject.lower()
        verb = plan.verb.lower()

        # Correct the verb if subject is plural
        if re.match('\w+s\\b', subject) and re.match('is\\b', verb):
            verb = re.sub(r'^is', 'are', verb)

        # List one, two, or three+ objects
        objects = ''
        n_objects = len(plan.objects)
        if n_objects == 1:
            objects = plan.objects[0]
        elif n_objects == 2:
            objects = ' and '.join(plan.objects)
        elif n_objects >= 3:
            objects = ', '.join(plan.objects[:-1]) + ', and ' + plan.objects[-1]

        # Make objects lowercase
        objects = objects.lower()

        # Join the subject, verb, and objects
        sentence = ' '.join([subject, verb, objects])

        # Capitalize only the first letter of the sentence
        sentence = sentence[0].upper() + sentence[1:].lower()

        # Capitalize names of days
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for day in days:
            sentence = sentence.replace(day.lower(), day)

        # End the sentence with a period
        sentence += '.'

        # Add the sentence to the list of sentences
        sentences.append(sentence)

    # Join the list of sentences with a single space and return the result
    return ' '.join(sentences)
