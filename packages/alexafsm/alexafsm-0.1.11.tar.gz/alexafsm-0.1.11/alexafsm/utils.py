import inspect
import json

from typing import Set

from alexafsm.policy import Policy
from alexafsm.session_attributes import INITIAL_STATE


def validate(policy: Policy, schema_file: str, ignore_intents: Set[str] = ()):
    """Check for inconsistencies in policy definition"""
    schema = {}
    with open(schema_file, mode='r') as f:
        schema = json.loads(f.read())

    intents = [intent['intent'] for intent in schema['intents']
               if intent['intent'] not in ignore_intents]
    states = policy.machine.states
    events = []
    states_have_out_transitions = set()
    states_have_in_transitions = set()
    funcs = [func for func, _ in inspect.getmembers(type(policy), predicate=inspect.isfunction)]

    def _validate_transition(tran):
        assert tran.source in states, f"Invalid source state: {tran.source}!!"
        assert tran.dest in states, f"Invalid dest state: {tran.dest}!!"
        assert all(prep in funcs for prep in tran.prepare), \
            f"Invalid prepare function: {tran.prepare}!!"
        assert all(cond.func in funcs for cond in tran.conditions), \
            f"Invalid conditions function: {tran.conditions}!!"
        assert all(after in funcs for after in tran.after), \
            f"Invalid after function: {tran.after}!!"

        states_have_in_transitions.add(tran.dest)
        states_have_out_transitions.add(tran.source)

    def _validate_ambiguous_transition(event, source, trans):
        unconditional_trans = [tran for tran in trans if not tran.conditions]
        assert len(unconditional_trans) < 2,\
            f"Event {event} for source {source} has multiple unconditional out-bound transitions:" \
            f" {', '.join([tran.dest for tran in trans])}"

    for _, event in policy.machine.events.items():
        assert event.name in intents, f"Invalid event/trigger: {event.name}!"
        events.append(event.name)

        for source, trans in event.transitions.items():
            for transition in trans:
                assert source in states, f"Invalid source state: {source}!!"
                _validate_transition(transition)

            _validate_ambiguous_transition(event.name, source, trans)

    intent_diff = set(intents) - set(events)
    assert not intent_diff, f"Some intents are not handled: {intent_diff}"

    in_diff = set(states) - states_have_in_transitions - {INITIAL_STATE}
    out_diff = set(states) - states_have_out_transitions - set('exiting')

    assert not in_diff, f"Some states have no inbound transitions: {in_diff}"
    assert not out_diff, f"Some states have no outbound transitions: {out_diff}"


def print_machine(policy: Policy):
    def _print_transition(tran):
        print(f"\t\t{tran.source} -> {tran.dest}", end='')
        if tran.prepare:
            print(f", prepare: {tran.prepare}", end='')
        if tran.conditions:
            print(f", conditions: {[cond.func for cond in tran.conditions]}", end='')
        print()

    print(f"Machine states:\n\t{', '.join(policy.machine.states)}")
    print("\nEvents and transitions:\n")
    for _, event in policy.machine.events.items():
        print(f"Event: {event.name}")

        for source, trans in event.transitions.items():
            print(f"\tSource: {source}")
            for transition in trans:
                _print_transition(transition)


def graph(policy_cls, png_file):
    policy = policy_cls.initialize(with_graph=True)
    policy.graph.draw(png_file, prog='dot')


def get_dialogs(request, response):
    """Return key information about a conversation turn as stored in a pair of request & response"""
    request_id = request['request']['requestId']

    # there are no attributes when starting a new conversation from the alexa device
    session_attributes = request['session'].get('attributes', {})
    from_state = session_attributes.get('state', INITIAL_STATE)
    intent = response['sessionAttributes'].get('intent', None)
    slots = response['sessionAttributes'].get('slots', None)
    to_state = response['sessionAttributes'].get('state', None)
    speech = response['response']['outputSpeech']['text']
    return request_id, from_state, intent, slots, to_state, speech


def events_states_transitions(policy: Policy):
    """
    Return events, states, and transitions of a policy.
    Initial and exiting states are excluded
    """
    all_states = set(policy.machine.states.keys())
    all_states.remove(INITIAL_STATE)
    all_states.remove('exiting')
    all_events = set()
    all_transitions = set()
    for _, e in policy.machine.events.items():
        all_events.add(e.name)
        for source, transitions in e.transitions.items():
            for transition in transitions:
                all_transitions.add((source, transition.dest))

    return all_events, all_states, all_transitions


def used_events_states_transitions(recorded_requests_responses):
    """Based on recorded data, compute and return the used events, states, and transitions"""
    used_events = set()
    used_states = set()
    used_transitions = set()
    dialog_data = [get_dialogs(request, response)
                   for request, response in recorded_requests_responses]
    for request_id, from_state, intent, slots, to_state, speech in dialog_data:
        used_events.add(intent)
        used_states.add(from_state)
        used_states.add(to_state)
        used_transitions.add((from_state, to_state))

    if INITIAL_STATE in used_states:
        used_states.remove(INITIAL_STATE)
    return used_events, used_states, used_transitions


def unused_events_states_transitions(policy, recorded_requests_responses):
    """Based on recorded data and a policy, compute and return the unused events, states, and
     transitions"""
    all_events, all_states, all_transitions = events_states_transitions(policy)
    used_events, used_states, used_transitions = used_events_states_transitions(recorded_requests_responses)
    unused_states = all_states - used_states
    unused_events = all_events - used_events
    unused_transitions = all_transitions - used_transitions
    return unused_events, unused_states, unused_transitions
