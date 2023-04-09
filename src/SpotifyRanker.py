# Imports
import requests
import argparse

# Spotify API Keys
CLIENT_ID     = "3271009f09f948e0b6ac1e333dae3b03"
CLIENT_SECRET = "441ff81babc9436ba7bce004685d8f6b"

# Sorts Lists Based On User Preference
def merge_sort(list):
    # base case: if the list has fewer than 2 elements, it is already sorted
    if len(list) < 2:
        return list

    # split the list into two halves
    mid = len(list) // 2
    left = list[:mid]
    right = list[mid:]

    # recursive calls to merge_sort on the two halves
    left = merge_sort(left)
    right = merge_sort(right)

    # initialize the merged list and the indices for the left and right lists
    merged = []
    i = 0
    j = 0

    # while both lists have elements remaining
    while i < len(left) and j < len(right):
        # compare the current elements of the left and right lists
        while(1):
            print("[INFO] Which Song Do You Prefer: (1) {}, Or (2) {}?".format(left[i], right[j]))
            response = input()

            # if the user selects the left element, append it to the merged list and increment the left index
            if response == "1":
                merged.append(left[i])
                i += 1
                break

            # if the user selects the right element, append it to the merged list and increment the right index
            elif response == "2":
                merged.append(right[j])
                j += 1
                break
        
            else:
                print("[WARN] Please Type Either 1 Or 2 To Indicate Your Preference.")

    # append the remaining elements of the left list, if any, to the merged list
    merged.extend(left[i:])

    # append the remaining elements of the right list, if any, to the merged list
    merged.extend(right[j:])

    # return the merged and sorted list
    return merged

# Returns A List Of A Given Artists Tracks
def get_tracks(ARTIST_NAME):
    # Use the client ID and secret to authenticate and get an access token
    auth_response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "client_credentials"
    }, auth=(CLIENT_ID, CLIENT_SECRET))
    access_token = auth_response.json()["access_token"]

    # Use the access token to search for the artist
    search_response = requests.get("https://api.spotify.com/v1/search", params={
        "q": ARTIST_NAME,
        "type": "artist"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    # Get the artist ID from the search results
    ARTIST_ID = search_response.json()["artists"]["items"][0]["id"]

    # Use the artist ID to get the artist's albums
    albums_response = requests.get(f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums", params={
        "include_groups": "album,single",
        "limit": 50
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    # Get the IDs of the artist's albums
    album_ids = [album["id"] for album in albums_response.json()["items"]]

    # For each album, use the album ID to get the tracks
    tracks = []
    for album_id in album_ids:
        tracks_response = requests.get(f"https://api.spotify.com/v1/albums/{album_id}/tracks", params={
            "limit": 50
        }, headers={
            "Authorization": f"Bearer {access_token}"
        })

        # # Add the tracks to the list
        # tracks.extend(tracks_response.json()["items"])

        # Add the names of the tracks to the list
        tracks.extend([track["name"] for track in tracks_response.json()["items"]])

    return tracks

# Returns A List Of A Given Artists Albums
def get_albums(ARTIST_NAME):
    # Use the client ID and secret to authenticate and get an access token
    auth_response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "client_credentials"
    }, auth=(CLIENT_ID, CLIENT_SECRET))
    access_token = auth_response.json()["access_token"]

    # Use the access token to search for the artist
    search_response = requests.get("https://api.spotify.com/v1/search", params={
        "q": ARTIST_NAME,
        "type": "artist"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    # Get the artist ID from the search results
    ARTIST_ID = search_response.json()["artists"]["items"][0]["id"]

    # Use the artist ID to get the artist's albums
    albums_response = requests.get(f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums", params={
        "include_groups": "album,single",
        "limit": 50
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    # Get the IDs of the artist's albums
    albums = [album["name"] for album in albums_response.json()["items"]]
    return albums

def main(ARTIST_NAME, mode):
    # Get Data & Run Algorithm
    if mode == 0:
        print("[INFO] Attempting To Fetch Tracks For The Artist '{}'".format(ARTIST_NAME))
        data = list(set(get_tracks(ARTIST_NAME)))
    else:
        print("[INFO] Attempting To Fetch Albums For The Artist '{}'".format(ARTIST_NAME))
        data = list(set(get_albums(ARTIST_NAME)))
    sortedData = merge_sort(data)

    # Save Result
    with open("{} Ranking.txt".format(ARTIST_NAME), 'w') as file:
        # Write Title
        file.write("{} Ranking:\n\n".format(ARTIST_NAME))

        # Write Each Item In The List To A New Line
        for i, item in zip(range(1, len(sortedData) + 1), sortedData):
            file.write("{}: {}\n".format(i, item))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank An Artists Albums/Tracks")

    parser.add_argument("-a", "--artist", help="Specify Artist", type=str)
    parser.add_argument("-l", "--album", help="Rank Albums", action="store_true")
    parser.add_argument("-t", "--track", help="Rank Albums", action="store_true")

    args = parser.parse_args()

    if((args.album and args.track) or (not args.album and not args.track)):
        print("[ERROR] Invalid Combination Of Mode Flags")
        exit()

    if(args.artist == ""):
        print("[ERROR] No Artist Specified")
        exit()

    # Run Program
    main(args.artist, 0 if args.track else 1)