"""
JSON Database Module for Highrise Bot
A simple file-based database using JSON for data persistence
Supports CRUD operations with automatic file management
"""

import json
import os
import threading
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import uuid


class JSONDatabase:
    """
    A simple JSON-based database with CRUD operations
    Thread-safe with automatic file persistence
    """
    
    def __init__(self, db_path: str = "data", auto_save: bool = True):
        """
        Initialize the JSON database
        
        Args:
            db_path: Directory path for database files
            auto_save: Whether to automatically save changes to disk
        """
        self.db_path = db_path
        self.auto_save = auto_save
        self.tables: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        
        # Create database directory if it doesn't exist
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        
        # Load existing tables
        self._load_tables()
    
    def _load_tables(self) -> None:
        """Load all JSON files from the database directory"""
        if not os.path.exists(self.db_path):
            return
        
        for filename in os.listdir(self.db_path):
            if filename.endswith('.json'):
                table_name = filename[:-5]  # Remove .json extension
                file_path = os.path.join(self.db_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.tables[table_name] = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    self.tables[table_name] = {}
    
    def _save_table(self, table_name: str) -> None:
        """Save a specific table to disk"""
        if not self.auto_save:
            return
        
        file_path = os.path.join(self.db_path, f"{table_name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.tables.get(table_name, {}), f, indent=2, ensure_ascii=False)
    
    def create_table(self, table_name: str) -> bool:
        """
        Create a new table
        
        Args:
            table_name: Name of the table to create
            
        Returns:
            bool: True if table was created, False if it already exists
        """
        with self._lock:
            if table_name in self.tables:
                return False
            
            self.tables[table_name] = {}
            self._save_table(table_name)
            return True
    
    def drop_table(self, table_name: str) -> bool:
        """
        Drop a table and its file
        
        Args:
            table_name: Name of the table to drop
            
        Returns:
            bool: True if table was dropped, False if it didn't exist
        """
        with self._lock:
            if table_name not in self.tables:
                return False
            
            del self.tables[table_name]
            
            # Remove the file
            file_path = os.path.join(self.db_path, f"{table_name}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return True
    
    def list_tables(self) -> List[str]:
        """
        Get list of all table names
        
        Returns:
            List[str]: List of table names
        """
        with self._lock:
            return list(self.tables.keys())
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists
        
        Args:
            table_name: Name of the table
            
        Returns:
            bool: True if table exists
        """
        return table_name in self.tables
    
    # CRUD Operations
    
    def create(self, table_name: str, data: Dict[str, Any], 
               record_id: Optional[str] = None) -> str:
        """
        Create a new record in the table
        
        Args:
            table_name: Name of the table
            data: Data to insert
            record_id: Optional custom ID, generates UUID if not provided
            
        Returns:
            str: The ID of the created record
            
        Raises:
            ValueError: If table doesn't exist or ID already exists
        """
        with self._lock:
            if table_name not in self.tables:
                raise ValueError(f"Table '{table_name}' does not exist")
            
            if record_id is None:
                record_id = str(uuid.uuid4())
            
            if record_id in self.tables[table_name]:
                raise ValueError(f"Record with ID '{record_id}' already exists")
            
            # Add metadata
            record_data = data.copy()
            record_data['_id'] = record_id
            record_data['_created_at'] = datetime.now().isoformat()
            record_data['_updated_at'] = datetime.now().isoformat()
            
            self.tables[table_name][record_id] = record_data
            self._save_table(table_name)
            
            return record_id
    
    def read(self, table_name: str, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Read a record from the table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to read
            
        Returns:
            Optional[Dict[str, Any]]: The record data or None if not found
        """
        with self._lock:
            if table_name not in self.tables:
                return None
            
            return self.tables[table_name].get(record_id)
    
    def read_all(self, table_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Read all records from the table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dict[str, Dict[str, Any]]: All records in the table
        """
        with self._lock:
            if table_name not in self.tables:
                return {}
            
            return self.tables[table_name].copy()
    
    def update(self, table_name: str, record_id: str, 
               data: Dict[str, Any], merge: bool = True) -> bool:
        """
        Update a record in the table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to update
            data: New data for the record
            merge: If True, merge with existing data. If False, replace completely
            
        Returns:
            bool: True if record was updated, False if not found
        """
        with self._lock:
            if table_name not in self.tables:
                return False
            
            if record_id not in self.tables[table_name]:
                return False
            
            if merge:
                # Merge with existing data
                existing_data = self.tables[table_name][record_id]
                updated_data = existing_data.copy()
                updated_data.update(data)
            else:
                # Replace completely but preserve metadata
                existing_data = self.tables[table_name][record_id]
                updated_data = data.copy()
                updated_data['_id'] = record_id
                updated_data['_created_at'] = existing_data.get('_created_at', datetime.now().isoformat())
            
            updated_data['_updated_at'] = datetime.now().isoformat()
            
            self.tables[table_name][record_id] = updated_data
            self._save_table(table_name)
            
            return True
    
    def delete(self, table_name: str, record_id: str) -> bool:
        """
        Delete a record from the table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to delete
            
        Returns:
            bool: True if record was deleted, False if not found
        """
        with self._lock:
            if table_name not in self.tables:
                return False
            
            if record_id not in self.tables[table_name]:
                return False
            
            del self.tables[table_name][record_id]
            self._save_table(table_name)
            
            return True
    
    def count(self, table_name: str) -> int:
        """
        Count records in a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            int: Number of records in the table
        """
        with self._lock:
            if table_name not in self.tables:
                return 0
            
            return len(self.tables[table_name])
    
    def find(self, table_name: str, filter_func: callable) -> List[Dict[str, Any]]:
        """
        Find records matching a filter function
        
        Args:
            table_name: Name of the table
            filter_func: Function that takes a record and returns True if it matches
            
        Returns:
            List[Dict[str, Any]]: List of matching records
        """
        with self._lock:
            if table_name not in self.tables:
                return []
            
            matching_records = []
            for record in self.tables[table_name].values():
                try:
                    if filter_func(record):
                        matching_records.append(record.copy())
                except Exception:
                    # Skip records that cause errors in the filter function
                    continue
            
            return matching_records
    
    def find_one(self, table_name: str, filter_func: callable) -> Optional[Dict[str, Any]]:
        """
        Find the first record matching a filter function
        
        Args:
            table_name: Name of the table
            filter_func: Function that takes a record and returns True if it matches
            
        Returns:
            Optional[Dict[str, Any]]: First matching record or None
        """
        results = self.find(table_name, filter_func)
        return results[0] if results else None
    
    def find_by_field(self, table_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """
        Find records where a field equals a specific value
        
        Args:
            table_name: Name of the table
            field: Field name to check
            value: Value to match
            
        Returns:
            List[Dict[str, Any]]: List of matching records
        """
        return self.find(table_name, lambda record: record.get(field) == value)
    
    def save_all(self) -> None:
        """Force save all tables to disk"""
        with self._lock:
            for table_name in self.tables:
                self._save_table(table_name)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dict[str, Any]: Database statistics
        """
        with self._lock:
            stats = {
                'total_tables': len(self.tables),
                'table_stats': {},
                'db_path': self.db_path,
                'auto_save': self.auto_save
            }
            
            for table_name, table_data in self.tables.items():
                stats['table_stats'][table_name] = {
                    'record_count': len(table_data),
                    'file_exists': os.path.exists(os.path.join(self.db_path, f"{table_name}.json"))
                }
            
            return stats


# Example usage and utility functions
class UserDatabase:
    """
    Example implementation for managing user data in the Highrise bot
    """
    
    def __init__(self, db_path: str = "data"):
        self.db = JSONDatabase(db_path)
        self.table_name = "users"
        
        # Create table if it doesn't exist
        if not self.db.table_exists(self.table_name):
            self.db.create_table(self.table_name)
    
    def add_user(self, user_id: str, username: str, **additional_data) -> str:
        """Add a new user to the database"""
        user_data = {
            'user_id': user_id,
            'username': username,
            'join_count': 1,
            'last_seen': datetime.now().isoformat(),
            **additional_data
        }
        return self.db.create(self.table_name, user_data, user_id)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by user ID"""
        return self.db.read(self.table_name, user_id)
    
    def update_user(self, user_id: str, **data) -> bool:
        """Update user data"""
        return self.db.update(self.table_name, user_id, data)
    
    def increment_join_count(self, user_id: str) -> bool:
        """Increment user's join count"""
        user = self.get_user(user_id)
        if user:
            new_count = user.get('join_count', 0) + 1
            return self.update_user(user_id, 
                                  join_count=new_count,
                                  last_seen=datetime.now().isoformat())
        return False
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        return list(self.db.read_all(self.table_name).values())
    
    def find_users_by_username(self, username: str) -> List[Dict[str, Any]]:
        """Find users by username"""
        return self.db.find_by_field(self.table_name, 'username', username)
