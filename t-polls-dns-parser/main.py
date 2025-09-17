from parser import parsing_product_urls, parsing_reviews


if __name__ == "__main__":
    parsing_product_urls()
    parsing_reviews()
    print("Done! All data is in assets/dns_data.csv")
