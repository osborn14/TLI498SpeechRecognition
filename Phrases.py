import Constants as CONSTANTS

# "a" phrases taken from: https://pdfs.semanticscholar.org/2e7e/bdd353c1de9e47fdd1cf0fce61bd33d87103.pdf
# "b" phrases taken from: https://www.cnet.com/how-to/google-home-complete-list-of-commands/
phrase_repeats = 3
phrases = [
    {
        CONSTANTS.ID: "a1",
        CONSTANTS.PHRASE: "Please take this dirty table cloth to the cleaners for me.",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "table cloth",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["tablecloth"]
            }
        ]
    }, {
        CONSTANTS.ID: "a2",
        CONSTANTS.PHRASE: "My father ran him off here six years ago.",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "six",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["6"]
            }
        ]
    }, {
        CONSTANTS.ID: "a3",
        CONSTANTS.PHRASE: "Who authorized the unlimited expense account?"
    }, {
        CONSTANTS.ID: "a4",
        CONSTANTS.PHRASE: "We can get it if we dig, he said patiently."
    }, {
        CONSTANTS.ID: "a5",
        CONSTANTS.PHRASE: "The fish began to leap frantically on the surface of the small lake."
    }, {
        CONSTANTS.ID: "a6",
        CONSTANTS.PHRASE: "Micheal colored the bedroom wall with crayons.",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "micheal",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["michael"]
            }
        ]
    }, {
        CONSTANTS.ID: "a7",
        CONSTANTS.PHRASE: "Right now may not be the best time for business mergers."
    }, {
        CONSTANTS.ID: "a8",
        CONSTANTS.PHRASE: "Highway and freeway mean the same thing."
    }, {
        CONSTANTS.ID: "a9",
        CONSTANTS.PHRASE: "His hip struck the knee of the next player."
    }, {
        CONSTANTS.ID: "a10",
        CONSTANTS.PHRASE: "Jazz and swing fans like fast music."
    }, {
        CONSTANTS.ID: "b1",
        CONSTANTS.PHRASE: "What is the weather like?"
    }, {
        CONSTANTS.ID: "b2",
        CONSTANTS.PHRASE: "How many ounces are in a cup?"
    }, {
        CONSTANTS.ID: "b3",
        CONSTANTS.PHRASE: "Set an alarm for 5:30am.",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "5:",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["five "]
            }, {
                CONSTANTS.WORD: "30",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["thirty "]
            }, {
                CONSTANTS.WORD: "5:30",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["530"]
            }, {
                CONSTANTS.WORD: "am",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: [" a m", " a. m.", " am"]
            }
        ]
    }, {
        CONSTANTS.ID: "b4",
        CONSTANTS.PHRASE: "Play Drake on Spotify."
    }, {
        CONSTANTS.ID: "b5",
        CONSTANTS.PHRASE: "Turn on the lights."
    }, {
        CONSTANTS.ID: "b6",
        CONSTANTS.PHRASE: "Raise the temperature 5 degrees.",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "5",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["five"]
            }, {
                CONSTANTS.WORD: " degrees",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["°"]
            }
        ]
    }, {
        CONSTANTS.ID: "b7",
        CONSTANTS.PHRASE: "Add spaghetti to my shopping list."
    }, {
        CONSTANTS.ID: "b8",
        CONSTANTS.PHRASE: "How much is a round-trip flight to New York?",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "round-trip",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["round trip"]
            }
        ]
    }, {
        CONSTANTS.ID: "b9",
        CONSTANTS.PHRASE: "What's the best restaurant in Berlin?"
    }, {
        CONSTANTS.ID: "b10",
        CONSTANTS.PHRASE: "Find my phone."
    }, {
        CONSTANTS.ID: "b11",
        CONSTANTS.PHRASE: "Play MSNBC from Tunein.",
        CONSTANTS.TRANSLATION_LIST: [
            {
                CONSTANTS.WORD: "msnbc",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["m s n b c", "m. s. n. b. c."]
            }, {
                CONSTANTS.WORD: "Tunein",
                CONSTANTS.ACCEPTABLE_ALTERNATIVE_LIST: ["tune in"]
            }
        ]
    }
]
