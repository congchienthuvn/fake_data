
DROP TABLE IF EXISTS order_item CASCADE;
DROP TABLE IF EXISTS "order" CASCADE;
DROP TABLE IF EXISTS promotion_product CASCADE;
DROP TABLE IF EXISTS promotion CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS seller CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS brand CASCADE;

CREATE TABLE brand (
  brand_id    SERIAL PRIMARY KEY,
  brand_name  VARCHAR(100) NOT NULL UNIQUE,
  country     VARCHAR(50),
  created_at  TIMESTAMP
);

CREATE TABLE category (
  category_id         SERIAL PRIMARY KEY,
  category_name       VARCHAR(100) NOT NULL UNIQUE,
  parent_category_id  INT REFERENCES category (category_id),
  level               SMALLINT CHECK (level IN (1, 2)),
  created_at          TIMESTAMP
);

CREATE TABLE seller (
  seller_id    SERIAL PRIMARY KEY,
  seller_name  VARCHAR(150),
  join_date    DATE,
  seller_type  VARCHAR(50) CHECK (seller_type IN ('Official', 'Marketplace')),
  rating       DECIMAL(2,1) CHECK (rating >= 0 AND rating <= 5),
  country      VARCHAR(50)
);

CREATE TABLE customer (
  customer_id    SERIAL PRIMARY KEY,
  customer_name  VARCHAR(150),
  email          VARCHAR(150) UNIQUE,
  phone          VARCHAR(20) UNIQUE,
  gender         VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
  address        VARCHAR(255),
  city           VARCHAR(100),
  created_at     TIMESTAMP
);

CREATE TABLE product (
  product_id    SERIAL PRIMARY KEY,
  product_name  VARCHAR(200),
  category_id   INT REFERENCES category (category_id),
  brand_id      INT REFERENCES brand (brand_id),
  seller_id     INT REFERENCES seller (seller_id),
  price         DECIMAL(12,2) CHECK (price > 0),
  stock_qty     INT CHECK (stock_qty >= 0),
  rating        DECIMAL(2,1) CHECK (rating >= 0 AND rating <= 5),
  created_at    TIMESTAMP,
  is_active     BOOLEAN DEFAULT TRUE
);

CREATE TABLE promotion (
  promotion_id    SERIAL PRIMARY KEY,
  promotion_name  VARCHAR(100),
  promotion_type  VARCHAR(50),
  discount_type   VARCHAR(20) CHECK (discount_type IN ('percentage', 'fixed_amount')),
  discount_value  NUMERIC(10,2) CHECK (
                    discount_value > 0 AND
                    (discount_type = 'fixed_amount' OR discount_value <= 100)),
  start_date      DATE CHECK (start_date >= DATE(created_at)),
  end_date        DATE,
  created_at      TIMESTAMP,
  CHECK (end_date >= start_date)
);

CREATE TABLE promotion_product (
  promo_product_id  SERIAL PRIMARY KEY,
  promotion_id      INT REFERENCES promotion (promotion_id),
  product_id        INT REFERENCES product (product_id),
  created_at        TIMESTAMP,
  UNIQUE (promotion_id, product_id)
);


CREATE TABLE "order" (
  order_id      SERIAL PRIMARY KEY,
  customer_id   INT REFERENCES customer (customer_id),
  order_date    TIMESTAMP,
  status        VARCHAR(20) CHECK (status IN
                ('PLACED','PAID','SHIPPED','DELIVERED','CANCELLED','RETURNED')),
  total_amount  DECIMAL(12,2) CHECK (total_amount >= 0),
  created_at    TIMESTAMP,
  CHECK (created_at >= order_date)
);

CREATE TABLE order_item (
  order_item_id  BIGSERIAL PRIMARY KEY,
  order_id       INT REFERENCES "order" (order_id),
  product_id     INT REFERENCES product (product_id),
  order_date     TIMESTAMP,   -- copy từ order.order_date, dùng để partition theo tháng
  quantity       INT CHECK (quantity > 0),
  unit_price     DECIMAL(12,2) CHECK (unit_price > 0),
  subtotal       DECIMAL(12,2) CHECK (subtotal = quantity * unit_price),
  created_at     TIMESTAMP,
  CHECK (created_at >= order_date)
);