
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
query GetTournaments($IdRange: [ID], $Loca: String, $Range: String, $Start: Timestamp, $End: Timestamp, $Page: Int) {
  tournaments(query: {
    perPage : 500,
    page : $Page
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
      id,
      name,
      endAt,
      venueAddress,
      images{
        url
      }
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
  "End": 0,
  "Page": 0
}

TOURNAMENT_QUERRY = """
query GetTournament($TournamentID: ID) {
  tournaments(query: {
    perPage : 500,
    page : 1,
    filter: {
      id: $TournamentID
    }
  }){
    nodes {
      id,
      name,
      city,
      venueAddress,
      startAt,
      endAt,
      numAttendees,
      url(relative:false),
      participants(query: {
        page:1,
        perPage:500
      }) {
        nodes{
          entrants {
            seeds { placement }
          },
          player{
            id
          }
        }
      }
    }
  }
}
"""

TOURNAMENT_QUERRY_VAR = {
  "TournamentID": 0
}

SETS_QUERRY = """
query GetSets($PlayerID: ID!) {
  player(id: $PlayerID){
    sets(page:1, perPage:50){
      nodes{ 
        winnerId,
        slots{
          entrant {
            id,
            participants{
              player { id }
            }
          }
        }
      }
    }
  }
}
"""

SETS_QUERRY_VAR = {
  "PlayerID": 0
}