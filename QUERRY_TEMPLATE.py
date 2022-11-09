
VIDEOGAME_QUERRY = """
query GetVideoGame($IdRange: [ID]) {
  videogames(query: {
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