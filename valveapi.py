#!/usr/bin/env python
import dota2api, json

api = dota2api.Initialise()
livegames = api.get_live_league_games()
#parsed = json.loads(str(livegames))

print(livegames.name)
#print(json.dumps(parsed, indent=2, sort_keys=True))
