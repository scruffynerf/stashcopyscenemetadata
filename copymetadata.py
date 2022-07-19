import json
import sys
import re

try:
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
if SCENE_FROM_URL.isnumeric():
  # we're good
  SCENE_FROM_ID = SCENE_FROM_URL
else:
  # extract the scene id from url
  sceneIDextract = re.match(r"^http.*/scenes/([0-9]+)", SCENE_FROM_URL)
  SCENE_FROM_ID = sceneIDextract.group(1)
if SCENE_FROM_ID.isnumeric():
  # scene = graphql.getScene(SCENE_TO)
  scenefrom = graphql.getScene(SCENE_FROM_ID)
  # log.info(scene)
  # log.info(scenefrom)
  # FYI this is overkill but it does pass most of the important bits onward
  # bug reports welcomed. 
  # I know movie info isn't passed right yet, nor thumbnail
  print(json.dumps(scenefrom))
else:
  log.info("URL should be the local url for a scene or _just_ the scene number")
  sys.exit()
# Last Updated July 19, 2022
