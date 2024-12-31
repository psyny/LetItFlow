# Endpoints

POST /login
body:
- credentials: credentials

response:
- status: string: status of the login
- player: player: player data of the player id given in credentials

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
- partId: string: current party id
- currentStateOnly: boolean: get only the latest gamestateView, no actions
- statePoint: number: current state point

response:
- statePoint: number: new state point
- gamestateView: gamestateView: state of the game after the actions are taken. based on player access level.
- actions: list of actions since the last state point.


POST /entity
body:
- credentials: credentials
- entityId: string: entityId of the entity being edited
- operation: string: update, delete
- entity: entity

response:
- status: string: result of the operation


POST /entityInstance
body:
- credentials: credentials
- istanceId: string: istanceId of the entity being edited
- operation: string: update, delete
- entityInstance: entityInstance

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
- actionId: string: id of a action instance
- actionType: string: the type of action
- sourceId: string: instanceID of the source
- targetIds: list of strings: instanceIDs of the target
- actionData: list of actionData

actionData: object
- key: string: name of the data
- value: string: value of the data

party: object
- partyId: object: id of the party 
- name: string: name of the party
- playerColors: map of string to string: map playerId to color name
- gamestate: gamestate: current game state of this party

player: object
- playerId: string: player id
- name: string: player name
- active: bool: is the player active?
- accessLevel: map string to string: player access level by party id 

entity: object
- playerId: string: player who usually owns the entity
- entityId: string: entity ID for this entity 
- type: string: entity type (player character, creature, object, etc) 
- name: string: entity name
- label: string: short label to easily identify, usually a number
- active: bool: is entity currently active?
- imageName: string: name of the image object
- baseStats: object: 
-- hp: number: max hp value
-- initiative: number: initiative value
-- dex: number: dex value

entityInstance: object
- instanceId: string: instance id of this instance
- entityId: string: entity that this instance is instance of
- playerId: string: player who currently owns the instance
- label: string: short label to easily identify, usually a number. Same as the entity by default
- stats: object
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

gamestate: object: game state how its saved on the database
- partyId: string: party id
- partyName: string: current party id of the game
- entities: map of string to entity: map entityId to entity objects that are part of this part
- entityInstances: map of string to entityInstance: map instanceId to entity objects that are part of this part
- phase: string: current phase of the game (inactive, lobby, exploration, or tactical)
- inactive: object:
-- title: string: title to display in the inactive game
- tactical: object:
-- inTatical: list of string: entity instanceIds in combat
-- turnOrder: list of string: entity instanceIds in order of turn.
-- currentTurn: string: entity instanceIds who current turn is
- exploration: object:
-- places: map of string to strings: map places to entity instanceIds 
- lobby: object:
-- title: string: title to display in the lobby
- vfxs: list of active vfxs

gamestateView: object: game state how its viewed by the frontend. It's sub fields varies according to access level. 
Has everything a gamestate has, but for the entities and entityInstances has only what its access level permits.
Also has a new field:
- entityInstanceView: map of string to entityInstanceView: map instanceViewId to entityInstanceView objects. How all entities are displayed to this player

# Access Levels
def: defines the access level of each player
- admin: has full access to evertying in the system and everything a dungeonmaster can do.
- dungeonmaster: has control over its party and create new parties. Can create players and attach them to his party. Can create entities, instances, etc. Has control over every entity in its party. Can add VFx, pass turn and change the game phase on the gamestate. And everything a player can do.
- veteran: has control over the entities owned by itself. Can edit its data fields. Can do everything a rookie can do.
- rookie: has control over the entityInstance owned by itself. Can edit its data fields. Can do everything a spectator can do.
- spectator: only view the game, can't control anything. 


# Actions
Actions designed to work both as a signalizer to the backend whats happened to the frontend.
And as a list of things that happened since the last state.
Each actionType is hard coded. The ideia is that the data-based effects of an action is done on the BE.
The FE tells the action it wants to take, the BE checks for permissions, change the data accordingly.
When the FE receives actions (usually via the POST refreshstate endpoint), it do the visual effects of this action.
With the same endpoint the FE will receive the gamestate AFTER the actions are taken. So the FE dont need to know how the actions affects the data.

Possible actionType and its descriptions:
- ChangePhase: change current game phase. ActionData: "NewPhase".
- InstanceUpdate: change an entityInstance data (except entityId). ActionData: "Field", "Value".
- InstanceViewUpdate: change an entityInstanceView data (except entityId). ActionData: "Field", "Value".
- InTactical: adds or removes the entity instance to the tactical mode view. ActionData: "InstanceId", "InTactical" ("true" or "false")
- SetTurnOrder: set the turn order of an ntity instance in tactical mode view: ActionData: "InstanceId", "Position"
- PassTurn: passes current turn on tatical phase. ActionData: empty
- CurrentTurn: sets the current turn on tatical phase to the entityinstance of given id. ActionData: "InstanceId"
- ShortRest: short rest to the entityinstance of given id. ActionData: "InstanceId"
- LongRest: long rest to the entityinstance of given id. ActionData: "InstanceId"