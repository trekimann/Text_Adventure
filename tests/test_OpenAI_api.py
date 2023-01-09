import pytest

import src

@pytest.mark.test
def test_call_openAI_to_create_new_enemies():
    # Test that the OpenAI API is called to create a new map
    enemy_description = "Stargate SG-1"
    api = src.api.OpenAI_api.OpenAI_API()
    map_JSON = api.generate_enemy_JSON(enemy_description)
    assert map_JSON != None
    assert map_JSON != ""
    assert type(map_JSON) == str

@pytest.mark.test
def test_raw_return_is_cleaned():
    raw_return = '\n\n[{"enemyType": "Goa\'uld", "name": "Jaffa Warrior", "description": "The Jaffa are a race of genetically engineered humanoids used by the Goa\'uld System Lords as their primary military force. They are fiercely loyal to their masters and will stop at nothing to complete their assigned tasks. Jaffa Warriors are highly trained in the art of combat, skilled with a variety of weapons, and have the added bonus of being able to carry and use the Goa\'uld Staff Weapon. They also have the ability to invoke the Goa\'uld Symbiote within them, granting them increased strength, stamina, and healing ability.", "health": 100, "loot_chance": 0.5, "loot": "Federation Credit", "lootAmount": 200, "damage_resistance_multiplier": 2.0, "attack_multiplier": 1.5}, {"enemyType": "Wraith", "name": "Wraith Drone", "description": "The Wraith are a race of aliens native to the Pegasus Galaxy. They are highly advanced and incredibly powerful, capable of draining the life force of their victims, and even turning them into mindless drones to do their bidding. The Wraith Drone is the basic soldier of the Wraith army, armed with a staff weapon and formidable combat skills. They are deadly in both combat and in their special ability to drain the life force from their victims.", "health": 50, "loot_chance": 0.8, "loot": "Ancient Technology", "lootAmount": 1, "damage_resistance_multiplier": 1.5, "attack_multiplier": 1.2}, {"enemyType": "Replicator", "name": "Replicator Drone", "description": "The Replicators are an advanced race of robotic lifeforms created by the Asgard to combat the Goa\'uld. The Replicators have a single goal: to replicate and spread as far and as fast as possible. The Replicator Drone is the basic fighting unit of this powerful race, equipped with advanced weapons and tactics to thwart all attempts to stop it. It is virtually impossible to destroy, with the ability to repair and rebuild itself even after taking heavy damage.", "health": 75, "loot_chance": 0.3, "loot": "Naquadah", "lootAmount": 150, "damage_resistance_multiplier": 1.5, "attack_multiplier": 2.5}, {"enemyType": "Asgard", "name": "Asgard Clone", "description": "The Asgard are an ancient race of powerful, god-like beings that once roamed the universe. They are now extinct, but their advanced technology and knowledge has been passed on to the younger races. The Asgard Clones are artificially created replications of the Asgard, with all of their power and knowledge. They are highly advanced and can take many forms, with devastating weapons and tactics to protect their creator.", "health": 200, "loot_chance": 0.75, "loot": "Asgard Technology", "lootAmount": 1, "damage_resistance_multiplier": 5.0, "attack_multiplier": 3.0, "boss": true, "weakAgainst": "Staff Weapon", "weaknessMultiplier": 0.5}]'

    api = src.api.OpenAI_api.OpenAI_API()
    cleaned = api.clean_json_response(raw_return)
    assert cleaned != None
    assert cleaned != ""
