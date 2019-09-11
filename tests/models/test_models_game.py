from app.models.game import GameModel


def test_repr(app):
    with app.app_context():
        game = GameModel.query.get(1)
        print(repr(game))
        assert repr(game) == 'ID: 1 NAME: None ST_ID: 1'


def test_comp(app):
    with app.app_context():
        game1 = GameModel.query.get(1)
        game1.patch_from_json({'name': 'a'})
        game2 = GameModel(1)
        game2.patch_from_json({'name': 'z'})
        assert not game1 == game2
        assert game1 < game2


def test_from_json(app):
    data = {
        'name': 'test1',
        'st_id': 1,
        'active': True,
        'lore': 'test2',
        'summary': 'test3'
    }
    with app.app_context():
        game = GameModel.query.get(1)
        game.patch_from_json(data)
        game_json = game.to_json()
        for key in data:
            print(key, data[key], game.__getattribute__(key), game_json[key])
            assert data[key] == game.__getattribute__(key)
            assert data[key] == game_json[key]

        game.patch_from_json({'active': False})
        print(game.active)
        assert not game.active


def test_return_all(app):
    with app.app_context():
        assert len(GameModel.return_all()['games']) == 1
        GameModel(1)
        assert len(GameModel.return_all()['games']) == 2

