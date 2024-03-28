from enum import Enum

from PIL import ImageColor


class DefinedColor(Enum):
    AliceBlue = "#F0F8FF"
    Amethyst = "#9966CC"
    AntiqueWhite = "#FAEBD7"
    Aqua = "#00FFFF"
    Aquamarine = "#7FFFD4"
    Azure = "#F0FFFF"
    Beige = "#F5F5DC"
    Bisque = "#FFE4C4"
    Black = "#000000"
    BlanchedAlmond = "#FFEBCD"
    Blue = "#0000FF"
    BlueViolet = "#8A2BE2"
    Brown = "#A52A2A"
    BurlyWood = "#DEB887"
    CadetBlue = "#5F9EA0"
    Chartreuse = "#7FFF00"
    Chocolate = "#D2691E"
    Coral = "#FF7F50"
    CornflowerBlue = "#6495ED"
    Cornsilk = "#FFF8DC"
    Crimson = "#DC143C"
    Cyan = "#00FFFF"
    DarkBlue = "#00008B"
    DarkCyan = "#008B8B"
    DarkGoldenrod = "#B8860B"
    DarkGray = "#A9A9A9"
    DarkGreen = "#006400"
    DarkKhaki = "#BDB76B"
    DarkMagenta = "#8B008B"
    DarkOliveGreen = "#556B2F"
    DarkOrange = "#FF8C00"
    DarkOrchid = "#9932CC"
    DarkRed = "#8B0000"
    DarkSalmon = "#E9967A"
    DarkSeaGreen = "#8FBC8F"
    DarkSlateBlue = "#483D8B"
    DarkSlateGray = "#2F4F4F"
    DarkSlateGrey = "#2F4F4F"
    DarkTurquoise = "#00CED1"
    DarkViolet = "#9400D3"
    DeepPink = "#FF1493"
    DeepSkyBlue = "#00BFFF"
    DimGray = "#696969"
    DimGrey = "#696969"
    DodgerBlue = "#1E90FF"
    FireBrick = "#B22222"
    FloralWhite = "#FFFAF0"
    ForestGreen = "#228B22"
    Fuchsia = "#FF00FF"
    Gainsboro = "#DCDCDC"
    GhostWhite = "#F8F8FF"
    Gold = "#FFD700"
    Goldenrod = "#DAA520"
    Gray = "#808080"
    Grey = "#808080"
    Green = "#008000"
    GreenYellow = "#ADFF2F"
    Honeydew = "#F0FFF0"
    HotPink = "#FF69B4"
    IndianRed = "#CD5C5C"
    Indigo = "#4B0082"
    Ivory = "#FFFFF0"
    Khaki = "#F0E68C"
    Lavender = "#E6E6FA"
    LavenderBlush = "#FFF0F5"
    LawnGreen = "#7CFC00"
    LemonChiffon = "#FFFACD"
    LightBlue = "#ADD8E6"
    LightCoral = "#F08080"
    LightCyan = "#E0FFFF"
    LightGoldenrodYellow = "#FAFAD2"
    LightGreen = "#90EE90"
    LightGrey = "#D3D3D3"
    LightPink = "#FFB6C1"
    LightSalmon = "#FFA07A"
    LightSeaGreen = "#20B2AA"
    LightSkyBlue = "#87CEFA"
    LightSlateGray = "#778899"
    LightSlateGrey = "#778899"
    LightSteelBlue = "#B0C4DE"
    LightYellow = "#FFFFE0"
    Lime = "#00FF00"
    LimeGreen = "#32CD32"
    Linen = "#FAF0E6"
    Magenta = "#FF00FF"
    Maroon = "#800000"
    MediumAquamarine = "#66CDAA"
    MediumBlue = "#0000CD"
    MediumOrchid = "#BA55D3"
    MediumPurple = "#9370DB"
    MediumSeaGreen = "#3CB371"
    MediumSlateBlue = "#7B68EE"
    MediumSpringGreen = "#00FA9A"
    MediumTurquoise = "#48D1CC"
    MediumVioletRed = "#C71585"
    MidnightBlue = "#191970"
    MintCream = "#F5FFFA"
    MistyRose = "#FFE4E1"
    Moccasin = "#FFE4B5"
    NavajoWhite = "#FFDEAD"
    Navy = "#000080"
    OldLace = "#FDF5E6"
    Olive = "#808000"
    OliveDrab = "#6B8E23"
    Orange = "#FFA500"
    OrangeRed = "#FF4500"
    Orchid = "#DA70D6"
    PaleGoldenrod = "#EEE8AA"
    PaleGreen = "#98FB98"
    PaleTurquoise = "#AFEEEE"
    PaleVioletRed = "#DB7093"
    PapayaWhip = "#FFEFD5"
    PeachPuff = "#FFDAB9"
    Peru = "#CD853F"
    Pink = "#FFC0CB"
    Plaid = "#CC5533"
    Plum = "#DDA0DD"
    PowderBlue = "#B0E0E6"
    Purple = "#800080"
    Red = "#FF0000"
    RosyBrown = "#BC8F8F"
    RoyalBlue = "#4169E1"
    SaddleBrown = "#8B4513"
    Salmon = "#FA8072"
    SandyBrown = "#F4A460"
    SeaGreen = "#2E8B57"
    Seashell = "#FFF5EE"
    Sienna = "#A0522D"
    Silver = "#C0C0C0"
    SkyBlue = "#87CEEB"
    SlateBlue = "#6A5ACD"
    SlateGray = "#708090"
    SlateGrey = "#708090"
    Snow = "#FFFAFA"
    SpringGreen = "#00FF7F"
    SteelBlue = "#4682B4"
    Tan = "#D2B48C"
    Teal = "#008080"
    Thistle = "#D8BFD8"
    Tomato = "#FF6347"
    Turquoise = "#40E0D0"
    Violet = "#EE82EE"
    Wheat = "#F5DEB3"
    White = "#FFFFFF"
    WhiteSmoke = "#F5F5F5"
    Yellow = "#FFFF00"
    YellowGreen = "#9ACD32"
    FairyLight = "#FFE42D"
    FairyLightNCC = "#FF9D2A"


class Palette(Enum):
    Cloud = [
        DefinedColor.Blue,
        DefinedColor.DarkBlue,
        DefinedColor.DarkBlue,
        DefinedColor.DarkBlue,
        DefinedColor.DarkBlue,
        DefinedColor.DarkBlue,
        DefinedColor.DarkBlue,
        DefinedColor.DarkBlue,
        DefinedColor.Blue,
        DefinedColor.DarkBlue,
        DefinedColor.SkyBlue,
        DefinedColor.SkyBlue,
        DefinedColor.LightBlue,
        DefinedColor.White,
        DefinedColor.LightBlue,
        DefinedColor.SkyBlue,
    ]
    Heat = [
        "#000000",
        "#330000",
        "#660000",
        "#990000",
        "#CC0000",
        "#FF0000",
        "#FF3300",
        "#FF6600",
        "#FF9900",
        "#FFCC00",
        "#FFFF00",
        "#FFFF33",
        "#FFFF66",
        "#FFFF99",
        "#FFFFCC",
        "#FFFFFF",
    ]
    Lava = [
        DefinedColor.Black,
        DefinedColor.Maroon,
        DefinedColor.Black,
        DefinedColor.Maroon,
        DefinedColor.DarkRed,
        DefinedColor.DarkRed,
        DefinedColor.Maroon,
        DefinedColor.DarkRed,
        DefinedColor.DarkRed,
        DefinedColor.DarkRed,
        DefinedColor.Red,
        DefinedColor.Orange,
        DefinedColor.White,
        DefinedColor.Orange,
        DefinedColor.Red,
        DefinedColor.DarkRed,
    ]
    Ocean = [
        DefinedColor.MidnightBlue,
        DefinedColor.DarkBlue,
        DefinedColor.MidnightBlue,
        DefinedColor.Navy,
        DefinedColor.DarkBlue,
        DefinedColor.MediumBlue,
        DefinedColor.SeaGreen,
        DefinedColor.Teal,
        DefinedColor.CadetBlue,
        DefinedColor.Blue,
        DefinedColor.DarkCyan,
        DefinedColor.CornflowerBlue,
        DefinedColor.Aquamarine,
        DefinedColor.SeaGreen,
        DefinedColor.Aqua,
        DefinedColor.LightSkyBlue,
    ]
    Party = [
        "#5500AB",
        "#84007C",
        "#B5004B",
        "#E5001B",
        "#E81700",
        "#B84700",
        "#AB7700",
        "#ABAB00",
        "#AB5500",
        "#DD2200",
        "#F2000E",
        "#C2003E",
        "#8F0071",
        "#5F00A1",
        "#2F00D0",
        "#0007F9",
    ]
    Rainbow = [
        "#FF0000",
        "#D52A00",
        "#AB5500",
        "#AB7F00",
        "#ABAB00",
        "#56D500",
        "#00FF00",
        "#00D52A",
        "#00AB55",
        "#0056AA",
        "#0000FF",
        "#2A00D5",
        "#5500AB",
        "#7F0081",
        "#AB0055",
        "#D5002B",
    ]

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @staticmethod
    def get_grpc_color(color):
        ...
        # r, g, b = ImageColor.getcolor(color.value if isinstance(color, DefinedColor) else color, "RGB")
        # return led_communication_pb2.Color(r=r, g=g, b=b)

    def grpc_data(self) -> dict:
        ...
        # return led_communication_pb2.Palette(
        #     c1=self.get_grpc_color(self.value[0]),
        #     c2=self.get_grpc_color(self.value[1]),
        #     c3=self.get_grpc_color(self.value[2]),
        #     c4=self.get_grpc_color(self.value[3]),
        #     c5=self.get_grpc_color(self.value[4]),
        #     c6=self.get_grpc_color(self.value[5]),
        #     c7=self.get_grpc_color(self.value[6]),
        #     c8=self.get_grpc_color(self.value[7]),
        #     c9=self.get_grpc_color(self.value[8]),
        #     c10=self.get_grpc_color(self.value[9]),
        #     c11=self.get_grpc_color(self.value[10]),
        #     c12=self.get_grpc_color(self.value[11]),
        #     c13=self.get_grpc_color(self.value[12]),
        #     c14=self.get_grpc_color(self.value[13]),
        #     c15=self.get_grpc_color(self.value[14]),
        #     c16=self.get_grpc_color(self.value[15]),
        # )
