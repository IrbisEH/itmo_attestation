drop table if exists books_series cascade;

drop table if exists reviews cascade;

drop table if exists rates cascade;

drop table if exists book_authors cascade;

drop table if exists authors cascade;

drop table if exists book_genre_tags cascade;

drop table if exists genre_tags cascade;

drop table if exists order_items cascade;

drop table if exists books cascade;

drop type if exists cover_type cascade;

drop table if exists orders cascade;

drop type if exists status_type cascade;

drop table if exists users cascade;

drop table if exists roles cascade;

drop type if exists role_name cascade;

drop table if exists sales cascade;

drop function if exists update_book_rating() cascade;

drop function if exists update_order_total_price() cascade;

