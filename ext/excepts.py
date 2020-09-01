class NoMutedRole(Exception):
    """Muted role not found in the guild"""
    def __init__(self, msg):
        super.__init__(super(str, msg))
        self.message = msg
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return {'error': NoMutedRole, 'msg': self.msg}

class NotMod(Exception):
    """You are not moderator / administrator of a guild"""
    def __init__(self, msg):
        super.__init__(super(str, msg))
        self.message = msg
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return {'error': NotMod, 'msg': self.msg}