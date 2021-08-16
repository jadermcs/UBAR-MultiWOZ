import json

path = "data/MultiWOZ_2.2"

acts = json.load(open(f"{path}/dialog_acts.json"))
trans = json.load(open("corrections.json"))

parse_data = {}
for i in range(1, 18):
    with open(f"{path}/train/dialogues_{i:03}.json", encoding="utf-8") as fin:
        data = json.load(fin)
        for entry in data:
            parse = {}
            did = entry["dialogue_id"].split(".")[0].lower()
            parse_data[did] = {}
            goal = entry["services"]
            for g in goal:
                parse[g] = {"info":{}, "fail_info":{}, "book":{}, "fail_book":{}}

            log = []
            for turn in range(len(entry["turns"])//2):
                log_entry = {}
                log_entry["user"] = entry["turns"][turn*2]["utterance"]
                # TODO delex
                log_entry["user_delex"] = entry["turns"][turn*2]["utterance"]
                log_entry["resp"] = entry["turns"][turn*2+1]["utterance"]
                log_entry["turn_num"] = turn
                dialog_acts = acts[did.upper()+".json"][str(turn*2+1)]["dialog_act"]
                acts_list = []
                for (k, v) in dialog_acts.items():
                    acts_list += ["["+x+"]" for x in k.lower().split('-')]
                    acts_list += list(set([x[0].replace("book","",1) for x in v if x[0] != "none"]))
                log_entry["sys_act"] = " ".join([trans[x] for x in acts_list])

                constraint = []
                constraint_delex = []
                for cons in entry["turns"][turn*2]["frames"]:
                    if cons["service"] in goal:
                        constraint.append("["+cons["service"]+"]")
                        constraint_delex.append("["+cons["service"]+"]")
                        for (k,v) in cons["state"]["slot_values"].items():
                            key = k.split("-")[1]
                            if key.startswith("book"):
                                parse[cons["service"]]["book"][key.lstrip("book")] = v[0]
                                constraint.append(key.lstrip("book"))
                                constraint_delex.append(key.lstrip("book"))
                            else:
                                parse[cons["service"]]["info"][key] = v[0]
                                constraint.append(key)
                                constraint_delex.append(key)
                            constraint.append(" ".join(v).lower())

                log_entry["constraint"] = " ".join(trans[x] for x in constraint)
                log_entry["cons_delex"] = " ".join(trans[x] for x in constraint_delex)
                # TODO fix turn_domain
                if "[general]" in acts_list:
                    log_entry["turn_domain"] = "[general]"
                elif acts_list and acts_list[0] != "[booking]":
                    log_entry["turn_domain"] = acts_list[0]
                elif constraint:
                    log_entry["turn_domain"] = constraint[0]
                else:
                    log_entry["turn_domain"] = "[general]"
                if log_entry["turn_domain"] == "[bus]":
                    log_entry["turn_domain"] = "[train]"
                # TODO set pointer to right value
                log_entry["pointer"] = "0,1,0,0,0,0"
                # TODO set match to right value
                log_entry["match"] = "1"
                log.append(log_entry)

            parse_data[did]["goal"] = parse
            parse_data[did]["log"] = log

            if did == "pmul4398":
                print(json.dumps(parse_data[did], indent=2))

with open("data_for_damd.json", "w") as fout:
    json.dump(parse_data, fout, indent=2)
