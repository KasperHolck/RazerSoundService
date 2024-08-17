#######################################################################
# ----------------------------- IMPORTS ----------------------------- #
#######################################################################

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import os
import subprocess
import math
import sys
from tkinter import messagebox
import ctypes
import argparse
from elevate import elevate

# Main dir
main_path_rss = os.environ['PROGRAMDATA'] + "\\RazerSoundService"

nssm_path = main_path_rss + "\\dist\\dependencies\\nssm.exe"

server_path = main_path_rss + "\\dist\\dependencies\\server.dist\\RustRazerSound.exe"

#######################################################################
# ---------------------------- Main loop ---------------------------- #
#######################################################################
    
def control_service(action):
    try:
        result = subprocess.run(action, check=True, shell=True, capture_output=True)
        success = result.stdout.strip().decode('utf-16')
        error = result.stderr.strip().decode('utf-16')
        
        if success:
            messagebox.showinfo("RazerSoundService", success)
        else:
            print(error)
            messagebox.showerror("RazerSoundService", error)
            
    except subprocess.CalledProcessError as e:
        # Print the output and error
        error_msg = e.stderr.strip().decode('utf-16', errors='ignore') if e.stderr else str(e)
        
        messagebox.showerror("RazerSoundService",
                             f"An error occurred:\n{e}")
        
    except FileNotFoundError:
        messagebox.showerror("RazerSoundService", "File not found.")
    
    except Exception as e:
        messagebox.showerror("RazerSoundService", f"An error occurred: {e}")

def install_service():
    # Install service:
    action = [nssm_path, "install", "RazerSoundService", server_path]
    
    control_service(action)

    # Set description:
    action = [nssm_path, "set", "RazerSoundService", "description", "A service that plays a sound continuously."]
    control_service(action)
    
    # Start the service:
    action = [nssm_path, "start", "RazerSoundService"]
    control_service(action)

def uninstall_service():
    action = [nssm_path, "stop", "RazerSoundService"]
    control_service(action)
    
    action = [nssm_path, "remove", "RazerSoundService"]
    control_service(action)

def restart_service():
    action = [nssm_path, "restart", "RazerSoundService"]
    control_service(action)

def get_service_status():
    action = [nssm_path, "status", "RazerSoundService"]
    control_service(action)

def start_service():
    action = [nssm_path, "start", "RazerSoundService"]
    control_service(action)

def stop_service():
    action = [nssm_path, "stop", "RazerSoundService"]
    control_service(action)

def quit_tray_app(icon):
    icon.stop()

#######################################################################
# -------------------------- Click actions -------------------------- #
#######################################################################

def on_clicked(icon, item):
    match item.text:
        case 'Install':
            install_service()
            
        case 'Uninstall':
            uninstall_service()
        
        case 'Start':
            start_service()
            
        case 'Stop':
            stop_service()
        
        case 'Restart':
            restart_service()
        
        case 'Get Status':
            get_service_status()
            
        case 'Quit':
            quit_tray_app(icon)
 
#######################################################################
# ----------------------- Build icon and menu ----------------------- #
#######################################################################
       
def create_icon_image():
    """Builds the image for the icon.
    """
    green = 175
    
    # Create an empty image with a green background
    size = (64, 64)  # Size of the image
    image = Image.new('RGBA', size, (0, green, 0, 255))  # Green background
    draw = ImageDraw.Draw(image)

    # Create a circular mask
    mask = Image.new('L', size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size[0], size[1]), fill=255)
    image.putalpha(mask)  # Apply the circular mask

    # Define the points of the diamond
    center = (32, 32)
    offset = 20  # Distance from center to corners

    points = [
        (center[0], center[1] - offset),  # Top point
        (center[0] + offset, center[1]),  # Right point
        (center[0], center[1] + offset),  # Bottom point
        (center[0] - offset, center[1])   # Left point
    ]

    # Draw the diamond shape
    draw.polygon(points, fill=(0, 0, 0))  # White diamond

    # Add a smaller diamond inside for a layered effect
    inner_offset = 10
    inner_points = [
        (center[0], center[1] - inner_offset),
        (center[0] + inner_offset, center[1]),
        (center[0], center[1] + inner_offset),
        (center[0] - inner_offset, center[1])
    ]
    draw.polygon(inner_points, fill=(0, green, 0))  # Black inner diamond

    # Optionally add a border around the diamond
    draw.line(points + [points[0]], fill=(0, 0, 0), width=2)

    return image

def build_menu() -> Menu:
    """Builds the menu for the tray icon.
    """
    return Menu(
        MenuItem(
            'Service', Menu(
                MenuItem(
                    'Install', on_clicked),
                MenuItem(
                    'Uninstall', on_clicked))),
        MenuItem(
            'Control', Menu(
                MenuItem(
                    'Start', on_clicked),
                MenuItem(
                    'Stop', on_clicked),
                MenuItem(
                    'Restart', on_clicked))),
        MenuItem(
            'Get Status', on_clicked),
        MenuItem(
            'Quit', on_clicked)
        )

#######################################################################
# ---------------------------- Main loop ---------------------------- #
#######################################################################

def setup(icon):
    icon.visible = True

def main():
    icon_image = create_icon_image()
    
    menu = build_menu()
    
    icon = Icon("RazerSoundService_Icon", icon_image, f"RazerSoundService", menu)
    
    icon.run(setup)

#######################################################################
# -------------------------- Run the server ------------------------- #
#######################################################################

def parsed_args():
    """Checks for parsed args and acts accordingly.\n
    If --debug is present will call elevate() to run as admin.\n
    Otherwise will check if the user is admin and if not will show an error message.
    """
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="RazerSoundService Tray Application")
    parser.add_argument(
        "-d", "--debug", help="When flag is set the program path is changed to development directory", action="store_true")

    args = parser.parse_args()

    # Check if debug arg is present and elevate the program
    if args.debug:
        elevate()
    elif not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showerror("RazerSoundService",
                             "Please run this application as administrator.")
        sys.exit()

def check_file_existence():
    """Ensures that the main directory exists and that the settings file exists.\n
    Otherise they are created.
    """
    # Ensure the main directory exists
    if not os.path.exists(main_path_rss):
        os.makedirs(main_path_rss)
        messagebox.showinfo("RazerSoundService",
                            f"The main directory has been created here: {main_path_rss}.\nThe folder will open where you have to drag\nthe dist folder into.\nRerun the tray application.")
        os.startfile(main_path_rss)
        sys.exit()

if __name__ == "__main__":
    # Parse arguments
    parsed_args()
    
    # Check for main directory existence
    check_file_existence()
    
    # Start the tray application
    main()