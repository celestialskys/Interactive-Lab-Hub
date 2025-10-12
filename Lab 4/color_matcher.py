from typing import Tuple, List, Dict
import colorsys

class ColorMatcher:
    RGB = Tuple[int, int, int]
    RGBA = Tuple[int, int, int, float]

    def __init__(self, color: Tuple[int, int, int, float]):
        """Initialize with an RGBA color."""
        self.r, self.g, self.b, self.a = color

    def complementary(self) -> RGBA:
        """Return complementary RGBA color."""
        r, g, b, a = self.r, self.g, self.b, self.a
        return (255 - r, 255 - g, 255 - b, a)

    def to_hex(self) -> str:
        """Convert to hex (including alpha)."""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}{round(self.a*255):02X}"

    @staticmethod
    def hex_to_rgba(hex_str: str) -> RGBA:
        """Convert hex string (#RRGGBB or #RRGGBBAA) to RGBA tuple."""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            r, g, b = [int(hex_str[i:i+2], 16) for i in (0, 2, 4)]
            a = 1.0
        elif len(hex_str) == 8:
            r, g, b, a = [int(hex_str[i:i+2], 16) for i in (0, 2, 4, 6)]
            a /= 255
        else:
            raise ValueError("Invalid hex length")
        return (r, g, b, a)

# Example usage
if __name__ == "__main__":
    base = ColorMatcher((85, 102, 119, 0.5))
    print("Complementary:", base.complementary())
    print("Hex:", base.to_hex())

    from_hex = ColorMatcher(ColorMatcher.hex_to_rgba("#55667780"))
    print("From hex -> complement:", from_hex.complementary())
