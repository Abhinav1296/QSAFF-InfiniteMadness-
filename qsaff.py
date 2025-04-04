# CosmicFileLocker: A Quantum-Inspired File Encryption Tool
import qiskit as quantum
from cryptography.fernet import Fernet  # For real encryption
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Dict
from datetime import datetime

class CosmicFileLocker:
    def __init__(self):
        # Use Qiskit to generate a quantum-inspired random seed for key generation
        self.quantum_core = quantum.QuantumCircuit(5, 5)
        self.quantum_core.h(range(5))  # Apply Hadamard gates for superposition
        self.quantum_core.measure_all()
        self.storage = {}  # Simulated "black hole vault" as a dictionary

    def _generate_key_from_password(self, user_id: str, password: str) -> bytes:
        """Generate an encryption key from user ID and password using PBKDF2."""
        salt = self._get_quantum_random_bytes(16)  # Quantum-inspired salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive((user_id + password).encode()))
        return key

    def _get_quantum_random_bytes(self, length: int) -> bytes:
        """Simulate quantum randomness using Qiskit (falls back to classical if simulator unavailable)."""
        try:
            from qiskit import Aer, execute
            backend = Aer.get_backend('qasm_simulator')
            job = execute(self.quantum_core, backend, shots=1)
            result = job.result().get_counts()
            random_bits = list(result.keys())[0]  # Get binary string (e.g., '10110')
            byte_value = int(random_bits, 2).to_bytes((len(random_bits) + 7) // 8, byteorder='big')
            return byte_value.ljust(length, b'\x00')[:length]
        except Exception:
            return os.urandom(length)  # Fallback to classical randomness

    def _is_password_strong(self, password: str) -> bool:
        """Check if the password meets minimum strength requirements."""
        if len(password) < 8:
            print("Error: Password must be at least 8 characters long.")
            return False
        if not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            print("Error: Password must contain at least one uppercase letter and one digit.")
            return False
        return True

    def _make_unique_file_name(self, file_name: str) -> str:
        """Ensure file_name is unique by appending a number if it already exists."""
        base_name = file_name
        counter = 1
        while file_name in self.storage:
            file_name = f"{base_name}_{counter}"
            counter += 1
        return file_name

    def lock_new_file(self, user_id: str, password: str, file_name: str, file_content: str) -> str:
        """Encrypt a new file and store it with a user-provided file name."""
        if not self._is_password_strong(password):
            return None
        file_name = self._make_unique_file_name(file_name)  # Ensure uniqueness
        key = self._generate_key_from_password(user_id, password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_content.encode())
        self.storage[file_name] = {
            "data": encrypted_data,
            "user_id": user_id,
            "key": key,
            "created": datetime.now().isoformat(),
            "last_accessed": None
        }
        return file_name

    def change_lock(self, file_name: str, old_user_id: str, old_password: str, new_user_id: str, new_password: str) -> bool:
        """Change the encryption key of an existing file."""
        if file_name not in self.storage:
            print(f"Error: File '{file_name}' not found in cosmic vault.")
            return False
        
        if not self._is_password_strong(new_password):
            return False
        
        stored = self.storage[file_name]
        old_key = self._generate_key_from_password(old_user_id, old_password)
        if old_key != stored["key"]:
            print("Error: Incorrect old ID or password.")
            return False

        # Decrypt with old key
        fernet = Fernet(old_key)
        try:
            decrypted_data = fernet.decrypt(stored["data"]).decode()
        except Exception:
            print("Error: Failed to decrypt with old credentials.")
            return False

        # Encrypt with new key
        new_key = self._generate_key_from_password(new_user_id, new_password)
        new_fernet = Fernet(new_key)
        new_encrypted_data = new_fernet.encrypt(decrypted_data.encode())
        self.storage[file_name] = {
            "data": new_encrypted_data,
            "user_id": new_user_id,
            "key": new_key,
            "created": stored["created"],
            "last_accessed": stored["last_accessed"]
        }
        return True

    def _generate_mfa_code(self) -> str:
        """Generate a 6-digit MFA code using quantum randomness."""
        random_bytes = self._get_quantum_random_bytes(3)  # Enough for 6 digits
        code = str(int.from_bytes(random_bytes, byteorder='big') % 1000000).zfill(6)
        return code

    def retrieve_file(self, file_name: str, user_id: str, password: str) -> str:
        """Decrypt and return the file content if credentials and MFA match."""
        if file_name not in self.storage:
            print(f"Error: File '{file_name}' not found in cosmic vault.")
            return None
        
        stored = self.storage[file_name]
        key = self._generate_key_from_password(user_id, password)
        if key != stored["key"]:
            print("Error: Incorrect ID or password.")
            return None
        
        mfa_code = self._generate_mfa_code()
        print(f"Your MFA code is: {mfa_code}")
        user_input = input("Enter the MFA code: ").strip()
        if user_input != mfa_code:
            print("Error: Incorrect MFA code.")
            return None
        
        fernet = Fernet(key)
        try:
            decrypted_data = fernet.decrypt(stored["data"]).decode()
            self.storage[file_name]["last_accessed"] = datetime.now().isoformat()  # Update access time
            return decrypted_data
        except Exception:
            print("Error: Failed to decrypt file.")
            return None

    def delete_file(self, file_name: str, user_id: str, password: str) -> bool:
        """Delete a file from the cosmic vault if credentials match."""
        if file_name not in self.storage:
            print(f"Error: File '{file_name}' not found in cosmic vault.")
            return False
        
        stored = self.storage[file_name]
        key = self._generate_key_from_password(user_id, password)
        if key != stored["key"]:
            print("Error: Incorrect ID or password.")
            return False
        
        del self.storage[file_name]
        print(f"File '{file_name}' has been vaporized from the cosmic vault.")
        return True

    def show_file_details(self, file_name: str) -> None:
        """Display metadata for a specific file."""
        if file_name not in self.storage:
            print(f"Error: File '{file_name}' not found in cosmic vault.")
            return
        stored = self.storage[file_name]
        print(f"File Name: {file_name}")
        print(f"Owner: {stored['user_id']}")
        print(f"Created: {stored['created']}")
        print(f"Last Accessed: {stored['last_accessed'] or 'Never'}")

    def export_file(self, file_name: str, user_id: str, password: str, filepath: str) -> bool:
        """Export an encrypted file to disk."""
        if file_name not in self.storage:
            print(f"Error: File '{file_name}' not found in cosmic vault.")
            return False
        
        stored = self.storage[file_name]
        key = self._generate_key_from_password(user_id, password)
        if key != stored["key"]:
            print("Error: Incorrect ID or password.")
            return False
        
        with open(filepath, "wb") as f:
            f.write(stored["data"])
        print(f"File '{file_name}' exported to {filepath}.")
        return True

    def import_file(self, user_id: str, password: str, filepath: str) -> str:
        """Import an encrypted file from disk into the vault."""
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} not found on disk.")
            return None
        
        if not self._is_password_strong(password):
            return None
        
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        
        file_name = os.path.basename(filepath)  # Use filename from filepath as default
        file_name = self._make_unique_file_name(file_name)  # Ensure uniqueness
        key = self._generate_key_from_password(user_id, password)
        self.storage[file_name] = {
            "data": encrypted_data,
            "user_id": user_id,
            "key": key,
            "created": datetime.now().isoformat(),
            "last_accessed": None
        }
        print(f"File imported as '{file_name}'.")
        return file_name

    def list_locked_files(self) -> None:
        """Display all locked file names."""
        if not self.storage:
            print("No files locked in the cosmic vault.")
        else:
            print("Locked Files in Cosmic Vault:")
            for file_name in self.storage:
                print(f"- {file_name} (Owner: {self.storage[file_name]['user_id']})")

def main():
    locker = CosmicFileLocker()
    while True:
        print("\n=== Cosmic File Locker ===")
        print("1. Lock a new file")
        print("2. Change lock on existing file")
        print("3. Retrieve a locked file")
        print("4. List all locked files")
        print("5. Delete a locked file")
        print("6. Show file details")
        print("7. Export a locked file")
        print("8. Import a locked file")
        print("9. Exit")
        choice = input("What would you like to do? (1-9): ").strip()

        if choice == "1":
            user_id = input("Enter your cosmic ID: ").strip()
            password = input("Enter your cosmic password: ").strip()
            file_name = input("Enter a name for your file: ").strip()
            file_content = input("Enter the file content to lock: ").strip()
            file_name = locker.lock_new_file(user_id, password, file_name, file_content)
            if file_name:
                print(f"File locked successfully! Your file name is: '{file_name}'")
                print(f"Encrypted data (cosmic view): {locker.storage[file_name]['data']}")
            else:
                print("Failed to lock file due to weak password.")

        elif choice == "2":
            file_name = input("Enter the file name to change lock: ").strip()
            old_user_id = input("Enter your old cosmic ID: ").strip()
            old_password = input("Enter your old cosmic password: ").strip()
            new_user_id = input("Enter your new cosmic ID: ").strip()
            new_password = input("Enter your new cosmic password: ").strip()
            if locker.change_lock(file_name, old_user_id, old_password, new_user_id, new_password):
                print("Lock changed successfully!")
                print(f"New encrypted data (cosmic view): {locker.storage[file_name]['data']}")
            else:
                print("Failed to change lock.")

        elif choice == "3":
            file_name = input("Enter the file name to retrieve: ").strip()
            user_id = input("Enter your cosmic ID: ").strip()
            password = input("Enter your cosmic password: ").strip()
            content = locker.retrieve_file(file_name, user_id, password)
            if content:
                print(f"Decrypted File Content: {content}")
            else:
                print("Failed to retrieve file.")

        elif choice == "4":
            locker.list_locked_files()

        elif choice == "5":
            file_name = input("Enter the file name to delete: ").strip()
            user_id = input("Enter your cosmic ID: ").strip()
            password = input("Enter your cosmic password: ").strip()
            if locker.delete_file(file_name, user_id, password):
                print("File deleted successfully!")
            else:
                print("Failed to delete file.")

        elif choice == "6":
            file_name = input("Enter the file name to view details: ").strip()
            locker.show_file_details(file_name)

        elif choice == "7":
            file_name = input("Enter the file name to export: ").strip()
            user_id = input("Enter your cosmic ID: ").strip()
            password = input("Enter your cosmic password: ").strip()
            filepath = input("Enter the export filepath (e.g., file.cosmic): ").strip()
            if locker.export_file(file_name, user_id, password, filepath):
                print("Export successful!")
            else:
                print("Export failed.")

        elif choice == "8":
            user_id = input("Enter your cosmic ID: ").strip()
            password = input("Enter your cosmic password: ").strip()
            filepath = input("Enter the filepath to import (e.g., file.cosmic): ").strip()
            file_name = locker.import_file(user_id, password, filepath)
            if file_name:
                print(f"Import successful! New file name: '{file_name}'")
            else:
                print("Import failed.")

        elif choice == "9":
            print("Exiting Cosmic File Locker. Goodbye, traveler!")
            break

        else:
            print("Invalid choice. Please select 1-9.")

if __name__ == "__main__":
    main()
