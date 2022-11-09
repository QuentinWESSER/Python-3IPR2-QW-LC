
VIDEOGAME_QUERRY = """
query GetVideoGame($IdRange: [ID]) {
  videogames(query: {
    perPage : 500,
    filter: {
      id : $IdRange
    }
  }){
    nodes{
      id,
      name,
      images {
        url
      }
    }
  }
}
"""

VIDEOGAME_QUERRY_VAR = {
  "IdRange": []
}