


# BOT-SPECIFIC:

botToken = "" #token of the bot

commanderRoleID = "" #id of the role commanders have

easterEggs = {
"example":"Example response"
"freeshavakadoo":"You pronounced that wrong."
} #easter egg message dict. formatting: "call":"response". Do not use capitalization in the call! Remove the contents of the dict to disable easter eggs



# DEFAULT-SETTINGS:

silencedRoleName = "Silenced" #name of the silenced role

botPrefix = "s!" #command prefix

unsilenceTime = 600 #integer or float in seconds for how long until a user is unsilenced

msgCache = "msgs.txt" #name of file that holds messages

deathCache = "deaths.txt" #name of file that holds death counts



# DON'T TOUCH:

commandList = ["s!clear", "s!upload", "s!userRoles", "s!deaths"] #a list of the bot's commands so command calls don't get stored (don't touch this unless you know what you're doing)
