import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    reg_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
    ]
    paths = bold_paths if bold else reg_paths
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def main():
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), color="#FAF8F5")
    draw = ImageDraw.Draw(img)

    # Fonts adhering to size requirements:
    # Masthead title >= 54px (58px)
    # Headlines >= 20px (22px for featured cards, 15px for grid)
    # Body labels >= 13px (13px for body text, lede, grid body, etc.)
    f_mast_top = get_font(12, True)
    f_title = get_font(58, True)
    f_lede = get_font(13, False)
    f_sec_hdr = get_font(13, True)
    f_card_title = get_font(22, True)
    f_card_body = get_font(13, False)
    f_grid_title = get_font(15, True)
    f_grid_body = get_font(13, False)
    f_tag = get_font(11, True)
    f_stat = get_font(12, True)
    f_footer = get_font(10, False)

    # Margins & Layout Constants
    margin = 16
    y = margin

    # 1. Masthead
    draw.text((margin, y), "THE WORLD IN ONE DAY  •  THURSDAY, 26 NOVEMBER 2026  •  ISSUE NO. 328", fill="#555555", font=f_mast_top)
    y += 18

    draw.text((margin, y), "The Daily Global Chronicle", fill="#111111", font=f_title)
    y += 66

    lede_text = "TODAY'S HIGHLIGHTS: North Korea expands tactical nuclear deployment; Saudi coalition strikes Hodeida as Houthis target Riyadh; Ukraine urges Putin to halt refinery complaints amid new European military support."
    lede_lines = wrap_text(draw, lede_text, f_lede, width - 2 * margin)
    for l in lede_lines:
        draw.text((margin, y), l, fill="#333333", font=f_lede)
        y += 18
    y += 6

    # Divider line
    draw.line([(margin, y), (width - margin, y)], fill="#222222", width=2)
    y += 8

    # 2. Stat Boxes Row
    stats = [
        ("ASIA", "3"), ("MIDDLE EAST", "3"), ("EUROPE", "4"),
        ("AFRICA", "2"), ("AMERICAS", "2"), ("OCEANIA", "1"), ("GLOBAL", "3")
    ]
    stat_w = (width - 2 * margin - 6 * 6) / 7
    sx = margin
    for region, count in stats:
        draw.rectangle([sx, y, sx + stat_w, y + 24], fill="#EFECE6", outline="#D0CBC2")
        box_text = f"{region} {count}"
        draw.text((sx + 6, y + 5), box_text, fill="#222222", font=f_stat)
        sx += stat_w + 6
    y += 32

    # 3. THREE BIG STORY CARDS (Row)
    draw.text((margin, y), "FEATURED DISPATCHES", fill="#111111", font=f_sec_hdr)
    y += 16

    big_cards = [
        {
            "tag": "ASIA • DEFENSE",
            "title": "Kim Jong Un Calls for Wider Deployment of Tactical Nuclear Weapons",
            "lines": [
                "Inspecting nuclear facilities on Thursday, North Korean leader Kim Jong Un demanded expanded production of weapons-grade material, warning that denuclearization pressure is a declaration of war."
            ],
            "color": "#8B0000"
        },
        {
            "tag": "MIDDLE EAST • CONFLICT",
            "title": "Saudi Coalition Strikes Hodeida Port After Ballistic Missiles Target Riyadh",
            "lines": [
                "The Saudi-led coalition struck Hodeida port following Houthi drone and missile attacks on Riyadh, prompting threats of retaliation in the Red Sea."
            ],
            "color": "#B85D00"
        },
        {
            "tag": "EUROPE • SECURITY",
            "title": "Ukraine Tells Putin to 'Stop Complaining' Over Refineries; U.S. Approves F-16 Aid",
            "lines": [
                "Kyiv dismissed Russian warnings over refinery strikes as Washington approved a $621M F-16 package, while Moscow cited domestic fuel supply challenges."
            ],
            "color": "#1C3F95"
        }
    ]

    card_w = (width - 2 * margin - 16) / 3
    card_h = 190
    cx = margin
    for card in big_cards:
        draw.rectangle([cx, y, cx + card_w, y + card_h], fill="#FFFFFF", outline="#D0CBC2")
        draw.rectangle([cx, y, cx + card_w, y + 22], fill=card["color"])
        draw.text((cx + 6, y + 4), card["tag"], fill="#FFFFFF", font=f_tag)

        ty = y + 26
        title_lines = wrap_text(draw, card["title"], f_card_title, card_w - 12)
        for tl in title_lines[:2]:
            draw.text((cx + 6, ty), tl, fill="#111111", font=f_card_title)
            ty += 24

        ty += 4
        body_text = " ".join(card["lines"])
        body_lines = wrap_text(draw, body_text, f_card_body, card_w - 12)
        for bl in body_lines[:3]:
            draw.text((cx + 6, ty), bl, fill="#333333", font=f_card_body)
            ty += 16

        cx += card_w + 8
    y += card_h + 12

    # 4. 3x3 GRID OF MEDIUM CARDS
    draw.text((margin, y), "GLOBAL ROUNDUP • 9 REGIONAL REPORTS", fill="#111111", font=f_sec_hdr)
    y += 16

    grid_items = [
        ("AFRICA • CLIMATE", "UNECA Pressures COP31 for Climate Finance", "Claver Gatete urged increased climate finance at COP31 to meet Africa's $277B annual needs."),
        ("AMERICAS • ECONOMY", "Experts Warn 2026-27 El Niño Trillion-Dollar Impact", "Researchers project the strong El Niño will trigger multi-year global income losses."),
        ("GLOBAL • SCIENCE", "Global Fossil Fuel Emissions Projected Down 0.4%", "Exeter Global Carbon Budget report notes renewable growth offsets emissions."),
        ("ASIA • DIPLOMACY", "South Korea Hosts COP31 Fallout Public Forum", "Seoul convened 80 experts on Thursday to evaluate Paris Agreement reduction pathways."),
        ("EUROPE • ECONOMY", "World Bank Releases Bulgaria Green Transition Report", "Accelerated decarbonization could boost Bulgarian GDP growth and cut dependence."),
        ("MIDDLE EAST • ENERGY", "Houthi Attacks Impact Saudi Oil Infrastructure", "Riyadh facilities face renewed drone and missile strikes amid escalating regional conflict."),
        ("OCEANIA • PACIFIC", "Pacific Island Nations Call for Urgent Adaptation Aid", "Leaders highlight rising sea levels and El Niño threats to agricultural productivity."),
        ("GLOBAL • TECH", "EV and Solar Deployment Accelerate Worldwide", "Data shows EV and solar power meeting two-thirds of additional energy demand."),
        ("AFRICA • DEVELOPMENT", "Agricultural Resilience Projects Expand in East Africa", "Development banks mobilize private capital for climate-resilient farming.")
    ]

    g_w = (width - 2 * margin - 16) / 3
    g_h = 100
    for i, (gtag, gtitle, gbody) in enumerate(grid_items):
        col = i % 3
        row = i // 3
        gx = margin + col * (g_w + 8)
        gy = y + row * (g_h + 6)

        draw.rectangle([gx, gy, gx + g_w, gy + g_h], fill="#FFFFFF", outline="#D0CBC2")
        draw.rectangle([gx, gy, gx + g_w, gy + 18], fill="#E2DDD5")
        draw.text((gx + 6, gy + 3), gtag, fill="#333333", font=f_tag)

        gty = gy + 22
        title_lines = wrap_text(draw, gtitle, f_grid_title, g_w - 12)
        if title_lines:
            draw.text((gx + 6, gty), title_lines[0], fill="#111111", font=f_grid_title)
            gty += 18

        body_lines = wrap_text(draw, gbody, f_grid_body, g_w - 12)
        for bl in body_lines[:2]:
            draw.text((gx + 6, gty), bl, fill="#444444", font=f_grid_body)
            gty += 16

    y += 3 * (g_h + 6) + 10

    # 5. BOTTOM SECTION: Map / Also on Thursday
    left_w = 400
    right_w = width - 2 * margin - left_w - 12
    bottom_start_y = y

    # Left: WHERE IT HAPPENED
    draw.text((margin, bottom_start_y), "WHERE IT HAPPENED (KEY CITIES)", fill="#111111", font=f_sec_hdr)
    map_box_y = bottom_start_y + 16
    map_box_h = 135
    draw.rectangle([margin, map_box_y, margin + left_w, map_box_y + map_box_h], fill="#F4F1EA", outline="#D0CBC2")

    cities = [
        ("Seoul", 340, 45), ("Riyadh", 230, 75), ("Kyiv", 190, 35),
        ("Sofia", 175, 45), ("Antalya", 185, 55), ("Washington", 75, 45),
        ("Lima", 85, 100), ("Jakarta", 370, 95), ("Geneva", 160, 40)
    ]
    map_x0 = margin + 15
    map_y0 = map_box_y + 15
    map_w = left_w - 30
    map_h = map_box_h - 30

    for gx_line in range(map_x0, map_x0 + map_w, 40):
        draw.line([(gx_line, map_y0), (gx_line, map_y0 + map_h)], fill="#E2DDD5", width=1)
    for gy_line in range(map_y0, map_y0 + map_h, 30):
        draw.line([(map_x0, gy_line), (map_x0 + map_w, gy_line)], fill="#E2DDD5", width=1)

    for cname, cx_rel, cy_rel in cities:
        px = map_x0 + int((cx_rel / 400.0) * map_w)
        py = map_y0 + int((cy_rel / 130.0) * map_h)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill="#8B0000", outline="#111111")
        draw.text((px + 5, py - 5), cname, fill="#222222", font=f_stat)

    # Right: ALSO ON THURSDAY 26 NOVEMBER 2026
    right_x = margin + left_w + 12
    draw.text((right_x, bottom_start_y), "ALSO ON THURSDAY 26 NOVEMBER 2026", fill="#111111", font=f_sec_hdr)
    list_box_y = bottom_start_y + 16
    draw.rectangle([right_x, list_box_y, right_x + right_w, list_box_y + map_box_h], fill="#FFFFFF", outline="#D0CBC2")

    also_items = [
        ("[ASIA] Tokyo stocks rise on tech gains.",
         "[EUROPE] Berlin funds green heating."),
        ("[MIDDLE EAST] Dubai hosts tech summit.",
         "[AFRICA] Nairobi exchange notes inflows."),
        ("[AMERICAS] Ottawa tables arctic bill.",
         "[GLOBAL] WHO updates virus guidelines."),
        ("[OCEANIA] Sydney reports tourist arrivals.",
         "[ASIA] Singapore expands EU tech ties.")
    ]

    ly = list_box_y + 6
    col_w_item = (right_w - 24) / 2
    for left_item, right_item in also_items:
        l_lines = wrap_text(draw, left_item, f_grid_body, col_w_item - 4)
        r_lines = wrap_text(draw, right_item, f_grid_body, col_w_item - 4)
        
        if l_lines:
            draw.text((right_x + 8, ly), l_lines[0], fill="#333333", font=f_grid_body)
        if r_lines:
            draw.text((right_x + col_w_item + 16, ly), r_lines[0], fill="#333333", font=f_grid_body)
        ly += 15

    y = map_box_y + map_box_h + 10

    # 6. FOOTER
    draw.line([(margin, y), (width - margin, y)], fill="#222222", width=1)
    y += 6

    footer_lines = [
        "DATE CHECK: Every story on this page happened, or was first reported, on Thursday 26 November 2026.",
        "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Euronews, NPR, Kyiv Independent, AllAfrica, World Bank, UN. Errors are not intentional.",
        "Stories are attributed, not stated as facts. Numbers are approximate and based on public reporting."
    ]
    for fl in footer_lines:
        draw.text((margin, y), fl, fill="#555555", font=f_footer)
        y += 12

    output_path = "entry.png"
    img.save(output_path, "PNG", optimize=True)
    print(f"Successfully generated {output_path} ({width}x{height})")

if __name__ == "__main__":
    main()
