import config

def is_staff(member):
    return any(
        role.id in [
            config.STAFF_ROLE_ID,
            config.OWNER_ROLE_ID
        ]
        for role in member.roles
    )

def is_owner(member):
    return any(
        role.id == config.OWNER_ROLE_ID
        for role in member.roles
    )
