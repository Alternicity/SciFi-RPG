import yaml
import os

class YAMLManager:
    def __init__(self, directory):
        # Ensure directory exists where runtime YAML files will be stored
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # A cache to hold in-memory data that we want to write to YAML later (batching)
        self._cache = {}

    def _get_file_path(self, file_name):
        """Helper function to get the full path to a YAML file."""
        return os.path.join(self.directory, f"{file_name}.yaml")

    def load_data(self, file_name):
        """Load data from a YAML file."""
        file_path = self._get_file_path(file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return yaml.safe_load(file) or {}
        return {}

    def save_data(self, file_name, data):
        """Save data to a YAML file."""
        file_path = self._get_file_path(file_name)
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def update_data(self, file_name, data):
        """Update in-memory data, to be written later in batch."""
        if file_name not in self._cache:
            self._cache[file_name] = self.load_data(file_name)
        
        # Merge the new data into the existing cache
        self._cache[file_name].update(data)

    def batch_save(self):
        """Write all cached updates to their respective YAML files."""
        for file_name, data in self._cache.items():
            self.save_data(file_name, data)
        # Clear cache after saving
        self._cache.clear()

    def delete_data(self, file_name, data):
        """Delete specific data entries from the YAML file."""
        existing_data = self.load_data(file_name)
        for key in data:
            existing_data.pop(key, None)
        self.save_data(file_name, existing_data)
