import customtkinter as ctk
from frontend.components.pet_card_with_feeding_logs import PetCardWithFeedingLogs

# Mock Pet and Owner classes for testing
class MockPet:
    def __init__(self):
        self.id = 1
        self.name = "Buddy"
        self.breed = "Golden Retriever"
        self.birthdate = "2020-01-01"
        self.image_path = None
        self.owner_id = 1
    def age(self):
        return "4 years"

class MockOwner:
    def __init__(self):
        self.name = "Alice"
        self.contact_number = "123-456-7890"
        self.address = "123 Main St"

# Mock image store (replace with your actual image store if needed)
class MockImageStore:
    def get_thumbnail(self, pet):
        return None
    def append(self, item):
        pass  # Do nothing for tests

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Test PetCardWithFeedingLogs")

    pet = MockPet()
    owner = MockOwner()
    image_store = MockImageStore()

    card = PetCardWithFeedingLogs(root, pet, image_store, owner=owner)
    card.pack(padx=20, pady=20)

    root.mainloop()