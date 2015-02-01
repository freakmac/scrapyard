import cache
import network
import scraper
import urllib

KICKASS_URL = 'http://kickass.so'

################################################################################
def movie(movie_info):
    return __search('category:{0} imdb:{1}'.format('movies', movie_info['imdb_id'][2:]))

################################################################################
def episode(show_info, episode_info):
    return __search('category:{0} {1} season:{2} episode:{3}'.format('tv', show_info['title'], episode_info['season_index'], episode_info['episode_index']))

################################################################################
def __search(query):
    magnet_infos = []

    rss_data = network.rss_get_cached_optional(KICKASS_URL + '/usearch/{0}'.format(urllib.quote(query)), expiration=cache.HOUR, params={ 'field': 'seeders', 'sorder': 'desc', 'rss': '1' })
    if rss_data:
        for rss_item in rss_data.entries:
            magnet_infos.append(scraper.Magnet(rss_item.torrent_magneturi, rss_item.title, int(rss_item.torrent_seeds), int(rss_item.torrent_peers)))

    return magnet_infos