# Endpoints

POST /login
body:
- credentials: credentials

response:
- status: string: status of the login
- permission: string: permission group

POST /actions
body:
- credentials: credentials
- actions: list of action

response:
- status: string


POST /macro
body:
- credentials: credentials
- macro: string: macro name
- parameters: list of objects:
-- key: string: parameter key
-- value: string: parameter value

response:
- status: string



POST /refreshstate
body:
- credentials: credentials
- stateOnly: boolean: get only the latest state, no actions
- statePoint: number: current state point

response:
- statePoint: number: new state point
- gameState: object: state of the game after the actions are taken
- actions: list of action


POST /character
body:
- credentials: credentials
- entityId: string: entityId of the character being edited
- operation: string: update, delete
- character: character

response:
- status: string: result of the operation

POST /player
body:
- credentials: credentials
- playerId: string: playerId being updated
- operation: string: update, delete
- player: player

response:
- status: string: result of the operation

POST /party
body:
- credentials: credentials
- partyId: string: partyId being updated
- operation: string: update, delete
- party: party

response:
- status: string: result of the operation



# Definitions
credentials: object
- playerId: string: player name
- playerKey: string: player pass key

action: object
- sourceId: string: entityID of the source
- targetIds: list of strings: entityIDs of the target
- actionData: list of actionData

actionData: object
- key: string: name of the data
- value: string: value of the data

party: object
- partyId: object: id of the party 
- name: string: name of the party

player: object
- playerId: string: player id
- partyIds: list of string: ids of the party the player is part of
- name: string: player name
- color: map string to string: maps the player color by party id
- permission: map string to string: player permission group by party id

entity: object
- playerId: string: player who owns the entity
- entityId: string: entity ID for this entity 
- type: string: entity type (player character, creature, object, etc) 
- name: string: entity name
- label: string: short label to easily identify, usually a number
- entityBaseStats: object: 
-- hp: number: max hp value
-- initiative: number: initiative value
-- dex: number: dex value
- entitySoftStats: object:
-- hp: number: current hp value
-- tempHp: number: current temp hp
-- initiative: number: current initiative (rolled + bonus)
-- ally: bool: is the entity an ally of the party?
-- visible: bool: is the entity visible by the party?
-- conditions: list of condition: conditions this entity has

condition: object
- conditionId: string: id of the condition
- name: string: condition name
- endTrigger: string: trigger to end this condition (endTurn, startTurn, other)
- endValue: number: number associated with condition end
- effectTrigger: string: when the condition takes effect (endTurn, startTurn, other)
- effectValue: string: number associated with effect value (damage number, etc)

vfx: object
- vfxId: string: id of the vfx
- vfxKey1: string
- vfxVal1: number
- vfxKey2: string
- vfxVal3: number
- vfxKey4: string
- vfxVal4: number

gamestate: object
- entities: list of entity: list of entities currently relevant to the game.
- player: list of players: list of players currently relevant to the game.
- vfxs: list of vfx
- phase: string: current phase of the game (combat, exploration, lobby, etc)
- combat: object:
-- turnOrder: list of string: entityIds, in order of turn.
-- currentTurn: string: entity Id who current turn is
- exploration: object:
-- places: map of string to strings: map places to entityId
- lobby: object:
-- title: string: tittle to display in the lobby



