import cache
# import datetime
# import dateutil.parser
# import dateutil.tz
import network
import utils

TRAKT_URL     = 'https://api.trakt.tv'
TRAKT_HEADERS = { 'content-type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': '64cf92c702ff753cc14a6d421824efcd32f22058f79bf6d637fa92e23229f35f' }

################################################################################
# Movies
################################################################################
def movie(trakt_slug, people_needed=False):
    if trakt_slug:
        json_data = network.json_get_cached_mandatory(TRAKT_URL + '/movies/' + trakt_slug, expiration=cache.WEEK, params={ 'extended': 'full,images' }, headers=TRAKT_HEADERS)
        if json_data:
            result =    {
                            'trakt_slug':       json_data['ids']['slug'],
                            'imdb_id':          json_data['ids']['imdb'],
                            'title':            json_data['title'],
                            'year':             json_data['year'],
                            'overview':         json_data['overview'],
                            'tagline':          json_data['tagline'],
                            'thumb':            json_data['images']['poster']['full'],
                            'art':              json_data['images']['fanart']['full'],
                            'runtime':          (json_data['runtime'] * 60 * 1000) if json_data['runtime'] else 0,
                            'genres':           json_data['genres'],
                            'rating':           json_data['rating'],
                            'released':         json_data['released'],
                            'certification':    json_data['certification']
                        }

            if people_needed:
                result['people'] = { 'cast': [], 'crew': { 'directing': [], 'production': [], 'writing': [] } }
                json_data = network.json_get_cached_mandatory(TRAKT_URL + '/movies/' + trakt_slug + '/people', expiration=cache.WEEK, params={ 'extended': 'images' }, headers=TRAKT_HEADERS)
                if json_data:
                    for json_item in json_data['cast']:
                        result['people']['cast'].append({
                                                            'name':         json_item['person']['name'],
                                                            'headshot':     json_item['person']['images']['headshot']['full'],
                                                            'character':    json_item['character']
                                                        })

                    for json_item in json_data['crew']['directing']:
                        result['people']['crew']['directing'].append({
                                                                        'name':     json_item['person']['name'],
                                                                        'headshot': json_item['person']['images']['headshot']['full'],
                                                                        'job':      json_item['job']
                                                                     })

                    for json_item in json_data['crew']['production']:
                        result['people']['crew']['production'].append({
                                                                        'name':     json_item['person']['name'],
                                                                        'headshot': json_item['person']['images']['headshot']['full'],
                                                                        'job':      json_item['job']
                                                                      })

                    for json_item in json_data['crew']['writing']:
                        result['people']['crew']['writing'].append({
                                                                        'name':     json_item['person']['name'],
                                                                        'headshot': json_item['person']['images']['headshot']['full'],
                                                                        'job':      json_item['job']
                                                                    })

            return result

################################################################################
def movies_popular(page=1, limit=10):
    json_data = network.json_get_cached_mandatory(TRAKT_URL + '/movies/popular', expiration=cache.DAY, params={ 'page': page, 'limit': limit}, headers=TRAKT_HEADERS)
    if json_data:
        return __movie_list(json_data)

# ################################################################################
def movies_trending(page=1, limit=10):
    json_data = network.json_get_cached_mandatory(TRAKT_URL + '/movies/trending', expiration=cache.HOUR, params={ 'page': page, 'limit': limit}, headers=TRAKT_HEADERS)
    if json_data:
        return __movie_list(json_data)

# ################################################################################
# def movies_search(query):
#     json_data = network.json_get('{0}/{1}'.format(TRAKT_URL, 'search'), params={ 'query': query, 'type': 'movie' }, headers=TRAKT_HEADERS)
#     if json_data:
#         return __movie_list(json_data)

# ################################################################################
def __movie_list(json_data):
    movie_infos = []
    if json_data:
        movie_infos = utils.mt_map(lambda json_item: movie(json_item['movie']['ids']['slug'] if 'movie' in json_item else json_item['ids']['slug']), json_data)
    return { 'movies': movie_infos }

################################################################################
# Shows
################################################################################
# def show(trakt_slug, seasons_needed=False):
#     if trakt_slug:
#         json_data = network.json_get_cached_mandatory(TRAKT_URL + '/shows/' + trakt_slug, expiration=cache.WEEK, params={ 'extended': 'full,images' }, headers=TRAKT_HEADERS)
#         if json_data:
#             result =    {
#                             'trakt_slug':       json_data['ids']['slug'],
#                             'imdb_id':          json_data['ids']['imdb'],
#                             'title':            json_data['title'],
#                             'year':             json_data['year'],
#                             'overview':         json_data['overview'],
#                             'studio':           json_data['network'],
#                             'thumb':            json_data['images']['poster']['full'],
#                             'art':              json_data['images']['fanart']['full'],
#                             'runtime':          (json_data['runtime'] * 60 * 1000) if json_data['runtime'] else 0,
#                             'genres':           json_data['genres'],
#                             'rating':           json_data['rating'],
#                             'first_aired':      json_data['first_aired'],
#                             'certification':    json_data['certification']
#                         }

#             if seasons_needed:
#                 result['seasons'] = []
#                 json_data = network.json_get_cached_mandatory(TRAKT_URL + '/shows/' + trakt_slug + '/seasons', expiration=cache.WEEK, params={ 'extended': 'full,images' }, headers=TRAKT_HEADERS)
#                 if json_data:
#                     for json_item in json_data:
#                         if json_item['number'] > 0:
#                             result['seasons'].append({
#                                                         'show_title':       result['title'],
#                                                         'season_index':     json_item['number'],
#                                                         'title':            'Season {0}'.format(json_item['number']),
#                                                         'overview':         json_item['overview'],
#                                                         'episode_count':    json_item['episode_count'],
#                                                         'thumb':            json_item['images']['poster']['full'],
#                                                         'art':              result['art']
#                                                     })

#             return result

# ################################################################################
# def show_season(trakt_slug, season_index):
#     show_info = show(trakt_slug)
#     if show_info:
#         json_data = network.json_get_cached_mandatory(TRAKT_URL + '/shows/' + trakt_slug + '/seasons/' + str(season_index), expiration=cache.DAY, params={ 'extended': 'full,images' }, headers=TRAKT_HEADERS)
#         if json_data:
#             episode_infos = []
#             for json_item in json_data:
#                 if json_item['first_aired'] and datetime.datetime.now(dateutil.tz.tzutc()) > dateutil.parser.parse(json_item['first_aired']):
#                     episode_infos.append({
#                                             'show_title':       show_info['title'],
#                                             'season_index':     json_item['season'],
#                                             'episode_index':    json_item['number'],
#                                             'title':            json_item['title'],
#                                             'thumb':            json_item['images']['screenshot']['full'],
#                                             'art':              json_item['images']['screenshot']['full'],
#                                             'overview':         json_item['overview'],
#                                             'rating':           json_item['rating'],
#                                             'first_aired':      json_item['first_aired'],
#                                          })

#             return {'episodes': episode_infos }

# ################################################################################
# def show_episode(trakt_slug, season_index, episode_index):
#     episode_infos = show_season(trakt_slug, season_index)
#     if episode_infos:
#         episode_info = next((episode_info for episode_info in episode_infos['episodes'] if episode_info['episode_index'] == episode_index), None)
#         return episode_info

# ################################################################################
# def shows_popular(page=1, limit=10):
#     json_data = network.json_get_cached_mandatory(TRAKT_URL + '/shows/popular', expiration=cache.DAY, params={ 'page': page, 'limit': limit}, headers=TRAKT_HEADERS)
#     if json_data:
#         return __show_list(json_data)

# ################################################################################
# def shows_trending(page=1, limit=10):
#     json_data = network.json_get_cached_mandatory(TRAKT_URL + '/shows/trending', expiration=cache.HOUR, params={ 'page': page, 'limit': limit}, headers=TRAKT_HEADERS)
#     if json_data:
#         return __show_list(json_data)

# ################################################################################
# def shows_search(query):
#     json_data = network.json_get(TRAKT_URL + '/search', params={ 'query': query, 'type': 'show' }, headers=TRAKT_HEADERS)
#     if json_data:
#         return __show_list(json_data)

# ################################################################################
# def __show_list(json_data):
#     show_infos = []
#     if json_data:
#         show_infos = utils.mt_map(lambda json_item: show(json_item['show']['ids']['slug'] if 'show' in json_item else json_item['ids']['slug']), json_data)
#     return { 'shows': show_infos }