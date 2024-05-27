SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Users`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `Users` (
  `user_id` integer PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `email` varchar(255),
  `password` varchar(255),
  `phone` varchar(255),
  `created_at` timestamp,
  `is_admin` BOOLEAN
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Products`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `Products` (
  `product_id` integer PRIMARY KEY AUTO_INCREMENT,
  `barcode` integer,
  `description` varchar(255),
  `description_ar` varchar(255),
  `price` double,
  `product_img` BLOB,
  `category_id` integer,
  `producing_country` varchar(255),
  `producing_company` varchar(255)
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Categories`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `Categories` (
  `category_id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `group` varchar(255),
  `subgroup` varchar(255)
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Purchases`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `Purchases` (
  `purchase_id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer,
  `purchase_date` timestamp,
  `payment_id` integer UNIQUE
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `PurchaseDetails`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `PurchaseDetails` (
  `purchase_detail_id` integer PRIMARY KEY AUTO_INCREMENT,
  `purchase_id` integer,
  `product_id` integer,
  `quantity` integer
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `PaymentMethods`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `PaymentMethods` (
  `method_id` integer PRIMARY KEY AUTO_INCREMENT,
  `method_name` varchar(255),
  `payment_type` varchar(255),
  `additional_fees` double
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Payments`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `Payments` (
  `payment_id` integer PRIMARY KEY AUTO_INCREMENT,
  `amount` double,
  `method_id` integer,
  `payment_status` varchar(255)
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Coupons`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `Coupons` (
  `coupon_id` integer PRIMARY KEY AUTO_INCREMENT,
  `coupon_code` varchar(255),
  `discount_type` varchar(255),
  `discount_amount` double,
  `valid_from` timestamp,
  `valid_until` timestamp NULL
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `PurchaseCoupons`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `PurchaseCoupons` (
  `purchase_coupon_id` integer PRIMARY KEY AUTO_INCREMENT,
  `purchase_id` integer,
  `coupon_id` integer
);

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `ProductOffers`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `ProductOffers` (
  `offer_id` integer PRIMARY KEY AUTO_INCREMENT,
  `product_id` integer,
  `offer_description` varchar(255),
  `offer_description_ar` varchar(255),
  `offer_img` BLOB,  -- Change 'image' to 'varchar(255)'
  `discount_amount` double,
  `valid_from` timestamp,
  `valid_until` timestamp NULL,
  `min_quantity` integer
);

ALTER TABLE `Purchases` ADD FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`);

ALTER TABLE `Purchases` ADD FOREIGN KEY (`payment_id`) REFERENCES `Payments` (`payment_id`);

ALTER TABLE `PurchaseDetails` ADD FOREIGN KEY (`purchase_id`) REFERENCES `Purchases` (`purchase_id`);

ALTER TABLE `PurchaseDetails` ADD FOREIGN KEY (`product_id`) REFERENCES `Products` (`product_id`);

ALTER TABLE `Payments` ADD FOREIGN KEY (`method_id`) REFERENCES `PaymentMethods` (`method_id`);

ALTER TABLE `PurchaseCoupons` ADD FOREIGN KEY (`purchase_id`) REFERENCES `Purchases` (`purchase_id`);

ALTER TABLE `PurchaseCoupons` ADD FOREIGN KEY (`coupon_id`) REFERENCES `Coupons` (`coupon_id`);

ALTER TABLE `ProductOffers` ADD FOREIGN KEY (`product_id`) REFERENCES `Products` (`product_id`);

ALTER TABLE `Products` ADD FOREIGN KEY (`category_id`) REFERENCES `Categories` (`category_id`);
