import os
import shutil
import datetime
import time
import zipfile
import logging
import configparser
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("minecraft_backup.log"),
        logging.StreamHandler()
    ]
)

class MinecraftBedrockBackup:
    def __init__(self, config_path="backup_config.ini"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file or create default if not exists"""
        config = configparser.ConfigParser()
        
        if not os.path.exists(self.config_path):
            logging.info("Creating default configuration file")
            config['Settings'] = {
                'ServerPath': r'C:\Minecraft\BedrockServer',
                'BackupPath': r'C:\Minecraft\Backups',
                'MaxBackups': '5',
                'BackupInterval': '24',  # hours
                'WorldName': 'Bedrock level'  # Default world name
            }
            
            with open(self.config_path, 'w') as f:
                config.write(f)
            
            logging.info(f"Default configuration created at {self.config_path}")
            logging.info("Please edit the configuration file with your server details and run again.")
            sys.exit(0)
        
        config.read(self.config_path)
        return config
    
    def create_backup(self):
        """Create a backup of the Minecraft Bedrock server world"""
        server_path = self.config['Settings']['ServerPath']
        backup_path = self.config['Settings']['BackupPath']
        world_name = self.config['Settings']['WorldName']
        
        # Ensure backup directory exists
        os.makedirs(backup_path, exist_ok=True)
        
        # Create timestamp for backup name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"minecraft_bedrock_backup_{timestamp}"
        backup_zip = os.path.join(backup_path, f"{backup_name}.zip")
        
        # Path to the world folder
        worlds_path = os.path.join(server_path, "worlds")
        world_path = os.path.join(worlds_path, world_name)
        
        if not os.path.exists(world_path):
            # Try to find the world folder if the name doesn't match
            if os.path.exists(worlds_path):
                world_folders = [d for d in os.listdir(worlds_path) 
                                if os.path.isdir(os.path.join(worlds_path, d))]
                if world_folders:
                    world_path = os.path.join(worlds_path, world_folders[0])
                    logging.info(f"Using world folder: {world_folders[0]}")
                else:
                    logging.error(f"No world folders found in {worlds_path}")
                    return False
            else:
                logging.error(f"World path not found: {world_path}")
                return False
        
        logging.info(f"Creating backup of world: {world_path}")
        
        try:
            # Create zip file
            with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Walk through all files in the world directory
                for root, _, files in os.walk(world_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate path inside the zip file
                        arcname = os.path.relpath(file_path, os.path.dirname(world_path))
                        logging.debug(f"Adding {file_path} as {arcname}")
                        zipf.write(file_path, arcname)
            
            logging.info(f"Backup created successfully: {backup_zip}")
            return True
        except Exception as e:
            logging.error(f"Error creating backup: {str(e)}")
            return False
    
    def cleanup_old_backups(self):
        """Remove old backups to keep only the specified number"""
        backup_path = self.config['Settings']['BackupPath']
        max_backups = int(self.config['Settings']['MaxBackups'])
        
        # List all backup files
        backup_files = [os.path.join(backup_path, f) for f in os.listdir(backup_path) 
                       if f.startswith("minecraft_bedrock_backup_") and f.endswith(".zip")]
        
        # Sort by modification time (newest first)
        backup_files.sort(key=os.path.getmtime, reverse=True)
        
        # Remove excess backups
        if len(backup_files) > max_backups:
            for old_backup in backup_files[max_backups:]:
                try:
                    os.remove(old_backup)
                    logging.info(f"Removed old backup: {old_backup}")
                except Exception as e:
                    logging.error(f"Error removing old backup {old_backup}: {str(e)}")
    
    def run_scheduled_backup(self):
        """Run backups at the specified interval"""
        interval_hours = float(self.config['Settings']['BackupInterval'])
        interval_seconds = interval_hours * 3600
        
        logging.info(f"Starting scheduled backup every {interval_hours} hours")
        
        while True:
            success = self.create_backup()
            if success:
                self.cleanup_old_backups()
            
            logging.info(f"Next backup in {interval_hours} hours")
            time.sleep(interval_seconds)

def main():
    print("Minecraft Bedrock Server Backup Tool")
    print("====================================")
    
    backup_tool = MinecraftBedrockBackup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        backup_tool.run_scheduled_backup()
    else:
        print("\nCreating a one-time backup...")
        success = backup_tool.create_backup()
        if success:
            backup_tool.cleanup_old_backups()
            print("\nBackup completed successfully!")
            print("\nTo run scheduled backups, use: python minecraft_backup.py --schedule")

if __name__ == "__main__":
    main()