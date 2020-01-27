import json
import collections

def extract_goals_from_goal_dict(goal):
    for key, value in goal.items():
        if key not in ["message", "topic"] and len(value) > 0:
            yield key

# def extract_slots_from_semis(current, new):
#     result = {}
#     for name, current_value in current.items():
#         new_value = new[name]
#         if new_value != "not mentioned" and new_value != current_value:
#             result[name] = new_value
#     return result

def extract_training_data_from_item(item):
    goals = list(extract_goals_from_goal_dict(item["goal"]))
    if len(goals) > 1:
        return
    goal = goals[0]
    turns = item["log"]
    # num_system_turns = int(len(turns) / 2)
    # current_semi = {}
    # for system_turn_index in range(num_system_turns):
    #     user_turn = turns[system_turn_index * 2]
    #     system_turn = turns[system_turn_index * 2 + 1]
    #     new_semi = system_turn["metadata"][goal]["semi"]
    #     utterance = user_turn["text"]
    #     training_datum = {"utterance": utterance}
    #     if system_turn_index == 0:
    #         training_datum["intent"] = goal
    #     training_datum["slots"] = extract_slots_from_semis(current_semi, new_semi)
    #     current_semi = new_semi
    #     yield training_datum
    utterance = turns[0]["text"]
    return {"utterance": utterance,
            "intent": goal}

if __name__ == "__main__":
    f = open("data/MULTIWOZ2.1/data.json")
    training_data = collections.defaultdict(list)
    data = json.load(f)
    for item in data.values():
        training_datum = extract_training_data_from_item(item)
        if training_datum:
            training_data[training_datum["intent"]].append(training_datum["utterance"])
    for intent, utterances in training_data.items():
        print("## intent:{}".format(intent))
        for utterance in utterances:
            print("- {}".format(utterance))
        print()
