
HOST = "irc.twitch.tv"  # the Twitch IRC server
PORT = 6667  # always use port 6667!
NICK = "klime_bot"  # your Twitch username, lowercase
PASS = ""  # your Twitch OAuth token
selection = input("Enable League mode? : ")
CHAN = input("Enter the channel name: ")  # the channel you want to join
RATE = 20  # messages per second
RiotAPI = ""
TwitchAPI = ""
if selection == "y":
    playerName = input("Enter the IGN: ")
playerRegion = "EUW1"
playerQue = "RANKED_SOLO_5x5"
allRunes = {7000: 'Template', 8004: 'The Brazen Perfect', 8005: 'Press the Attack', 8006: 'The Eternal Champion', 8007: 'The Savant', 8008: 'Lethal Tempo',
            8009: 'Presence of Mind', 8014: 'Coup de Grace', 8016: 'The Merciless Elite', 8017: 'Cut Down', 8021: 'Fleet Footwork', 8105: 'Relentless Hunter',
            8109: 'The Ingenious Hunter', 8112: 'Electrocute', 8114: 'The Immortal Butcher', 8115: 'The Aether Blade', 8120: 'Ghost Poro', 8124: 'Predator',
            8126: 'Cheap Shot', 8127: 'The Glorious Executioner', 8128: 'Dark Harvest', 8134: 'Ingenious Hunter', 8135: 'Ravenous Hunter', 8136: 'Zombie Ward',
            8138: 'Eyeball Collection', 8139: 'Taste of Blood', 8143: 'Sudden Impact', 8205: 'The Incontestable Spellslinger', 8207: 'The Cryptic', 8208: 'The Ancient One',
            8210: 'Transcendence', 8214: 'Summon Aery', 8220: 'The Calamity', 8224: 'Nullifying Orb', 8226: 'Manaflow Band', 8229: 'Arcane Comet', 8230: 'Phase Rush',
            8232: 'Waterwalking', 8233: 'Absolute Focus', 8234: 'Celerity', 8236: 'Gathering Storm', 8237: 'Scorch', 8242: 'Unflinching', 8243: 'The Ultimate Hat',
            8299: 'Last Stand', 8304: 'Magical Footwear', 8306: 'Hextech Flashtraption', 8313: 'Perfect Timing', 8316: 'Minion Dematerializer', 8318: 'The Ruthless Visionary',
            8319: 'The Stargazer', 8320: 'The Timeless', 8321: "Future's Market", 8326: 'Unsealed Spellbook', 8339: 'Celestial Body', 8344: 'The Virtuoso', 8345: 'Biscuit Delivery',
            8347: 'Cosmic Insight', 8351: 'Glacial Augment', 8359: 'Kleptomancy', 8410: 'Approach Velocity', 8414: 'The Imperious Behemoth', 8415: 'The Arcane Colossus',
            8416: 'The Enlightened Titan', 8429: 'Conditioning', 8430: 'Iron Skin', 8435: 'Mirror Shell', 8437: 'Grasp of the Undying', 8439: 'Aftershock', 8444: 'Second Wind',
            8446: 'Demolish', 8451: 'Overgrowth', 8453: 'Revitalize', 8454: 'The Leviathan', 8463: 'Font of Life', 8465: 'Guardian', 9101: 'Overheal', 9103: 'Legend: Bloodline', 9104: 'Legend: Alacrity', 9105: 'Legend: Tenacity', 9111: 'Triumph'}
