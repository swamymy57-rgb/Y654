
"""Game lobby API routes."""

from fastapi import APIRouter, HTTPException, Query

from app.services.game_lobby import GameLobbyService

router = APIRouter(
    prefix="/games",
    tags=["Game Lobby"],
)


@router.get("/lobby")
async def get_lobby():
    """Get complete game lobby information."""

    return GameLobbyService.get_lobby_data()


@router.get("/categories")
async def get_categories():
    """Get all available game categories."""

    return {
        "categories": GameLobbyService.get_categories()
    }


@router.get("/")
async def get_games(
    category: str = Query(default="ALL"),
    search: str | None = Query(default=None, max_length=100),
):
    """Get games with optional category and search filters."""

    valid_categories = {
        item["category_id"]
        for item in GameLobbyService.get_categories()
    }

    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail="Invalid game category",
        )

    if search and search.strip():
        games = GameLobbyService.search_games(search)
    else:
        games = GameLobbyService.get_games_by_category(category)

    if category != "ALL":
        games = [
            game for game in games
            if game["category"] == category
        ]

    return {
        "total": len(games),
        "games": games,
    }


@router.get("/{game_id}")
async def get_game(game_id: str):
    """Get details of a specific game."""

    game = GameLobbyService.get_game(game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    return game
  
