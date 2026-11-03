
import random
from datetime import datetime, time, timedelta

from faker import Faker

fake = Faker("vi_VN")
Faker.seed(42)
random.seed(42)

START_2024 = datetime(2024, 1, 1)
END_2024 = datetime(2024, 12, 31)

CATEGORIES = {
    "Electronics": ["Mobile Phones", "Laptops", "Tablets", "Accessories"],
    "Fashion": ["Men's Clothing", "Women's Clothing", "Shoes", "Bags"],
    "Home & Living": ["Furniture", "Kitchenware", "Bedding", "Home Decor"],
    "Beauty & Health": ["Skincare", "Makeup", "Supplements", "Personal Care"],
    "Sports & Outdoors": ["Fitness Equipment", "Sportswear", "Camping", "Cycling"],
}


def gen_brands(n=20):
    return [
        (fake.unique.company(),                       # brand_name (UNIQUE)
         fake.country(),                              # country
         fake.date_time_between(START_2024, END_2024))  # created_at
        for _ in range(n)
    ]


def gen_categories():
    rows = []
    main_names = list(CATEGORIES)
    for name in main_names:
        rows.append((name, None, 1, fake.date_time_between(START_2024, END_2024)))
    for parent_id, parent in enumerate(main_names, start=1):
        for sub in CATEGORIES[parent]:
            rows.append((sub, parent_id, 2, fake.date_time_between(START_2024, END_2024)))
    return rows


def gen_sellers(n=50):
    return [
        (fake.company(),
         fake.date_between(START_2024, END_2024),     # join_date
         random.choice(["Official", "Marketplace"]),
         round(random.uniform(3, 5), 1),
         "Vietnam")
        for _ in range(n)
    ]


def gen_customers(n=30000):
    rows, used_phones = [], set()
    for i in range(1, n + 1):
        gender = random.choice(["Male", "Female"])
        name = fake.name_male() if gender == "Male" else fake.name_female()

        while True:
            phone = "09" + "".join(random.choices("0123456789", k=8))
            if phone not in used_phones:
                used_phones.add(phone)
                break

        rows.append((
            name,
            f"{fake.user_name()}_{i}@{fake.free_email_domain()}",   # email (UNIQUE nhờ có _i)
            phone,
            gender,
            fake.street_address(),
            fake.city(),
            fake.date_time_between(START_2024, END_2024),
        ))
    return rows


def gen_products(categories, sellers, n=3000, n_brands=20):
    sub_ids = [i for i, c in enumerate(categories, start=1) if c[2] == 2]

    rows = []
    for _ in range(n):
        seller_id = random.randint(1, len(sellers))
        join_date = sellers[seller_id - 1][1]
        # sản phẩm không được tạo trước ngày seller tham gia
        start = max(datetime(2024, 6, 1), datetime.combine(join_date, time.min))
        rows.append((
            fake.catch_phrase(),                      # product_name
            random.choice(sub_ids),                   # category_id
            random.randint(1, n_brands),              # brand_id
            seller_id,
            round(random.uniform(100_000, 50_000_000), 2),   # price
            random.randint(0, 500),                   # stock_qty
            round(random.uniform(3, 5), 1),           # rating
            fake.date_time_between(start, END_2024),  # created_at
            random.random() < 0.9,                    # is_active (90% còn bán)
        ))
    return rows


def gen_promotions(n=30):
    rows = []
    for _ in range(n):
        created_at = fake.date_time_between(datetime(2024, 12, 1), datetime(2025, 1, 31))
        start = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 119))
        start = max(start, datetime.combine(created_at.date(), time.min))
        end = min(start + timedelta(days=random.randint(30, 50)), datetime(2025, 5, 31))

        discount_type = random.choice(["percentage", "fixed_amount"])
        if discount_type == "percentage":
            value = random.choice([5, 10, 15, 20, 30, 50])      # %
        else:
            value = random.choice([20, 50, 100, 200]) * 1000    # VND

        rows.append((
            f"{random.choice(['Mega Sale', 'Flash Sale', 'Super Deal', 'Brand Day'])} #{len(rows) + 1}",
            random.choice(["product", "category", "seller", "flash_sale"]),
            discount_type,
            value,
            start.date(),
            end.date(),
            created_at,
        ))
    return rows


def gen_promotion_products(promotions, n_products=3000):
    counts = [17] * 20 + [16] * 10
    rows = []
    for promo_id, k in enumerate(counts, start=1):
        promo = promotions[promo_id - 1]
        created_at, end_date = promo[6], promo[5]
        for product_id in random.sample(range(1, n_products + 1), k):
            rows.append((
                promo_id,
                product_id,
                fake.date_time_between(created_at, datetime.combine(end_date, time.min)),
            ))
    return rows