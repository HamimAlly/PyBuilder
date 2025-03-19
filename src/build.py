import os
import sys
import subprocess
import yaml

def load_config(config_file='build_config.yml'):
    """Load the YAML configuration file."""
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: The configuration file '{config_file}' was not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error loading YAML file: {e}")
        sys.exit(1)

def build_exe(config):
    """Build the executable using PyInstaller."""
    
    # Default values
    defaults = {
        'script_name': 'src/main.py',
        'icon': '',
        'onefile': True,
        'distpath': './dist',
        'workpath': './build',
        'specpath': './',
        'additional_options': []
    }

    # Update the config with defaults if keys are missing
    build_config = {key: config['build'].get(key, defaults[key]) for key in defaults}
    
    # Ensure the script file exists
    script_name = build_config['script_name']
    if not os.path.isfile(script_name):
        print(f"Error: The script '{script_name}' does not exist!")
        sys.exit(1)

    # Handle the icon option (check if it's non-empty)
    icon_option = ""
    icon_path = build_config['icon']
    if icon_path and os.path.isfile(icon_path):  # Only add the icon if it's a valid path
        icon_option = f"--icon={icon_path}"
    elif icon_path:
        print(f"Warning: The icon file '{icon_path}' does not exist or is invalid!")

    # Build the PyInstaller command based on the YAML config
    command = ['python', '-m', 'PyInstaller']
    
    # Add options from the configuration
    if build_config['onefile']:
        command.append('--onefile')
    
    command.append(f'--distpath={build_config["distpath"]}')
    command.append(f'--workpath={build_config["workpath"]}')
    command.append(f'--specpath={build_config["specpath"]}')
    
    # Add the icon option if available
    if icon_option:
        command.append(icon_option)

    # Add any additional options from the configuration
    if build_config['additional_options']:
        command.extend(build_config['additional_options'])

    # Add the script name to the command
    command.append(script_name)
    
    # Run the PyInstaller command
    subprocess.run(command, check=True)

    print(f"Build complete. The executable can be found in the '{build_config['distpath']}' folder.")

if __name__ == "__main__":
    # Load the configuration from the YAML file
    config = load_config('.config')
    
    # Build the executable using the loaded configuration
    build_exe(config)
