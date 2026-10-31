from django.core.management.base import BaseCommand

from bounty.models import HuntLog, WantedCriminal


CRIMINALS = [
    {
        "name": "Jax Harlan",
        "nickname": "Void Reaper",
        "reward": 12000,
        "latitude": "12.450000",
        "longitude": "-45.120000",
        "location_note": "Last seen near the Ring of Orpheus",
        "difficulty": 8,
        "armed": True,
        "has_crew": True,
        "escape_master": True,
    },
    {
        "name": None,
        "nickname": "Ghost Drift",
        "reward": 4500,
        "latitude": None,
        "longitude": None,
        "location_note": "Identity unknown; operates in nebula lanes",
        "difficulty": 5,
        "armed": False,
        "has_crew": False,
        "escape_master": True,
    },
    {
        "name": "Mira Voss",
        "nickname": "Chrome Fox",
        "reward": 8000,
        "latitude": "33.210000",
        "longitude": "101.550000",
        "location_note": "Cargo docks of Station Helix",
        "difficulty": 6,
        "armed": True,
        "has_crew": False,
        "escape_master": False,
    },
    {
        "name": "Orin Kade",
        "nickname": "Asteroid King",
        "reward": 15000,
        "latitude": "-8.900000",
        "longitude": "72.300000",
        "location_note": "Hidden base in Kepler Belt",
        "difficulty": 9,
        "armed": True,
        "has_crew": True,
        "escape_master": False,
    },
    {
        "name": "Sera Quill",
        "nickname": "Quiet Spark",
        "reward": 3000,
        "latitude": "0.000000",
        "longitude": "0.000000",
        "location_note": "Rumored to hide on Frontier Outpost 7",
        "difficulty": 3,
        "armed": False,
        "has_crew": False,
        "escape_master": False,
    },
    {
        "name": "Drex Sol",
        "nickname": "Plasma Jackal",
        "reward": 9500,
        "latitude": "54.100000",
        "longitude": "-12.400000",
        "location_note": "Pirate corridor Theta-9",
        "difficulty": 7,
        "armed": True,
        "has_crew": True,
        "escape_master": True,
    },
]


HUNTS = [
    (1, False, "Target escaped through an asteroid field."),
    (1, False, "Crew ambush; retreated to mothership."),
    (1, True, "Captured after chase across Ring of Orpheus."),
    (2, False, "Lost signal in nebula interference."),
    (2, False, "Decoy drone led us into a trap."),
    (3, True, "Arrested at Station Helix cargo dock."),
    (3, False, "First attempt failed; Fox jammed scanners."),
    (4, False, "Base defenses too strong; aborted."),
    (4, False, "Second run — crew scattered us."),
    (5, True, "Quiet Spark surrendered at Outpost 7."),
    (6, False, "Jackal slipped into warp with escorts."),
    (6, True, "Finally boxed in at Theta-9."),
]


class Command(BaseCommand):
    help = "Prefill database with sample criminals and hunt logs (idempotent)."

    def handle(self, *args, **options):
        if WantedCriminal.objects.exists():
            self.stdout.write(self.style.WARNING("Seed skipped: criminals already exist."))
            return

        criminals = []
        for data in CRIMINALS:
            criminals.append(WantedCriminal.objects.create(**data))

        for criminal_index, success, notes in HUNTS:
            HuntLog.objects.create(
                criminal=criminals[criminal_index - 1],
                success=success,
                notes=notes,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(criminals)} criminals and {len(HUNTS)} hunt logs."
            )
        )
