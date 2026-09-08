from django.core.management.base import BaseCommand
from store.models import Category, Product
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Seed GlowStock with 60 beauty products"

    def handle(self, *args, **kwargs):

        products = [
            # ---------------- MAKEUP (30) ----------------
            ("Makeup", "Matte Lipstick", "Velora", 599, 15, 35, "Smooth matte lipstick with rich, long-lasting color.", "Vitamin E, Shea Butter, Beeswax", 4.5),
            ("Makeup", "Liquid Lipstick", "Lushé", 699, 10, 28, "Highly pigmented liquid lipstick with a lightweight finish.", "Jojoba Oil, Vitamin E, Silica", 4.6),
            ("Makeup", "Lip Gloss", "GlowMuse", 449, 10, 42, "Glossy lip shine with a comfortable non-sticky feel.", "Castor Oil, Vitamin E, Hyaluronic Acid", 4.4),
            ("Makeup", "Lip Liner", "Belleza", 299, 5, 50, "Creamy lip liner for precise definition.", "Beeswax, Jojoba Oil, Vitamin E", 4.3),
            ("Makeup", "Lip Balm", "PurePetal", 199, 5, 65, "Moisturizing lip balm for soft and hydrated lips.", "Shea Butter, Cocoa Butter, Vitamin E", 4.5),
            ("Makeup", "Lip Tint", "Rosé Glow", 499, 12, 32, "Buildable lip tint for a natural rosy look.", "Aloe Vera, Rose Extract, Glycerin", 4.4),
            ("Makeup", "Lip Plumper", "PlumpPop", 799, 15, 22, "Glossy lip plumper designed for a fuller-looking pout.", "Peppermint Oil, Hyaluronic Acid, Vitamin E", 4.2),
            ("Makeup", "Liquid Foundation", "LumiBase", 899, 20, 18, "Buildable liquid foundation with smooth natural coverage.", "Glycerin, Vitamin E, Squalane", 4.6),
            ("Makeup", "BB Cream", "BareBloom", 649, 10, 45, "Lightweight BB cream combining coverage and hydration.", "Aloe Vera, Niacinamide, SPF", 4.5),
            ("Makeup", "CC Cream", "Complexion Care", 749, 12, 24, "Color-correcting cream for an even-looking complexion.", "Vitamin C, Niacinamide, Glycerin", 4.3),
            ("Makeup", "Concealer", "CoverMuse", 549, 10, 38, "Creamy concealer that blends easily and provides medium coverage.", "Vitamin E, Shea Butter, Glycerin", 4.5),
            ("Makeup", "Compact Powder", "SilkFinish", 499, 8, 55, "Pressed powder for a smooth shine-free finish.", "Kaolin, Silica, Vitamin E", 4.4),
            ("Makeup", "Loose Setting Powder", "CloudVeil", 599, 10, 27, "Fine loose powder that helps set makeup beautifully.", "Silica, Corn Starch, Kaolin", 4.5),
            ("Makeup", "Blush", "RosyPetal", 449, 8, 46, "Soft blendable blush for a naturally flushed look.", "Mica, Vitamin E, Jojoba Oil", 4.6),
            ("Makeup", "Highlighter", "GoldenGlow", 699, 12, 31, "Silky illuminating powder for a radiant glow.", "Mica, Squalane, Vitamin E", 4.7),
            ("Makeup", "Contour Stick", "SculptMuse", 649, 10, 19, "Cream contour stick for effortless face sculpting.", "Shea Butter, Jojoba Oil, Vitamin E", 4.3),
            ("Makeup", "Bronzer", "SunKissed", 599, 8, 37, "Buildable bronzer for a warm sun-kissed complexion.", "Mica, Cocoa Extract, Vitamin E", 4.5),
            ("Makeup", "Makeup Primer", "PerfectCanvas", 699, 10, 29, "Smoothing primer that creates an even makeup base.", "Dimethicone, Glycerin, Vitamin E", 4.6),
            ("Makeup", "Setting Spray", "StayGlow", 649, 12, 33, "Lightweight setting spray to help makeup stay fresh.", "Aloe Vera, Rose Water, Glycerin", 4.4),
            ("Makeup", "Kajal", "KohlMuse", 249, 5, 72, "Deep black kajal with a smooth application.", "Castor Oil, Vitamin E, Wax", 4.5),
            ("Makeup", "Eyeliner", "LineLuxe", 399, 8, 48, "Precision liquid eyeliner with an intense finish.", "Carbon Black, Aloe Vera, Glycerin", 4.4),
            ("Makeup", "Gel Eyeliner", "DramaLine", 499, 10, 26, "Creamy gel eyeliner for bold and defined eyes.", "Beeswax, Jojoba Oil, Vitamin E", 4.3),
            ("Makeup", "Mascara", "LashBloom", 599, 12, 41, "Volumizing mascara for fuller-looking lashes.", "Beeswax, Carnauba Wax, Vitamin E", 4.6),
            ("Makeup", "Eyeshadow Palette", "DreamEyes", 999, 18, 16, "Versatile eyeshadow palette with wearable and bold shades.", "Mica, Talc, Vitamin E", 4.7),
            ("Makeup", "Eyebrow Pencil", "BrowMuse", 349, 8, 39, "Precise eyebrow pencil for naturally defined brows.", "Carnauba Wax, Vitamin E, Jojoba Oil", 4.4),
            ("Makeup", "Eyebrow Gel", "BrowFix", 449, 10, 21, "Clear brow gel for neat and polished brows.", "Aloe Vera, Glycerin, Panthenol", 4.2),
            ("Makeup", "False Eyelashes", "LashLuxe", 499, 10, 24, "Lightweight reusable lashes for dramatic eye looks.", "Synthetic Fiber, Latex-Free Adhesive", 4.3),
            ("Makeup", "Makeup Sponge", "BlendBeauty", 299, 5, 58, "Soft blending sponge for foundation and concealer.", "Hydrophilic Foam", 4.5),
            ("Makeup", "Makeup Brush Set", "BrushBloom", 899, 15, 14, "Complete brush set for everyday makeup application.", "Synthetic Bristles, Aluminum Ferrules", 4.6),
            ("Makeup", "Eyelash Curler", "CurlMuse", 349, 5, 34, "Gentle eyelash curler for lifted-looking lashes.", "Stainless Steel, Silicone Pad", 4.4),

            # ---------------- SKINCARE (12) ----------------
            ("Skincare", "Hydrating Face Wash", "DewDrop", 399, 8, 52, "Gentle cleanser that removes impurities without drying the skin.", "Aloe Vera, Glycerin, Hyaluronic Acid", 4.6),
            ("Skincare", "Vitamin C Serum", "CGlow", 899, 15, 23, "Brightening serum with antioxidant-rich vitamin C.", "Vitamin C, Ferulic Acid, Vitamin E", 4.7),
            ("Skincare", "Niacinamide Serum", "ClearMuse", 699, 10, 31, "Lightweight serum for balanced and healthy-looking skin.", "Niacinamide, Zinc PCA, Hyaluronic Acid", 4.6),
            ("Skincare", "Hyaluronic Acid Serum", "HydraLuxe", 799, 12, 18, "Hydrating serum that helps maintain skin moisture.", "Hyaluronic Acid, Glycerin, Panthenol", 4.7),
            ("Skincare", "Moisturizer", "SoftPetal", 599, 10, 43, "Daily moisturizer for soft, comfortable and hydrated skin.", "Ceramides, Squalane, Glycerin", 4.5),
            ("Skincare", "Sunscreen SPF 50", "SunVeil", 749, 8, 36, "Broad-spectrum SPF 50 sunscreen with a lightweight feel.", "Zinc Oxide, Niacinamide, Vitamin E", 4.6),
            ("Skincare", "Face Toner", "FreshBloom", 449, 5, 29, "Refreshing toner that leaves skin feeling balanced.", "Rose Water, Witch Hazel, Glycerin", 4.4),
            ("Skincare", "Face Mist", "DewMist", 399, 5, 47, "Refreshing facial mist for an instant hydration boost.", "Rose Water, Aloe Vera, Glycerin", 4.5),
            ("Skincare", "Sheet Mask", "GlowSheet", 199, 5, 64, "Hydrating sheet mask for a fresh glowing appearance.", "Hyaluronic Acid, Aloe Vera, Green Tea", 4.5),
            ("Skincare", "Clay Mask", "PureClay", 499, 10, 25, "Purifying clay mask that helps absorb excess oil.", "Kaolin Clay, Green Tea, Zinc", 4.3),
            ("Skincare", "Under Eye Cream", "EyeBloom", 649, 10, 17, "Lightweight eye cream for a refreshed under-eye appearance.", "Caffeine, Peptides, Hyaluronic Acid", 4.4),
            ("Skincare", "Lip Scrub", "SugarPetal", 299, 5, 40, "Gentle sugar scrub for smoother and softer lips.", "Sugar, Shea Butter, Jojoba Oil", 4.5),

            # ---------------- HAIRCARE (8) ----------------
            ("Haircare", "Shampoo", "SilkRoots", 499, 10, 45, "Gentle cleansing shampoo for soft and manageable hair.", "Argan Oil, Aloe Vera, Keratin", 4.5),
            ("Haircare", "Conditioner", "SilkRoots", 549, 10, 39, "Nourishing conditioner for smoother-looking hair.", "Shea Butter, Argan Oil, Keratin", 4.6),
            ("Haircare", "Hair Serum", "GlossLocks", 699, 12, 27, "Lightweight serum that adds shine and smoothness.", "Argan Oil, Vitamin E, Jojoba Oil", 4.5),
            ("Haircare", "Hair Oil", "RootRevive", 449, 8, 53, "Nourishing hair oil blend for healthy-looking hair.", "Coconut Oil, Almond Oil, Amla Extract", 4.4),
            ("Haircare", "Hair Mask", "RepairMuse", 799, 15, 15, "Deep conditioning mask for dry and damaged-looking hair.", "Keratin, Shea Butter, Argan Oil", 4.6),
            ("Haircare", "Dry Shampoo", "FreshLocks", 599, 10, 22, "Quick-refresh dry shampoo for a clean-looking finish.", "Rice Starch, Kaolin, Aloe Vera", 4.2),
            ("Haircare", "Hair Spray", "HoldLuxe", 499, 8, 34, "Flexible hold hairspray for polished hairstyles.", "Panthenol, Aloe Vera, Styling Polymers", 4.3),
            ("Haircare", "Leave-in Conditioner", "SoftStrands", 649, 10, 28, "Lightweight leave-in care for smoother and softer hair.", "Coconut Oil, Aloe Vera, Keratin", 4.5),

            # ---------------- FRAGRANCE (5) ----------------
            ("Fragrance", "Eau de Parfum", "Élan Rose", 1499, 18, 12, "Elegant floral fragrance with a warm sophisticated finish.", "Rose, Jasmine, Vanilla, Musk", 4.7),
            ("Fragrance", "Eau de Toilette", "Blush Aura", 1199, 15, 20, "Fresh everyday fragrance with delicate floral notes.", "Peony, Citrus, Musk", 4.5),
            ("Fragrance", "Body Mist", "PetalCloud", 599, 10, 38, "Light and refreshing floral body mist.", "Rose, Peony, Vanilla", 4.4),
            ("Fragrance", "Perfume Roll-On", "MiniMuse", 449, 8, 31, "Compact roll-on fragrance for easy everyday use.", "Jasmine, Vanilla, Sandalwood", 4.3),
            ("Fragrance", "Fragrance Gift Set", "GlowGifts", 1999, 20, 8, "Beautiful fragrance collection made for gifting.", "Rose, Vanilla, Jasmine, Musk", 4.8),

            # ---------------- BODY CARE (5) ----------------
            ("Body Care", "Body Lotion", "VelvetSkin", 499, 8, 46, "Rich daily body lotion for soft and moisturized skin.", "Shea Butter, Cocoa Butter, Glycerin", 4.6),
            ("Body Care", "Body Wash", "SilkShower", 449, 8, 41, "Gentle body wash with a fresh floral fragrance.", "Aloe Vera, Glycerin, Rose Extract", 4.5),
            ("Body Care", "Body Scrub", "SugarGlow", 549, 10, 29, "Exfoliating body scrub for smoother-looking skin.", "Sugar, Coconut Oil, Vitamin E", 4.5),
            ("Body Care", "Hand Cream", "HandPetal", 299, 5, 57, "Moisturizing hand cream for soft and nourished hands.", "Shea Butter, Glycerin, Vitamin E", 4.4),
            ("Body Care", "Body Butter", "ButterBloom", 699, 12, 18, "Luxurious body butter for deep everyday moisturization.", "Shea Butter, Cocoa Butter, Coconut Oil", 4.7),
        ]

        expiry = date.today() + timedelta(days=365)

        created_count = 0
        updated_count = 0

        for category_name, name, brand, price, discount, stock, description, ingredients, rating in products:

            category = Category.objects.get(name=category_name)

            product, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "category": category,
                    "brand": brand,
                    "description": description,
                    "ingredients": ingredients,
                    "price": price,
                    "discount": discount,
                    "stock": stock,
                    "minimum_stock": 5,
                    "expiry_date": expiry,
                    "rating": rating,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed {len(products)} products. "
                f"Created: {created_count}, Updated: {updated_count}"
            )
        )