def add_to_env(key, value, env_path=".env"):
    line = f"{key}={value}\n"
    with open(env_path, "a") as file:
        file.write(line)

ClientID = str(input("Enter Client ID: "))
ClientSecret = str(input("Enter Client Secret: "))
TrackFlag = str(input("Enter Track-Flag Name: "))
try:
    add_to_env("CLIENT_ID", ClientID)
    add_to_env("CLIENT_SECRET", ClientSecret)
    add_to_env("SPOTIPY_REDIRECT_URL", 'http://127.0.0.1:8888/callback')
    add_to_env("TrackFlag", TrackFlag)
    print("Tokens and track-flag added successfully")
except Exception as e:
    print("somthing went wrong! Try to strart anything from begining")
    print(f"Error: {e}")
