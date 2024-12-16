import os
from copy import copy

import pygame
import ujson

from scripts.game_structure.game_essentials import game


class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None

        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")

    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"

                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )

                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite

                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart  # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50  # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        for x in [
            'lineart', 'lineartdf', 'lineartdead',
            'eyes', 'eyes2', 'skin',
            'scars', 'missingscars',
            'medcatherbs', 'wild',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars',
            'singlecolours', 'speckledcolours', 'tabbycolours', 'bengalcolours', 'marbledcolours',
            'rosettecolours', 'smokecolours', 'tickedcolours', 'mackerelcolours', 'classiccolours',
            'sokokecolours', 'agouticolours', 'singlestripecolours', 'maskedcolours',
            'shadersnewwhite', 'lightingnew',
            'whitepatches', 'tortiepatchesmasks',
            'fademask', 'fadestarclan', 'fadedarkforest',
            'symbols'
        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        # Define eye colors
        eye_colors = [
            # base game: 1-21
            
            # row one
            # ['1', '2', '3', '4', '5',
            # '6', '7', '8', '9', '10',
            # '11', '12', '13', '14', '15']
            # yellow, amber, hazel, pale green, green,
            # blue, dark blue, grey, cyan, emerald,
            # heather blue, sunlit ice, copper, sage, cobalt
            ['YELLOW', 'AMBER', 'HAZEL', 'PALE GREEN', 'GREEN',
             'BLUE', 'DARK BLUE', 'GREY', 'CYAN', 'EMERALD',
             'HEATHER BLUE', 'SUNLIT ICE', 'COPPER', 'SAGE', 'COBALT'],
            
            # row two
            # ['16', '17', '18', '19', '20',
            # '21', '22', '23', '24', '25',
            # '26', '27', '28', '29', '30']
            # pale blue, bronze, silver, pale yellow, gold,
            # green-yellow, chestnut, rime, rose quartz, twilight,
            # peach, boggy rain, tropical sunrise, ocean sunrise, headlights
            ['PALE BLUE', 'BRONZE', 'SILVER', 'PALE YELLOW', 'GOLD',
             'GREEN-YELLOW', 'CHESTNUT', 'RIME', 'ROSE QUARTZ', 'TWILIGHT',
             'PEACH', 'BOGGY RAIN', 'TROPICAL SUNRISE', 'OCEAN SUNRISE', 'HEADLIGHTS'],
            
            # row three
            # ['31', '32', '33', '34', '35',
            # '36', '37', '38', '39', '40',
            # '41', '42', '43', '44', '45']
            # purple, pink, red, orange, pansy,
            # budgie, ghost, dust, silver-blue, sapphire,
            # crystal, stone, magenta, sunlight, lime
            ['PURPLE', 'PINK', 'RED', 'ORANGE', 'PANSY',
             'BUDGIE', 'GHOST', 'DUST', 'SILVER-BLUE', 'SAPPHIRE',
             'CRYSTAL', 'STONE', 'MAGENTA', 'SUNLIGHT', 'LIME'],
            
            # row four
            # ['46', '47', '48', '49', '50',
            # '51', '52', '53', '54', '55',
            # '56', '57', '58', '59', '60']
            # dirt, dusk, sprout, light turquoise, deep purple,
            # lily of the incas, sky blue, tropical ocean, bright red, honey,
            # seaside, underbrush, dull purple, light pink, bone marrow
            ['DIRT', 'DUSK', 'SPROUT', 'LIGHT TURQUOISE', 'DEEP PURPLE',
             'LILY OF THE INCAS', 'SKY BLUE', 'TROPICAL OCEAN', 'BRIGHT RED', 'HONEY',
             'SEASIDE', 'UNDERBRUSH', 'DULL PURPLE', 'LIGHT PINK', 'BONE MARROW'],
            
            # row five
            # ['61', '62', '63', '64', '65',
            # '66', '67', '68', '69', '70',
            # '71', '72', '73', '74', '75']
            # pale brown, bog moss, deep magenta, cotton candy, crocodile
            # virdian, withered plant, ember, sunlit dusk, dirt clump
            # dry soil, brown, drowned ghost, dazzling sunrise, pale teal
            ['PALE BROWN', 'BOG MOSS', 'DEEP MAGENTA', 'COTTON CANDY', 'CROCODILE',
             'VIRDIAN', 'WITHERED PLANT', 'EMBER', 'SUNLIT DUSK', 'DIRT CLUMP',
             'DRY SOIL', 'BROWN', 'DROWNED GHOST', 'DAZZLING SUNRISE', 'PALE TEAL'],
            
            # row six
            # ['76', '77', '78', '79', '80',
            # '81', '82', '83', '84', '84',
            # '86', '87', '88', '89', '90']
            # amethyst, spring, storm cloud, dark tan, dark red
            # cherry blossom, pale gold, night clouds, pastel green, pumpkin
            # cyber gaze, mixed blues, soft night, sunburst, turquoise
            ['AMETHYST', 'SPRING', 'STORM CLOUD', 'DARK TAN', 'DARK RED',
             'CHERRY BLOSSOM', 'PALE GOLD', 'NIGHT CLOUDS', 'PASTEL GREEN', 'PUMPKIN',
             'CYBER GAZE', 'MIXED BLUES', 'SOFT NIGHT', 'SUNBURST', 'TURQUOISE'],
            
            # row seven
            # ['91', '92', '93', '94', '95', '96',
            # '97', '98', '99', '100',
            # '101', '102', '103', '104', '105']
            # burning flame, early dusk, mud, bright turquoise, wolf,
            # baby blue, seafoam, early sunrise, pastel skies, sparkling grape,
            # name me! (101), pond, fossil, azure, autumn
            ['BURNING FLAME', 'EARLY DUSK', 'MUD', 'BRIGHT TURQUOISE', 'WOLF',
            'BABY BLUE', 'SEAFOAM', 'EARLY SUNRISE', 'PASTEL SKIES', 'SPARKLING GRAPE',
            'NAME ME! (101)', 'POND', 'FOSSIL', 'AZURE', 'AUTUMN'],
            
            # row eight
            # ['106', '107', '108', '109', '110',
            # '111', '112', '113', '114', '115',
            # '116', '117', '118', '119', '120']
            # fire salamander, upsidedown magenta, purple glossy starling, turtle shell, verbena
            # name me! (111), bog water, pink pansy, upsidedown purple, slate
            # lush pond, bluejay, dusk clouds, pansy petal, budding leaves
            ['FIRE SALAMANDER', 'UPSIDEDOWN MAGENTA', 'PURPLE GLOSSY STARLING', 'TURTLE SHELL', 'VERBENA',
            'NAME ME! (111)', 'BOG WATER', 'PINK PANSY', 'UPSIDEDOWN PURPLE', 'SLATE',
            'LUSH POND', 'BLUEJAY', 'DUSK CLOUDS', 'PANSY PETAL', 'BUDDING LEAVES'],
            
            # row nine
            # ['121', '122', '123', '124', '125',
            # '126', '127', '128', '129', '130',
            # '131', '132', '133', '134', '135']
            # lavender garden, rouge, name me! (123), muddy ice, drying clay
            # scarlet gum, spring leaves, name me! (128), drying leaves, monte carlo
            # early sunrise, name me! (132), vegetated peat, name me! (134), name me! (135)
            ['LAVENDER GARDEN', 'ROUGE', 'NAME ME! (123)', 'MUDDY ICE', 'DRYING CLAY',
            'SCARLET GUM', 'SPRING LEAVES', 'NAME ME! (128)', 'DRYING LEAVES', 'MONTE CARLO',
            'EARLY SUNRISE', 'NAME ME! (132)', 'VEGETATED PEAT', 'NAME ME! (135)', 'NAME ME! (135)'],
            
            # row ten
            # ['136', '137', '138', '139', '140',
            # '141', '142', '143', '144', '145',
            # '146', '147', '148', '149', '150']
            # pastel clouds, wetlands, apple core, mountainous, angelic
            # woodpecker, red apple, name me! (143), sky-high flame, pink opal
            # early morning, name me! (147), blue-green water, reversed indigo, name me! (150)
            ['PASTEL CLOUDS', 'WETLANDS', 'APPLE CORE', 'MOUNTAINOUS', 'ANGELIC',
            'WOODPECKER', 'RED APPLE', 'NAME ME! (143)', 'SKY-HIGH FLAME', 'PINK OPAL',
            'EARLY MORNING', 'NAME ME! (147)', 'BLUE-GREEN WATER', 'REVERSED INDIGO', 'NAME ME! (150)'],
            
            # row eleven
            # ['151', '152', '153', '154', '155',
            # '156', '157', '158', '159', '160',
            # '161', '162', '163', '164', '165']
            # medium vermilion, water lettuce, manicure, name me! (154), light hazel,
            # night sea, name me! (157), camelot, muddy fen, fen,
            # name me! (161), sunset red, rose bud, name me! (164), pansy petals
            ['MEDIUM VERMILLION', 'WATER LETTUCE', 'MANICURE', 'NAME ME! (154)', 'LIGHT HAZEL',
            'NIGHT SEA', 'NAME ME! (157)', 'CAMELOT', 'MUDDY FEN', 'FEN',
            'NAME ME! (161)', 'SUNSET RED', 'ROSE BUD', 'NAME ME! (164)', 'PANSY PETALS'],
            
            # row twelve
            # ['166', '167', '168', '169', '170',
            # '171', '172', '173', '174', '175',
            # '176', '177', '178', '179', '180']
            # name me! (166), name me! (167), name me! (168), icy evergreen, name me! (170)
            # name me! (171), name me! (172), name me! (173), deep lilac, name me! (175)
            # candlelight flame, sunlit lagoon, night meadow, imperial sword, baby blue blanket
            ['NAME ME! (166)', 'NAME ME! (167)', 'NAME ME! (168)', 'ICY EVERGREEN', 'NAME ME! (170)',
            'NAME ME! (171)', 'NAME ME! (172)', 'NAME ME! (173)', 'DEEP LILAC', 'NAME ME! (175)',
            'CANDLELIGHT FLAME', 'SUNLIT LAGOON', 'NIGHT MEADOW', 'IMPERIAL SWORD', 'BABY BLUE BLANKET'],
            
            # row thirteen
            # ['181', '182', '183', '184', '185',
            # '186', '187', '188', '189', '190',
            # '191', '192', '193', '194', '195']
            # rainforest green, red-backed salamander, moss green, gentle glow, smashed mulberry
            # pastel purple clouds, cornflower, name me! (188), sakura, sunlit river
            # midnight sea, name me! (192), TikTok, raspberry blues, purple poison
            ['RAINFOREST GREEN', 'RED-BACKED SALAMANDER', 'MOSS GREEN', 'GENTLE GLOW', 'SMASHED MULBERRY',
            'PASTEL PURPLE CLOUDS', 'CORNFLOWER', 'NAME ME! (188)', 'SAKURA', 'SUNLIT RIVER',
            'MIDNIGHT SEA', 'NAME ME! (192)', 'TIKTOK', 'RASPBERRY BLUES', 'PURPLE POISON'],
            
            # row fourteen
            # ['196', '197', '198', '199', '200',
            # '201', '202', '203', '204', '205',
            # '206', '207', '208', '209', '210']
            # unnamed: 4 -- 200, 206, 207, 210
            # squash harvest, flamingo feather, swamp shack, ptilotus, name me! (200)
            # wild rice, river orchid, demonic glow, slate blue, enchanted meadow
            # name me! (206), name me! (207), nighttime seafoam, broccoli, name me! (210)
            ['SQUASH HARVEST', 'FLAMINGO FEATHER', 'SWAMP SHACK', 'PTILOTUS', 'NAME ME! (200)',
            'WILD RICE', 'RIVER ORCHID', 'DEMONIC GLOW', 'SLATE BLUE', 'ENCHANTED MEADOW',
            'NAME ME! (206)', 'NAME ME! (207)', 'NIGHTTIME SEAFOAM', 'BROCCOLI', 'NAME ME! (210)'],
            
            # row fifteen
            # ['211', '212', '213', '214', '215',
            # '216', '217', '218', '219', '220',
            # '221', '222', '223', '224', '225']
            # unnamed: 1 -- 223
            # black widow, demonic pink, purple illusion, red ranunculus, infernal flame
            # pelorous, flame, purple anemone, grapevine, velvet wine
            # wolf coat, cranberry bean, name me! (223), seafoam green, reversed flame
            ['BLACK WIDOW', 'DEMONIC PINK', 'PURPLE ILLUSION', 'RED RANUCULUS', 'INFERNAL FLAME',
            'PELOROUS', 'FLAME', 'PURPLE ANEMONE', 'GRAPEVINE', 'VELVET WINE',
            'WOLF COAT', 'CRANBERRY BEAN', 'NAME ME! (223)', 'SEAFOAM GREEN', 'REVERSED FLAME'],
            
            # row sixteen
            # ['226', '227', '228', '229', '230',
            # '231', '232', '233', '234', '235',
            # '236', '237', '238', '239', '240']
            # unnamed: 3 -- 228, 232, 236
            # mystical leather book, dark hailstorm, name me! (228), young pumpkin, dancing fairy
            # seaside, name me! (232), crimson steel, wonderberry, lungwort
            # name me! (236), red sunflower, reef, night lantern, sunny droplet
            ['MYSTICAL LEATHER BOOK', 'DARK HAILSTORM', 'NAME ME! (228)', 'YOUNG PUMPKIN', 'DANCING FAIRY',
            'SEASIDE', 'NAME ME! (232)', 'CRIMSON STEEL', 'WONDERBERRY', 'LUNGWORT',
            'NAME ME! (236)', 'RED SUNFLOWER', 'REEF', 'NIGHT LANTERN', 'SUNNY DROPLET'],
            
            # row seventeen
            # ['241', '242', '243', '244', '245',
            # '246', '247', '248', '249', '250',
            # '251', '252', '253', '254', '255']
            # unnamed: 3 -- 250, 253, 255
            # cosmic explorer, blanket flower, ocean abyss, combustion, skydiver
            # blackberry lemonade, royal peacock, black cherry, hot summer day, name me! (250)
            # red dahlia, nightshade bush, name me! (253), frozen light, name me! (255)
            ['COSMIC EXPLORER', 'BLANKET FLOWER', 'OCEAN ABYSS', 'COMBUSTION', 'SKYDIVER',
            'BLACKBERRY LEMONADE', 'ROYAL PEACOCK', 'BLACK CHERRY', 'HOT SUMMER DAY', 'NAME ME! (250)',
            'RED DAHLIA', 'NIGHTSHADE BUSH', 'NAME ME! (253)', 'FROZEN LIGHT', 'NAME ME! (255)'],
            
            # row eighteen
            # ['256', '257', '258', '259', '260',
            # '261', '262', '263', '264', '265',
            # unnamed: 1 -- 258
            # '266', '267', '268', '269', '270']
            # mystical midday, dulled purple, name me! (258), pastel sundown, enchanter's pink
            # plum pie, emerald tree, woodland firefly, morning brew, pink void
            # hazelnut, verdant leaf, kissable star, ghostly toad king, overgrown rose garden
            ['MYSTICAL MIDDAY', 'DULLED PURPLE', 'NAME ME! (258)', 'PASTEL SUNDOWN', 'ENCHANTERSPINK',
            'PLUM PIE', 'EMERALD TREE', 'WOODLAND FIREFLY', 'MORNING BREW', 'PINK VOID',
            'HAZELNUT', 'VERDANT LEAF', 'KISSABLE STAR', 'GHOSTLY TOAD KING', 'OVERGROWN ROSE GARDEN'],
            
            # row nineteen
            # ['271', '272', '273', '274', '275',
            # '276', '277', '278', '279', '280',
            # '281', '282', '283', '284', '285']
            # leather satchel, slug on pumpkin, harmonic pearl, red deer, gold mine
            # morning mirage, green toad, hare in a cabbage field, dirt road at night, mythical night lemon
            # lemony grape candy, dirt pond, tangerine sea, summer harvest, inversed plum
            ['LEATHER SATCHEL', 'SLUG ON PUMPKIN', 'HARMONIC PEARL', 'RED DEER', 'GOLD MINE',
            'MORNING MIRAGE', 'GREEN TOAD', 'HARE IN A CABBAGE FIELD', 'DIRT ROAD AT NIGHT', 'MYTHICAL NIGHT LEMON',
            'LEMONY GRAPE CANDY', 'DIRT POND', 'TANGERINE SEA', 'SUMMER HARVEST', 'INVERSED PLUM'],
            
            # row twenty
            # ['286', '287', '288', '289', '290',
            # '291', '292', '293', '294', '295',
            # '296', '297', '298', '299', '300']
            # vintage pink poodle, sparking metal, cyber blacklist, lovely cherry blossom, strawberry pink
            # coffee grounds, glittering amber, kingfisher, graphite pencil, pheasant in spring
            # river clay, russet, light at sea, chocolate, street caramel
            ['VINTAGE PINK POODLE', 'SPARKING METAL', 'CYBER BLACKLIST', 'LOVELY CHERRY BLOSSOM', 'STRAWBERRY PINK',
            'COFFEE GROUNDSA', 'GLITTERING AMBER', 'KINGFISHER', 'GRAPHITE PENCIL', 'PHEASANT IN SPRING',
            'RIVER CLAY', 'RUSSET', 'LIGHT AT SEA', 'CHOCOLATE', 'STREET CARAMEL'],
            
            # row twenty one
            # ['301', '302', '303', '304', '305',
            # '306', '307', '308', '309', '310',
            # '311', '312', '313', '314', '315']
            # dusty lamp, rugged leather, portafino, queen butterfly, firebug on moss
            # overcast cotton candy, mandy, snowing after dark, aqua, city trash
            # warm ash, sepia, wet phone screen, cerise lit, brilliant sky
            ['DUSTY LAMP', 'RUGGED LEATHER', 'PORTAFINO', 'QUEEN BUTTERFLY', 'FIREBUG ON MOSS',
            'OVERCAST COTTON CANDY', 'MANDY', 'SNOWING AFTER DARK', 'AQUA', 'CITY TRASH',
            'WARM ASH', 'SEPIA', 'WET PHONE SCREEN', 'CERISE LIT', 'BRILLIANT SKY'],
            
            # row twenty two
            # ['316', '317', '318', '319', '320',
            # '321', '322', '323', ''324, '325',
            # '326', '327', '328', '329', '330']
            # murky swamp, soulful taiga, reversed blues, russian violet, tuscan olive
            # spinel black, chic taupe, anarchist greys, black sunset blaze, precious coral reef
            # flowered moorland, balloon in the sky, nocturnal expedition, sea turtle green, fire
            ['MURKY SWAMP', 'SOULFUL TAIGA', 'REVERSED BLUES', 'RUSSIAN VIOLET', 'TUSCAN OLIVE',
            'SPINEL BLACK', 'CHIC TAUPE', 'ANARCHIST GREYS', 'BLACK SUNSET BLAZE', 'PRECIOUS CORAL REEF',
            'FLOWERED MOORLAND', 'BALLOON IN THE SKY', 'NOCTURNAL EXPEDITION', 'SEA TURTLE GREEN', 'FIRE'],
            
            # row twenty three
            # ['331', '332', '333', '334', '335',
            # '336', '337', '338', '339', '340',
            # '341', '342', '343', '344', '345']
            # unnamed: 2 -- 331, 333
            # name me! (331), berry smoothie, name me! (333), red macaw, holly on bush
            # autumn leaf, mossland creek, hot chocolate, green tree frog, ultramarine
            # lush forest, enjoyable evening, browning banana, water lily, crude gold
            ['NAME ME! (331)', 'BERRY SMOOTHIE', 'NAME ME! (333)', 'RED MACAW', 'HOLLY ON BUSH',
            'AUTUMN LEAF', 'MOSSLAND CREEK', 'HOT CHOCOLATE', 'GREEN TREE FROG', 'ULTRAMARINE',
            'LUSH FOREST', 'ENJOYABLE EVENING', 'BROWNING BANANA', 'WATER LILY', 'CRUDE GOLD'],
            
            # row twenty four
            # ['346', '347', '348', '349', '350',
            # '351', '352', '353', '354', '355',
            # '356', '357', '358', '359', '360']
            # bloodline fire, light in the deep, dark orchid, inversed inferno, noble plum
            # weeping willow, sea serpent, inversed maroon, reversed heroic red, Barbie
            # evening violet, velvet, galaxy empress, pecan, northern lights violet
            ['BLOODLINE FIRE', 'LIGHT IN THE DEEP', 'DARK ORCHID', 'INVERSED INFERNO', 'NOBLE PLUM',
            'WEEPING WILLOW', 'SEA SERPENT', 'INVERSED MAROON', 'REVERSED HEROIC RED', 'BARBIE',
            'EVENING VIOLET', 'VELVET', 'GALAXY EMPRESS', 'PECAN', 'NOTHERN LIGHTS VIOLET']
        ]

        for row, colors in enumerate(eye_colors):
            for col, color in enumerate(colors):
                self.make_group('eyes', (col, row), f'eyes{color}')
                self.make_group('eyes2', (col, row), f'eyes2{color}')

        # Define white patches
        white_patches = [
            ['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO', 'MOON', 'PHANTOM', 'POWDER',
             'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE'],
            ['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 'LIGHTSONG', 'VITILIGO', 'BLACKSTAR',
             'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL'],
            ['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO', 'PAWS', 'MITAINE',
             'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD'],
            ['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY', 'FAROFA', 'DAMIEN', 'MISTER', 'BELLY',
             'TAILTIP', 'TOES', 'TOPCOVER'],
            ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW', 'PANTS', 'REVERSEPANTS',
             'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW'],
            ['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT', 'MAO', 'LUNA', 'CHESTSPECK',
             'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER'],
            ['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART', 'SPARROW', 'VEST',
             'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE'],
            ['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE', 'FADEBELLY', 'FRONT',
             'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS'],
            ['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR', 'BUSTER', 'SMOKEY', 'HAWKBLAZE',
             'CAKE', 'ROSINA', 'PRINCESS'],
            ['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']
        ]

        for row, patches in enumerate(white_patches):
            for col, patch in enumerate(patches):
                self.make_group('whitepatches', (col, row), f'white{patch}')

        # Define colors and categories
        color_categories = [
            ['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK'],
            ['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA'],
            ['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']
        ]

        color_types = [
            'singlecolours', 'tabbycolours', 'marbledcolours', 'rosettecolours',
            'smokecolours', 'tickedcolours', 'speckledcolours', 'bengalcolours',
            'mackerelcolours', 'classiccolours', 'sokokecolours', 'agouticolours',
            'singlestripecolours', 'maskedcolours'
        ]

        for row, colors in enumerate(color_categories):
            for col, color in enumerate(colors):
                for color_type in color_types:
                    self.make_group(color_type, (col, row), f'{color_type[:-7]}{color}')

        # tortiepatchesmasks
        tortiepatchesmasks = [
            ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE'],
            ['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL',
             'GRUMPYFACE'],
            ['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE'],
            ['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY'],
            ['SHILOH', 'FRECKLED', 'HEARTBEAT']
        ]

        for row, masks in enumerate(tortiepatchesmasks):
            for col, mask in enumerate(masks):
                self.make_group('tortiepatchesmasks', (col, row), f"tortiemask{mask}")

        # Define skin colors 
        skin_colors = [
            ['BLACK', 'RED', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN'],
            ['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH'],
            ['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']
        ]

        for row, colors in enumerate(skin_colors):
            for col, color in enumerate(colors):
                self.make_group('skin', (col, row), f"skin{color}")

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """

        # Define scars
        scars_data = [
            ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
             "BOTHBLIND", "BURNPAWS", "BURNTAIL"],
            ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE", "FROSTFACE", "FROSTTAIL",
             "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"],
            ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE", "LEGBITE",
             "NECKBITE", "FACE"],
            ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]
        ]

        # define missing parts
        missing_parts_data = [
            ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]
        ]

        # scars 
        for row, scars in enumerate(scars_data):
            for col, scar in enumerate(scars):
                self.make_group('scars', (col, row), f'scars{scar}')

        # missing parts
        for row, missing_parts in enumerate(missing_parts_data):
            for col, missing_part in enumerate(missing_parts):
                self.make_group('missingscars', (col, row), f'scars{missing_part}')

        # accessories
        #to my beloved modders, im very sorry for reordering everything <333 -clay
        medcatherbs_data = [
            ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "CATTAIL", "POPPY", "ORANGE POPPY", "CYAN POPPY", "WHITE POPPY", "PINK POPPY"],
            ["BLUEBELLS", "LILY OF THE VALLEY", "SNAPDRAGON", "HERBS", "PETALS", "NETTLE", "HEATHER", "GORSE", "JUNIPER", "RASPBERRY", "LAVENDER"],
            ["OAK LEAVES", "CATMINT", "MAPLE SEED", "LAUREL", "BULB WHITE", "BULB YELLOW", "BULB ORANGE", "BULB PINK", "BULB BLUE", "CLOVER", "DAISY"]
        ]
        dryherbs_data = [
            ["DRY HERBS", "DRY CATMINT", "DRY NETTLES", "DRY LAURELS"]
        ]
        wild_data = [
            ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS", "SPARROW FEATHERS", "MOTH WINGS", "ROSY MOTH WINGS", "MORPHO BUTTERFLY", "MONARCH BUTTERFLY", "CICADA WINGS", "BLACK CICADA"]
        ]

        collars_data = [
            ["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"],
            ["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"],
            ["PINK", "PURPLE", "MULTI", "INDIGO"]
        ]

        bellcollars_data = [
            ["CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL"],
            ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"],
            ["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]
        ]

        bowcollars_data = [
            ["CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW", "LIMEBOW"],
            ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"],
            ["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]
        ]

        nyloncollars_data = [
            ["CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON", "LIMENYLON"],
            ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"],
            ["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]
        ]

        # medcatherbs
        for row, herbs in enumerate(medcatherbs_data):
            for col, herb in enumerate(herbs):
                self.make_group('medcatherbs', (col, row), f'acc_herbs{herb}')
        #dryherbs
        for row, dry in enumerate(dryherbs_data):
            for col, dryherbs in enumerate(dry):
                self.make_group('medcatherbs', (col, 3), f'acc_herbs{dryherbs}')     
        # wild
        for row, wilds in enumerate(wild_data):
            for col, wild in enumerate(wilds):
                self.make_group('wild', (col, 0), f'acc_wild{wild}')

        # collars
        for row, collars in enumerate(collars_data):
            for col, collar in enumerate(collars):
                self.make_group('collars', (col, row), f'collars{collar}')

        # bellcollars
        for row, bellcollars in enumerate(bellcollars_data):
            for col, bellcollar in enumerate(bellcollars):
                self.make_group('bellcollars', (col, row), f'collars{bellcollar}')

        # bowcollars
        for row, bowcollars in enumerate(bowcollars_data):
            for col, bowcollar in enumerate(bowcollars):
                self.make_group('bowcollars', (col, row), f'collars{bowcollar}')

        # nyloncollars
        for row, nyloncollars in enumerate(nyloncollars_data):
            for col, nyloncollar in enumerate(nyloncollars):
                self.make_group('nyloncollars', (col, row), f'collars{nyloncollar}')

    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            x_mod = 0
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                if self.symbol_dict[symbol]["variants"] > 1 and x_mod > 0:
                    x_mod += -1
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_pos = i + x_mod

                    if self.symbol_dict[symbol]["variants"] > 1:
                        x_mod += 1
                    elif x_mod > 0:
                        x_pos += - 1

                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (x_pos, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1

    def dark_mode_symbol(self, symbol):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((87, 76, 45), (239, 229, 206))
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()
