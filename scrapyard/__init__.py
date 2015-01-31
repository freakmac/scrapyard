#import cache
#import eztv
#import functools
#mport kickass
#import scraper
import trakt
#import utils
#import yts

################################################################################
# Common
################################################################################
# def __populate_magnets(providers, func):
#     provider_magnet_lists = utils.mt_map(func, providers)

#     magnets     = []
#     info_hashes = set()

#     for provider_magnet_list in provider_magnet_lists:
#         for magnet in provider_magnet_list:
#             if magnet.info_hash not in info_hashes:
#                 magnets.append(magnet)
#                 info_hashes.add(magnet.info_hash)

#     scraper.scrape_magnets(magnets, timeout=1)
#     magnets = sorted(magnets, key=lambda magnet: magnet.seeds, reverse=True)
#     magnets = [{'link': magnet.link, 'title': magnet.title, 'seeds': magnet.seeds, 'peers': magnet.peers } for magnet in magnets]

#     return magnets

################################################################################
# Movies
################################################################################
def movies_popular(page, limit):
    return trakt.movies_popular(page, limit)

# ################################################################################
def movies_trending(page, limit):
    return trakt.movies_trending(page, limit)

# ################################################################################
# def movies_search(query):
#     return trakt.movies_search(query)

# ################################################################################
# def movie(trakt_slug):
#     movie_info            = trakt.movie(trakt_slug, people_needed=True)
#     movie_info['magnets'] = cache.optional(__movie_magnets, expiration=cache.HOUR)([ kickass, yts ], movie_info)
#     return movie_info

# ################################################################################
# def __movie_magnets(providers, movie_info):
#     return __populate_magnets(providers, functools.partial(lambda module, movie_info: module.movie(movie_info), movie_info=movie_info))

################################################################################
# Shows
################################################################################
# def show(trakt_slug):
#     show_info = trakt.show(trakt_slug, seasons_needed=True)
#     return show_info

# ################################################################################
# def show_season(trakt_slug, season_index):
#     season_info = trakt.show_season(trakt_slug, season_index)
#     return season_info

# ################################################################################
# def show_episode(trakt_slug, season_index, episode_index):
#     show_info               = trakt.show(trakt_slug)
#     episode_info            = trakt.show_episode(trakt_slug, season_index, episode_index)
#     episode_info['magnets'] = cache.optional(__show_episode_magnets, expiration=cache.HOUR)([ eztv, kickass ], show_info, episode_info)
#     return episode_info

# ################################################################################
# def __show_episode_magnets(providers, show_info, episode_info):
#     return __populate_magnets(providers, functools.partial(lambda module, show_info, episode_info: module.episode(show_info, episode_info), show_info=show_info, episode_info=episode_info))

# ################################################################################
# def shows_popular(page, limit):
#     return trakt.shows_popular(page, limit)

# ################################################################################
# def shows_trending(page, limit):
#     return trakt.shows_trending(page, limit)

# ################################################################################
# def shows_search(query):
#     return trakt.shows_search(query)