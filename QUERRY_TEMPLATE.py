
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
      url(relative:false)
    }
  }
}
"""

TOURNAMENT_QUERRY_VAR = {
  "TournamentID": 0
}