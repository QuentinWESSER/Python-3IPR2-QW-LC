
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

TOURNAMENTS_QUERRY = """
query GetVideoGame($IdRange: [ID], $Loca: String, $Range: String, $Start: Timestamp, $End: Timestamp) {
  tournaments(query: {
    perPage : 500
    filter: {
      videogameIds: $IdRange,
      location: {
        distanceFrom: $Loca,
        distance: $Range
      },
      afterDate: $Start,
      beforeDate: $End
    }
  }){
    nodes {
      id
    },
    pageInfo {
      totalPages
    }
  }
}
"""

TOURNAMENTS_QUERRY_VAR = {
  "IdRange" : [], 
  "Loca": "",
  "Range": "" ,
  "Start": 0, 
  "End": 0
}