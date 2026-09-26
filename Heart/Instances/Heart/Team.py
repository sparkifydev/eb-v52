class Team:
    ID = [0, 1]
    Members = {}
    Type = 0
    ChatData = []

    def createTeamData(calling_instance, fields):
        return {
            'HighID': fields["TeamID"][0],
            'LowID': fields["TeamID"][1],
            'Members': {
                str(calling_instance.player.ID[1]): {
                    'HighID': calling_instance.player.ID[0],
                    'LowID': calling_instance.player.ID[1],
                    'Ready': False,
                    'Owner': True,
                    'TeamIndex': 0
                }
            },
            'Type': fields['roomType'],
            'mapID': fields['mapID'],
            'Invites': {},
            'ChatData': []
        }
