#!/usr/bin/env python3
"""
Typist Profile Definitions for Thai Numbers Typing Cost Analysis

Defines different typist skill levels with associated keystroke times
and characteristics for typing cost calculations.
"""

from typing import Any, Dict


class TypistProfile:
    """Represents different typist skill levels with associated keystroke times."""

    PROFILES = {
        "expert": {
            "name": "Expert Typist (90 WPM)",
            "keystroke_time": 0.12,
            "description": "Professional typist, ~90 WPM, touch typing mastery",
        },
        "skilled": {
            "name": "Skilled Typist",
            "keystroke_time": 0.20,
            "description": "Experienced office worker, good typing skills",
        },
        "average": {
            "name": "Average Non-secretarial",
            "keystroke_time": 0.28,
            "description": "Average office worker, moderate typing skills (default)",
        },
        "worst": {
            "name": "Worst Typist",
            "keystroke_time": 1.2,
            "description": "Hunt-and-peck typist, very slow typing",
        },
    }

    @classmethod
    def get_profile(cls, profile_name: str) -> Dict[str, Any]:
        """Get a typist profile by name."""
        if profile_name not in cls.PROFILES:
            raise ValueError(f"Unknown typist profile: {profile_name}")
        return cls.PROFILES[profile_name]

    @classmethod
    def list_profiles(cls) -> None:
        """Print formatted list of available typist profiles."""
        print("Available Typist Profiles:")
        print("-" * 50)
        for key, profile in cls.PROFILES.items():
            print(
                f"  {key:<8}: {profile['name']} ({profile['keystroke_time']}s per keystroke)"
            )
            print(f"           {profile['description']}")
            print()

    @classmethod
    def get_all_profiles(cls) -> Dict[str, Dict[str, Any]]:
        """Get all available typist profiles."""
        return cls.PROFILES.copy()


if __name__ == "__main__":
    """Demonstrate typist profile functionality."""
    import sys

    print("🎯 Thai Numbers Typing Cost Analysis - Typist Profiles Module")
    print("=" * 70)

    # List all profiles
    TypistProfile.list_profiles()

    # Test profile retrieval
    if len(sys.argv) > 1:
        profile_name = sys.argv[1]
        try:
            profile = TypistProfile.get_profile(profile_name)
            print(f"✅ Retrieved profile '{profile_name}':")
            print(f"   Name: {profile['name']}")
            print(f"   Keystroke time: {profile['keystroke_time']}s")
            print(f"   Description: {profile['description']}")
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("Use one of the available profile names above.")
            sys.exit(1)
    else:
        print("💡 Usage: python typist_profiles.py [profile_name]")
        print("   Example: python typist_profiles.py average")

    print("\n✅ Typist profiles module test completed successfully!")
