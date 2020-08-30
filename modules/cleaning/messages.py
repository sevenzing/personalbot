from modules.common.constants import BOT_ADMIN_ALIAS

CHANGE_BUILDING_MESSAGE = '🏣 Please, select your building\n'

# | Number of building
QUERY_SELECTED = '☑️ The %s building selected'

# | 'today' or 'tomorrow'  
CLEANING_NOTIFICATION = '❗ Hello! Do not forget about cleaning day %s'

# | Number of building, days left, day number, month name
NEXT_CLEANING = '🧹 Your building is %s, so the next cleaning day will be in *%d days*, on the *%s of %s*.\n'

NEXT_CLEANING_ERROR = '🚫 *Failed* to get your cleaning day. Write to @%s to fix this error' % BOT_ADMIN_ALIAS

HAVE_NOT_BUILDING = "🤷 You haven't chosen a building yet. \n/setbuilding"

BUTTON_ON_CLEANING = '%s On cleaning %s'
BUTTON_BEFORE_CLEANING = '%s Before cleaning %s'

ON_CMD_SETREMINDER = '⏰ Select the desired day and time of notification. \n\n\'❌\' means no notification on this day\n\'✅\' means notify about cleaning on this day'
