from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

# player
players = {'rachin': 100, 'tamim': 100, 'eman': 100, 'ibrahim': 100}
weapons = {'akm':20, 'm416': 7, 'grenade': 100}
healing_items = {'painkiller': 25, 'firstaid': 75, 'drink': 10}
elimination_count = {}

class AttackInput(BaseModel):
    action: str
    weapon: str
    bulletCount: int
    target: str
    attacker: str


@tool
def attacking(action: str, weapon: str, bulletCount: int, target: str, attacker:str) -> str:
    '''
     This tool allows the AI agent to attack a target player using a specified weapon.
    
    Actions: 'fire' and 'throw'
    - fire (reduce player health based on the weapon damage)
    - throw (player will receive granade damage)
    
    args:
    - target: Name  of the player being attacked
    - weapon: Type of weapon used ("bullet", "grenade")
    - action: what weapon is used
    -bulletCount: number of bullet that the target player received
    -attacker: who fire bullet or throw a grenade to the target
    
    returns:
    - A string message describing the result of the attack, including damage dealt and remaining health of the target.
    
    Notes:
    - If the target's health reaches 0, they are eliminated.
    - If an invalid weapon is used, the attack fails.

    '''

    action = action.lower()
    weapon = weapon.lower()
    attacker = attacker.lower()
    target = target.lower()

    if weapon not in weapons:
        return f"Invalid weapon: {weapon}"

    if target not in players:
        return f"Invalid target: {target}"

    if attacker not in players:
        return f"Invalid attacker: {attacker}"
    
    bulletCount = int(bulletCount)


    
    if action == 'fire':
        players[target] -= (weapons[weapon]*bulletCount)

        if players[target] <= 0 :
            print(f'[Tool 1 use] {players} is dead')
            players[target] = 0
            if attacker not in elimination_count:
                elimination_count[attacker] = 1
            else:
                elimination_count[attacker] += 1
            return f'player -> {attacker} killed player -> {target}'
        
        else:
            return f'[Tool 1 use] player -> {target} receive {weapons[weapon]*bulletCount} damage'

    if action == 'throw':
         print(f'[Tool 1 use] {target} is dead by grenade')
         players[target] = 0
         if attacker not in elimination_count:
            elimination_count[attacker] = 1
         else:
            elimination_count[attacker] += 1
         return f'player -> {attacker} killed player -> {target}'



    return f"Invalid action: {action}"


@tool
def healing(target: str, healing_type: str) -> str:
    """
    This tool allows a player to restore health using a specific healing method.
    
    Actions: "use" and "level"
    - use: Applies healing to the target player.
    - level: Increases the player's health based on the healing type used.
    
    args:
    - target: Name of the player receiving healing
    - healing_type: Type of healing used (e.g., "painkiller", "firstaid", "drink")
    
    returns:
    - A string message describing the result of the healing, including health restored and current health of the target.
    
    Notes:
    - Health cannot exceed the maximum limit
    - If an invalid healing type is used, the action fails
    """
    target = target.lower()
    healing_type = healing_type.lower()

    if healing_type not in healing_items:
        return f"Invalid healing item: {healing_type}"
     
    players[target] += healing_items[healing_type]

    if players[target] > 100:
        players[target] = 100

    print(f'[Tool2 use] player {target} use {healing_type} for recovary. new health level is {players[target]}')

    return f'player {target} successfully recover'

@tool
def killing_rank() -> str:
    '''
    this tool is use to see the leader board, who kill how much enemies.
    '''
    return f'leader board {elimination_count}'



model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')
tools = [attacking,healing, killing_rank]


agent = create_agent(model, tools, system_prompt='You are a Game Monitor AI Agent responsible for observing gameplay and tracking all player actions. Use the appropriate tools to process each action and update the game state accurately and consistently.')

print(f'--------- GAME START --------')
print(f'Initial health of players:{players}')

while True:
    user_input = input('Do you want to play the game or quit?: ')

    if user_input.lower() in ['quit', 'exit']:
        break

    response = agent.invoke({'messages':[('user',user_input)]})

    print(f"-_-_-_ {response['messages'][-1].content}")
    print(f'--__-- player state = {players}')

    # python3 C2-tools/task_game.py



    '''
 Just built a small Game Monitor AI Agent using LangChain and Google’s Gemini API.

It can track player actions like attacks, healing, and eliminations, and updates the game state in real time through custom tools.

This was a fun way to really understand how agents actually use tools instead of just calling APIs blindly.

Still a lot to improve—thinking of adding memory and more complex game logic next.

    '''
 