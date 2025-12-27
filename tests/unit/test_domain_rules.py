import pytest
from src.domain.entities.game import Game
from src.domain.entities.console import Console

def test_game_entity_creation():
    """
    Teste Unitário Puro (Domínio): 
    Verifica se a entidade Game pode ser instanciada corretamente.
    """
    game = Game(
        id=1, 
        name="The Legend of Zelda", 
        console_id=99,
        created_at=None,
        updated_at=None
    )
    
    assert game.name == "The Legend of Zelda"
    assert game.console_id == 99

def test_console_entity_creation():
    """
    Teste Unitário Puro (Domínio).
    """
    console = Console(
        id=1,
        name="Switch",
        company="Nintendo",
        created_at=None,
        updated_at=None,
        deleted_at=None
    )
    
    assert console.company == "Nintendo"