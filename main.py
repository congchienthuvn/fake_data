import generators as g
import loader

def main():
    brands = g.gen_brands()
    categories = g.gen_categories()
    sellers = g.gen_sellers()
    customers = g.gen_customers()
    products = g.gen_products(categories, sellers)
    promotions = g.gen_promotions()
    promo_products = g.gen_promotion_products(promotions)

    loader.load_all({
        "brand": brands,
        "category": categories,
        "seller": sellers,
        "customer": customers,
        "product": products,
        "promotion": promotions,
        "promotion_product": promo_products,
    })
    print("Xong!")


if __name__ == "__main__":
    main()