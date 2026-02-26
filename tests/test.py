# Change this:
import config

# To this:
try:
    import config
    
    print("Config imported successfully.")
    print(f"EMAIL: {config.EMAIL}")
except ImportError:
    from .. import config  # Try relative import if in a package