from frontend.components.pet_card import PetCard
import customtkinter as ctk
from frontend.style.style import (
    create_label, 
    create_frame, 
    get_subtitle_font, 
    get_card_detail_font,
    get_card_title_font,
    get_card_icon_font
)
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.vet_visit_controller import VetVisitController

class PetCardWithRecords(PetCard):
    def __init__(self, master, pet, image_store, owner=None, on_click=None, *args, **kwargs):
        self.vaccinations = VaccinationController().get_by_pet_id(pet.id)
        self.vet_visits = VetVisitController().get_by_pet_id(pet.id)
        self.on_click = on_click  # Save the callback
        super().__init__(master, pet, image_store, owner, on_click, *args, **kwargs)

    def _build_card(self):
        # Main container
        container = create_frame(self, "white")
        container.pack(padx=12, pady=12, fill="both", expand=True)
        self._bind_click(container)  # Make the card clickable

        # Horizontal layout: left (details), right (image)
        main_row = create_frame(container, "white")
        main_row.pack(fill="both", expand=True)

        # --- LEFT: Info Section ---
        info_frame = create_frame(main_row, "white")
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Name with icon
        name_frame = create_frame(info_frame, "white")
        name_frame.pack(pady=(0, 8), anchor="w")
        ctk.CTkLabel(
            name_frame,
            text="🐾",
            font=get_card_icon_font(),
        ).pack(side="left", padx=(0, 5))
        label_name = create_label(
            name_frame,
            self.pet.name,
            font=get_card_title_font()
        )
        label_name.pack(side="left")

        # Details with icon-text pairs
        details_frame = create_frame(info_frame, "white")
        details_frame.pack(fill="x", padx=8)

        # Breed row
        breed_row = create_frame(details_frame, "white")
        breed_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            breed_row,
            text="🐶",
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            breed_row,
            self.pet.breed or "Unknown",
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Birthdate row
        birth_row = create_frame(details_frame, "white")
        birth_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            birth_row,
            text="📅",
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            birth_row,
            self.pet.birthdate,
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Age row
        age_row = create_frame(details_frame, "white")
        age_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            age_row,
            text="🕒",
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            age_row,
            self.pet.age(),
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Owner row (only if owner exists)
        if self.owner:
            owner_row = create_frame(details_frame, "white")
            owner_row.pack(fill="x", pady=3)
            ctk.CTkLabel(
                owner_row,
                text="👤",
                font=get_card_icon_font(),
                width=24,
                anchor="w"
            ).pack(side="left")
            create_label(
                owner_row,
                f"{self.owner.name} ({self.owner.contact_number})",
                font=get_card_detail_font(),
                anchor="w"
            ).pack(side="left", padx=5)

        # --- RIGHT: Image Section ---
        image_frame = create_frame(main_row, "white")
        image_frame.pack(side="right", fill="y", padx=(10, 0))
        thumbnail = self._get_pet_thumbnail()
        label_image = ctk.CTkLabel(
            image_frame,
            image=thumbnail,
            text="",
            compound="top"
        )
        label_image.pack(anchor="center", pady=5)

        # --- BELOW: Vaccination and Vet Visit Records Section ---
        records_frame = create_frame(container, "white")
        records_frame.pack(fill="x", pady=(10, 0))

        # Vaccinations
        vacc_label = create_label(records_frame, "Vaccinations:", font=get_subtitle_font())
        vacc_label.pack(anchor="w")
        if self.vaccinations:
            for v in self.vaccinations:
                create_label(records_frame, f"• {v}", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)
        else:
            create_label(records_frame, "No vaccinations.", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)

        # Vet Visits
        visit_label = create_label(records_frame, "Vet Visits:", font=get_subtitle_font())
        visit_label.pack(anchor="w", pady=(8, 0))
        if self.vet_visits:
            for v in self.vet_visits:
                create_label(records_frame, f"• {v}", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)
        else:
            create_label(records_frame, "No vet visits.", font=get_card_detail_font(), anchor="w").pack(anchor="w", padx=10)

    def _bind_click(self, widget):
        def handler(event):
            if self.on_click:
                self.on_click(self.pet)
        widget.bind("<Button-1>", handler)
        for child in widget.winfo_children():
            self._bind_click(child)