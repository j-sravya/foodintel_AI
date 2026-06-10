-- Optional demo seed.
-- Run after 001_initial_schema.sql if you want sample production rows.

insert into companies (name, industry, subscription_plan)
values ('FreshPack Solutions', 'Food packaging sales', 'starter');

insert into seller_categories (company_id, name, product_focus, target_customers)
select id, 'Packaging', 'Leak-proof packaging', 'Restaurants, cafes, cloud kitchens, bakeries and QSR outlets'
from companies
where name = 'FreshPack Solutions';

insert into products (company_id, category_id, name, use_case, competitor_set)
select c.id, sc.id, 'Leak-proof containers', 'Reduce spillage and delivery packaging complaints',
array['UFlex', 'Huhtamaki', 'local disposable wholesalers']
from companies c
join seller_categories sc on sc.company_id = c.id
where c.name = 'FreshPack Solutions' and sc.name = 'Packaging';

insert into prospects (name, city, area, business_type, rating, outlet_count)
values
('Hapyningz Cafe & Kitchen', 'Hyderabad', 'A.S. Rao Nagar', 'Restaurant / Cafe', 4.3, 1),
('Red Bucket Biryani', 'Hyderabad', 'Kukatpally', 'Cloud Kitchen', 4.1, 2),
('Tossin Pizza Gachibowli', 'Hyderabad', 'Gachibowli', 'QSR / Pizza Outlet', 4.2, 1);

