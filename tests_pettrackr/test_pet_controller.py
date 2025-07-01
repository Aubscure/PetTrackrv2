# tests/test_pet_controller.py
import sys, os
from datetime import datetime, timedelta
import random
import string
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controllers.pet_controller import PetController
from backend.models.pet import Pet, Owner
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController
from backend.services.daycare_prices import compute_total_fee

class PetTrackrCLI:
    def __init__(self):
        self.controller, self.vet_visit_controller = PetController(), VetVisitController()
        self.vaccination_controller, self.feeding_log_controller = VaccinationController(), FeedingLogController()
        os.makedirs(os.path.join('..', 'data', 'images'), exist_ok=True)

    def _get_valid_input(self, prompt, validator=None):
        while True:
            try:
                v = input(prompt).strip()
                if validator: validator(v)
                return v
            except ValueError as e:
                print(f"❌ Invalid input: {e}")

    def _validate_date(self, s): datetime.strptime(s, "%Y-%m-%d")

    def add_pet_from_input(self):
        print("\n🐾 Add a New Pet")
        name = self._get_valid_input("Pet Name: ", lambda x: x or ValueError("Name cannot be empty"))
        breed = self._get_valid_input("Breed: ")
        birthdate = self._get_valid_input("Birthdate (YYYY-MM-DD): ", self._validate_date)
        image_path = self._get_valid_input("Path to image file (optional): ").strip() or None
        print("\n👤 Owner Information")
        owner_name = self._get_valid_input("Owner Name: ", lambda x: x or ValueError("Owner name cannot be empty"))
        contact_number = self._get_valid_input("Contact Number: ")
        address = self._get_valid_input("Address: ")
        pet = Pet(id=None, name=name, breed=breed or "", birthdate=birthdate, image_path="")
        owner = Owner(id=None, name=owner_name, contact_number=contact_number or "", address=address or "")
        if image_path and not os.path.isfile(image_path): print("❌ Image not found — saving without image."); image_path = None
        try:
            pet_id = self.controller.add_pet_with_owner(pet, owner, image_path)
            print("\n✅ Pet and owner saved successfully!")
            self.view_pet_profile(pet_id)
        except Exception as e:
            print(f"❌ Error saving pet: {e}")

    def list_pets(self):
        print("\n📋 All Pets with Owners:")
        try:
            pets, owners = self.controller.get_pets_with_owners()
            if not pets: print("No pets found in database"); return
            for i, (pet, owner) in enumerate(zip(pets, owners), 1):
                print(f"\n{i}. {pet}\n   Owner: {owner if owner else 'No owner information'}")
            while True:
                choice = input("\nEnter pet number to view profile (or 'back' to return): ").strip().lower()
                if choice == 'back': return
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pets): self.view_pet_profile(pets[idx].id); return
                    print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving pets: {e}")

    def _add_vet_visit(self, pet_id):
        print("\n🩺 Add Vet Visit")
        data = {
            "pet_id": pet_id,
            "visit_date": self._get_valid_input("Visit Date (YYYY-MM-DD): ", self._validate_date),
            "reason": input("Reason: "),
            "notes": input("Notes (optional): ")
        }
        self.vet_visit_controller.create(data)
        print("✅ Vet Visit saved.")

    def _add_vaccination(self, pet_id):
        print("\n💉 Add Vaccination")
        data = {
            "pet_id": pet_id,
            "vaccine_name": input("Vaccine Name: "),
            "date_administered": self._get_valid_input("Date Administered (YYYY-MM-DD): ", self._validate_date),
            "next_due": self._get_valid_input("Next Due Date (YYYY-MM-DD): ", self._validate_date),
            "category": input("Category (e.g., Core, Optional, Rabies): "),
            "notes": input("Notes (optional): ")
        }
        self.vaccination_controller.create(data)
        print("✅ Vaccination saved.")

    def view_pet_profile(self, pet_id):
        try:
            pet, owner = self.controller.get_pet_by_id(pet_id)
            if not pet: print(f"❌ Pet with ID {pet_id} not found"); return
            while True:
                print("\n" + "="*40 + f"\n🐾 {pet.name}'s Profile\n" + "="*40)
                print(f"Breed: {pet.breed}\nBirthdate: {pet.birthdate}")
                if pet.image_path and os.path.exists(os.path.join(self.controller.data_dir, pet.image_path)):
                    print(f"Image: {pet.image_path}")
                if owner: print(f"\n👤 Owner Information:\nName: {owner.name}\nContact: {owner.contact_number}\nAddress: {owner.address}")
                for label, ctrl, attr, fmt in [
                    ("🩺 Vet Visits", self.vet_visit_controller, "get_by_pet_id", lambda v: f"  - {v.visit_date}: {v.reason}" + (f"\n    Notes: {v.notes}" if v.notes else "")),
                    ("💉 Vaccinations", self.vaccination_controller, "get_by_pet_id", None),
                    ("🍖 Feeding Logs", self.feeding_log_controller, "get_by_pet_id", None),
                ]:
                    try:
                        items = getattr(ctrl, attr)(pet_id)
                        if items:
                            print(f"\n{label}:")
                            if label == "💉 Vaccinations":
                                for v in items:
                                    print(f"  - {v.vaccine_name} (Administered: {v.date_administered}, Next Due: {v.next_due})")
                                    if getattr(v, 'category', None):
                                        print(f"    Category: {v.category}")
                                    if getattr(v, 'notes', None):
                                        print(f"    Notes: {v.notes}")
                            elif label == "🍖 Feeding Logs":
                                # Display feeding logs with detailed breakdown
                                base = 350
                                total = 0
                                print("  --- Feeding Log Receipt ---")
                                for v in items:
                                    plan = ", ".join([desc for desc, flag in [("Once", v.feed_once), ("Twice", v.feed_twice), ("Thrice", v.feed_thrice)] if flag]) or "No feeding"
                                    if v.feed_once:
                                        addon = 85
                                    elif v.feed_twice:
                                        addon = 170
                                    elif v.feed_thrice:
                                        addon = 255
                                    else:
                                        addon = 0
                                    fee = v.num_days * (base + addon)
                                    total += fee
                                    print(f"  - {v.start_date} | {v.num_days} day(s) | Plan: {plan}")
                                    print(f"    Breakdown: {v.num_days} x (₱{base} base + ₱{addon} feeding) = ₱{fee}")
                                print("  --------------------------")
                                print(f"  TOTAL FEEDING INVOICE: ₱{total}")
                            else:
                                [print(fmt(v)) for v in items]
                    except Exception as e:
                        print(f"\n⚠️ Could not load {label.lower()}: {str(e)}")
                print("\nOptions:\n1. Add Vet Visit\n2. Add Vaccination\n3. Add Feeding Log\n4. Back to Menu")
                choice = input("\nChoose an option: ").strip()
                if choice == "1": self._add_vet_visit(pet.id)
                elif choice == "2": self._add_vaccination(pet.id)
                elif choice == "3": self._add_feeding_log(pet.id)
                elif choice == "4": return
                else: print("❌ Invalid choice. Please try again.")
        except Exception as e:
            print(f"❌ Error accessing pet profile: {e}")

    def add_random_pet(self):
        name = self._random_string()
        breed = random.choice(['Shih Tzu', 'Poodle', 'Bulldog', 'Aspin'])
        birthdate = self._random_date(2015, 2022)
        image_path = None
        owner_name = self._random_string()
        contact_number = self._random_phone()
        address = f"{random.randint(1,999)} {self._random_string(8)} St."
        pet = Pet(id=None, name=name, breed=breed, birthdate=birthdate, image_path="")
        owner = Owner(id=None, name=owner_name, contact_number=contact_number, address=address)
        try:
            pet_id = self.controller.add_pet_with_owner(pet, owner, image_path)
            print(f"\n✅ Random pet and owner saved! Pet ID: {pet_id}")
            self._add_random_feeding_log(pet_id)
            self._add_random_vaccination(pet_id)  # Add random vaccination
        except Exception as e:
            print(f"❌ Error saving random pet: {e}")

    def _add_random_vaccination(self, pet_id):
        vaccine_names = ["Rabies", "Distemper", "Bordetella", "Parvo"]
        categories = ["Core", "Optional", "Rabies"]
        vaccine_name = random.choice(vaccine_names)
        date_administered = self._random_date(2023, 2025)
        # Use model's default interval for next_due
        from backend.models.vaccination import Vaccination
        vax = Vaccination(
            pet_id=pet_id,
            vaccine_name=vaccine_name,
            date_administered=date_administered,
            category=random.choice(categories),
            notes=random.choice(["", "No side effects", "Mild fever", "Vet: Dr. Smith"])
        )
        data = vax.to_dict()
        # Remove is_due from dict before saving
        data.pop("is_due", None)
        self.vaccination_controller.create(data)
        print(f"✅ Random vaccination saved: {vaccine_name} ({date_administered})")

    def _add_random_feeding_log(self, pet_id):
        start_date = self._random_date(2023, 2025)
        num_days = random.randint(1, 14)
        feed_once = random.choice([True, False])
        feed_twice = not feed_once and random.choice([True, False])
        feed_thrice = not feed_once and not feed_twice
        data = {
            "pet_id": pet_id,
            "start_date": start_date,
            "num_days": num_days,
            "feed_once": feed_once,
            "feed_twice": feed_twice,
            "feed_thrice": feed_thrice
        }
        self.feeding_log_controller.create(data)
        print(f"✅ Random feeding log saved: {num_days} day(s) starting {start_date}")

    def run(self):
        menu = {
            "1": self.add_pet_from_input,
            "2": self.list_pets,
            "3": lambda: exit(print("Goodbye!")),
            "4": self.add_random_pet  # Add this line for random input
        }
        while True:
            print("\n=== PetTrackr Main Menu ===\n1. Add Pet\n2. View Pets\n3. Exit\n4. Add Random Pet")
            menu.get(input("\nChoose an option: ").strip(), lambda: print("❌ Invalid choice. Please try again."))()

    def _random_string(self, length=6):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def _random_date(self, start_year=2015, end_year=2025):
        start = datetime(start_year, 1, 1)
        end = datetime(end_year, 12, 31)
        delta = end - start
        random_days = random.randint(0, delta.days)
        return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

    def _random_phone(self):
        return "09" + ''.join(random.choices(string.digits, k=9))

if __name__ == "__main__":
    try:
        PetTrackrCLI().run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")