import base64
import json
import sys
import re
import requests

# if you put this into a subdirectory of scrapers, and pycommon is in scraper
sys.path.insert(0,'..')

try:
    import py_common.config as config
    import py_common.graphql as graphql
    import py_common.log as log
except ModuleNotFoundError:
    print("You need to download the folder 'py_common' from the community repo! (CommunityScrapers/tree/master/scrapers/py_common)", file=sys.stderr)
    sys.exit()

'''  This script runs a graphql function to copy scene info from another Stash scene.
     '''

def call_graphql(query, variables=None):
    return graphql.callGraphQL(query, variables)

FRAGMENT = json.loads(sys.stdin.read())
#SCENE_TO = FRAGMENT.get("id")
SCENE_FROM_URL = FRAGMENT.get("url")
if SCENE_FROM_URL is None:
  log.info("URL should be the local url for a scene or _just_ the scene number")
  sys.exit()
if SCENE_FROM_URL.isnumeric():
  # we're good
  SCENE_FROM_ID = SCENE_FROM_URL
else:
  # extract the scene id from url
  sceneIDextract = re.match(r"^http.*/scenes/([0-9]+)", SCENE_FROM_URL)
  if sceneIDextract is None:
     log.info("URL should be the local url for a scene or _just_ the scene number")
     sys.exit()
  SCENE_FROM_ID = sceneIDextract.group(1)
if SCENE_FROM_ID.isnumeric():
  # scene = graphql.getScene(SCENE_TO)
  scenefrom = graphql.getScene(SCENE_FROM_ID)
  # log.info(scene)
  # log.info(scenefrom)

  # FYI this is overkill but it does pass most of the important bits onward
  # bug reports welcomed

#adapted from Belley code, but no longer passes whole Movie object, just id
  if scenefrom.get("movies"):
    log.info(scenefrom["movies"])
    movie_list = []
    for movie in scenefrom["movies"]:
        if movie["movie"]:
             newmovie = {}
             newmovie["stored_id"] = movie["movie"]["id"]
             movie_list.append(newmovie)
    scenefrom["movies"] = movie_list

# unneeded?
#  if scenefrom.get("stash_ids"):
#     scenefrom["remote_site_id"] = scenefrom["stash_ids"][0]["stash_id"]
#     del scenefrom["stash_ids"]

#kudos to Belley for this code,
  api_key = ""
  if config.STASH.get("api_key"):
     api_key = config.STASH["api_key"]
  img_data = base64.b64encode(requests.get(scenefrom["paths"]["screenshot"], headers={"ApiKey": api_key}, timeout=10).content)
  scenefrom["image"] = "data:image/jpeg;base64," + img_data.decode('utf-8')

  print(json.dumps(scenefrom))
else:
  log.info("URL should be the local url for a scene or _just_ the scene number")
  sys.exit()
# Last Updated July 19, 2022
