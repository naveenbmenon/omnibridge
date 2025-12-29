from omnibridge.accounts.store import InMemoryTokenStore

# SINGLE shared token store for the whole app
token_store = InMemoryTokenStore()
