# Sentence Planner takes text plans as input and produces sentence plans

from math import floor
from typing import List
from project.data import TextPlan, SentencePlan


def generate_sentenceplans(textplans: List[TextPlan]) -> List[SentencePlan]:
    # Create empty list of sentence plans
    sentenceplans: List[SentencePlan] = list()

    # Iterate through the text plans
    for textplan in textplans:
        # Check the relation type of the first message in the textplan,
        # route the textplan to the appropriate method,
        # and append its output to the list of sentence plans
        if textplan.messages[0].relation == 'value-in-range':
            sentenceplans.append(sp_value_in_range(textplan))

        if textplan.messages[0].relation == 'condition-in-period':
            sentenceplans.append(sp_condition_in_period(textplan))

    # Return the list of sentence plans
    return sentenceplans


# ValueInRange text plans consist of a single message
def sp_value_in_range(textplan: TextPlan, roundtoten: bool = True) -> SentencePlan:
    # Assume there is only one message in the textplan, take its arguments
    args = textplan.messages[0].arguments

    if args['value'] == 'temperature':
        # Change 'temperature' to 'temperatures'
        subject = 'temperatures'
    else:
        # Otherwise write the name of the value as-is
        subject = args['value']

    # Round integer values to 'the 10s', 'the 20s', etc.
    if roundtoten:
        s_min = f"the {10 * floor(args['minimum'] / 10)}s"
        s_max = f"the {10 * floor(args['maximum'] / 10)}s"
    else:
        s_min = str(args['minimum'])
        s_max = str(args['maximum'])

    # If minimum is the same as maximum, just give the minimum
    if s_min == s_max:
        verb = 'will be in' if roundtoten else 'will be'
        objects = [s_min]
    else:
        verb = 'will range from'
        objects = [f'{s_min} to {s_max}']

    return SentencePlan(subject=subject, verb=verb, objects=objects)


# ConditionInPeriod text plans may consist of one or more messages
# to be aggregated into one sentence
def sp_condition_in_period(textplan: TextPlan) -> SentencePlan:
    # Assume all messages in the textplan refer to the same condition
    subject = textplan.messages[0].arguments['condition']
    verb = 'is predicted for'

    # Create empty list of sentence objects
    objects = []

    # Iterate through messages
    for message in textplan.messages:

        # Extract the arguments from the message
        args = message.arguments

        if args['period_start'] == args['period_end']:
            # If start and end period are the same, write only the start period
            objects.append(args['period_start'])

        elif args['period_end'].startswith(args['period_start']):
            # e.g. If 'sunday through sunday night', then write only 'sunday'
            objects.append(args['period_start'])

        else:
            # Write 'start period through end period'
            objects.append(f"{args['period_start']} through {args['period_end']}")

    # Return the sentence plan
    return SentencePlan(subject=subject, verb=verb, objects=objects)
