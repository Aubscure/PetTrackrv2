# PetTrackr: Programming Structures Overview

This document explains how core programming structures and concepts are implemented in the PetTrackr project. Each section includes specific examples and file references so you can easily locate them in the codebase.

---

## 1. Sequential Structures

**Definition:** Code that executes line by line, in order.

**Where in PetTrackr:**

- **Example:** The setup and initialization code in `backend/data/pets_db.py` and `frontend/gui.py` runs sequentially.
- **Code Reference:**
  - `backend/data/pets_db.py`
    ```python
    # ...existing code...
    def initialize_db():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(CREATE_PETS_TABLE)
        conn.commit()
        conn.close()
    # ...existing code...
    ```
  - `frontend/gui.py`
    ```python
    # ...existing code...
    app = App()
    app.mainloop()
    # ...existing code...
    ```

---

## 2. Decision Structures

**Definition:** Code that makes choices using `if`, `elif`, and `else`.

**Where in PetTrackr:**

- **Example:** Input validation and error handling in `frontend/views/pet_form_view.py` and `backend/services/data_import.py`.
- **Code Reference:**
  - `frontend/views/pet_form_view.py`
    ```python
    # ...existing code...
    if not pet_name:
        messagebox.showerror("Error", "Pet name is required.")
        return
    elif not age.isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return
    # ...existing code...
    ```
  - `backend/services/data_import.py`
    ```python
    # ...existing code...
    if not os.path.exists(filepath):
        raise FileNotFoundError("File does not exist.")
    # ...existing code...
    ```

---

## 3. Repetition Structures

**Definition:** Code that repeats actions using `for` or `while` loops.

**Where in PetTrackr:**

- **Example:** Iterating over pets for import/export in `backend/services/data_export.py` and `backend/services/data_import.py`.
- **Code Reference:**
  - `backend/services/data_export.py`
    ```python
    # ...existing code...
    for pet in pets:
        file.write(f"{pet['name']},{pet['age']},{pet['type']}\n")
    # ...existing code...
    ```
  - `backend/services/data_import.py`
    ```python
    # ...existing code...
    for line in file:
        fields = line.strip().split(',')
        # process fields
    # ...existing code...
    ```

---

## 4. String Methods

**Definition:** Built-in methods for manipulating strings.

**Where in PetTrackr:**

- **Example:** Parsing and formatting data in `backend/services/data_import.py`.
- **Code Reference:**
  - `backend/services/data_import.py`
    ```python
    # ...existing code...
    fields = line.strip().split(',')
    name = fields[0].capitalize()
    # ...existing code...
    ```

---

## 5. Text File Manipulation

**Definition:** Reading from and writing to text files.

**Where in PetTrackr:**

- **Example:** Exporting and importing pet data in `backend/services/data_export.py` and `backend/services/data_import.py`.
- **Code Reference:**
  - `backend/services/data_export.py`
    ```python
    # ...existing code...
    with open(filepath, 'w') as file:
        for pet in pets:
            file.write(f"{pet['name']},{pet['age']},{pet['type']}\n")
    # ...existing code...
    ```
  - `backend/services/data_import.py`
    ```python
    # ...existing code...
    with open(filepath, 'r') as file:
        for line in file:
            # process line
    # ...existing code...
    ```

---

## 6. Lists and Dictionaries

**Definition:** Data structures for storing collections and key-value pairs.

**Where in PetTrackr:**

- **Example:** Lists for storing pets, dictionaries for pet attributes.
- **Code Reference:**
  - `backend/services/data_export.py`
    ```python
    # ...existing code...
    pets = [
        {"name": "Buddy", "age": 3, "type": "Dog"},
        {"name": "Mittens", "age": 2, "type": "Cat"}
    ]
    # ...existing code...
    ```

---

## 7. Functions

**Definition:** Reusable blocks of code.

**Where in PetTrackr:**

- **Example:** Utility and handler functions throughout the codebase.
- **Code Reference:**
  - `backend/services/data_export.py`
    ```python
    # ...existing code...
    def export_pets_to_txt_from_db(filepath):
        # function body
    # ...existing code...
    ```

---

## 8. Program Modularization

**Definition:** Organizing code into modules and packages.

**Where in PetTrackr:**

- **Example:**
  - `frontend/` for GUI
  - `backend/` for logic, models, controllers, services
  - `tests_pettrackr/` for tests

---

## 9. Simple Graphics and Image Processing

**Definition:** Loading, displaying, and manipulating images.

**Where in PetTrackr:**

- **Example:** Image upload and manipulation in `frontend/components/image_uploader.py` using PIL.
- **Code Reference:**
  - `frontend/components/image_uploader.py`
    ```python
    # ...existing code...
    from PIL import Image
    img = Image.open(filepath)
    img = img.rotate(90)
    img.save(new_filepath)
    # ...existing code...
    ```

---

## 10. Graphical User Interfaces

**Definition:** Visual interfaces for user interaction.

**Where in PetTrackr:**

- **Example:** Built with customtkinter in `frontend/gui.py` and views in `frontend/views/`.
- **Code Reference:**
  - `frontend/gui.py`
    ```python
    # ...existing code...
    import customtkinter as ctk
    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            # setup GUI
    # ...existing code...
    ```

---

## 11. Designing with Classes

**Definition:** Object-oriented programming using classes.

**Where in PetTrackr:**

- **Example:** Models, controllers, and GUI components.
- **Code Reference:**
  - `backend/models/pet.py`
    ```python
    # ...existing code...
    class Pet:
        def __init__(self, name, age, pet_type):
            self.name = name
            self.age = age
            self.pet_type = pet_type
    # ...existing code...
    ```

---

## 12. Network Application and Client/Server Programming

**Definition:** Communication over a network.

**Where in PetTrackr:**

- **Status:** Not implemented.
- **Note:** `backend/services/network_service.py` exists as a placeholder for future network features.

---

## 13. Searching, Sorting, and Complexity

**Definition:** Algorithms for finding and ordering data; analyzing efficiency.

**Where in PetTrackr:**

- **Example:**
  - Searching: SQL queries in `backend/data/pets_db.py`
  - Sorting: Not explicitly implemented
  - Complexity: Not explicitly analyzed

---

## Summary Table

| Structure                          | Present? | Example File(s) / Location(s)                |
| ---------------------------------- | -------- | -------------------------------------------- |
| Sequential Structures              | Yes      | `backend/data/pets_db.py`, `frontend/gui.py` |
| Decision Structures                | Yes      | `frontend/views/pet_form_view.py`            |
| Repetition Structures              | Yes      | `backend/services/data_export.py`            |
| String Methods                     | Yes      | `backend/services/data_import.py`            |
| Text File Manipulation             | Yes      | `backend/services/data_export.py`            |
| Lists and Dictionaries             | Yes      | `backend/services/data_export.py`            |
| Functions                          | Yes      | Throughout                                   |
| Program Modularization             | Yes      | Project structure                            |
| Simple Graphics & Image Processing | Yes      | `frontend/components/image_uploader.py`      |
| Graphical User Interfaces          | Yes      | `frontend/gui.py`                            |
| Designing with Classes             | Yes      | `backend/models/pet.py`                      |
| Network Application/Client-Server  | No       | Placeholder only                             |
| Searching, Sorting, Complexity     | Partial  | SQL queries                                  |

---

**For more details, see the referenced files in each section. This document is generated from the PetTrackr codebase and may not reflect the latest changes.**
