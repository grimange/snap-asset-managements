from ldap3 import Server, Connection, ALL

def test():
    server = Server('ldap://38.105.19.195', get_info=ALL)
    conn = Connection(server, "testuser01@snapscale.lan", 'X2qctENxwhLom1q5qkXV', auto_bind=True)

    conn.search('DC=snapscale,DC=lan', '(objectClass=user)', attributes=['cn', 'mail', 'sAMAccountName'])

    print(conn.entries[0].entry_to_json())
