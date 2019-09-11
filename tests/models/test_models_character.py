from app.models.character import CharacterModel


def test_repr(app):
    with app.app_context():
        char = CharacterModel.get_by_id(1)
    print(repr(char))
    assert repr(char) == 'ID: 1 OWNER: 1 NAME: None'


def test_patch_from_json1(app):
    data = {
        'name': 'test1',
        'summary': 'test2',
        'char_type': 'test3',
        'game_id': 1,
        'lore': 'test4',
        'strength': 2,
        'reflex': 3,
        'speed': 4,
        'vitality': 5,
        'awareness': 6,
        'willpower': 7,
        'imagination': 8,
        'attunement': 9,
        'faith': 10,
        'luck': 11,
        'charisma': 12
    }

    with app.app_context():
        character = CharacterModel.get_by_id(1)
        character.patch_from_json(data)
        char_json = character.to_json()
        for key in data:
            print(key, data[key], char_json[key])
            assert data[key] == char_json[key]


def test_patch_from_json2(app):
    with app.app_context():
        char = CharacterModel.get_by_id(1)
        char.patch_from_json({'vitality': 2})
        assert char.vitality == 2


def test_sort(app):
    with app.app_context():
        character1 = CharacterModel.get_by_id(1)
        character1.patch_from_json({'name': 'a'})
        character2 = CharacterModel(1)
        character2.patch_from_json({'name': 'z'})
        assert not character1 == character2
        assert not character2 < character1
