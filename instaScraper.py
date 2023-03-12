import instaloader
 
# Creating an instance of the Instaloader class
bot = instaloader.Instaloader()
#bot.login(user="Your_username",passwd="Your_password") #Use this code to log-in to your account.


def getBasicInfo(profileid):
    # Loading the profile from an Instagram handle
    profile = instaloader.Profile.from_username(bot.context, profileid)
    # print("Username: ", profile.username)
    # print("User ID: ", profile.userid)
    # print("Number of Posts: ", profile.mediacount)
    #print("Followers Count: ", profile.followers)
    # print("Following Count: ", profile.followees)
    # print("Bio: ", profile.biography)
    # print("External URL: ", profile.external_url)   
    # print('\n')
    return profile.followers
