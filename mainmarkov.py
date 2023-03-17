
import base64
from requests import post, get
import json
import lyricsgenius

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result= get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]
    
def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()   
result = search_for_artist(token, "Taylor Swift")
artist_id = result  ["id"] 
songs = get_songs_by_artists(token, artist_id)
songs_list = []

    
 
for song in songs:
    if '(' in song['name']:
       ix = song['name'].find('(')
       songs_list.append(song['name'][:ix-1])
       
    else:
        songs_list.append(song['name'])
    
    
API_KEY = "wWRTQycAcCbVEpIqGfnFd_mEzvWOVyq_as6nOpADeSD_XQ4QATH-gObWyLZI-Yu3"
  

genius = lyricsgenius.Genius(access_token=API_KEY)
genius.verbose = False

# Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.remove_section_headers = True
artist = genius.search_artist(artist_name = "Taylor Swift", max_songs = 1, sort = "title")

        
with open("taylorlyrics.txt","w") as lyr:
    for song in songs_list:
        curr_song = artist.song(song_name=song)
        lyrics = curr_song.lyrics
        ix = lyrics.find("Lyrics")
        for l in lyrics[ix+6:-7]:
            try:
                l = l.lower()
                if l in list('\n qwertyuioplkjhgfdsazxcvbnm'):
                    lyr.write(l)
            except UnicodeEncodeError:
                continue
        
                   