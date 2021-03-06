from django.conf.urls import patterns, include, url
from django.contrib import admin
from digispaceapp import views
from django.conf.urls.static import static
from DigiSpace import settings

#from django.views.generic import direct_to_template
from django.views.generic import TemplateView
mobileapp_urlpattern = patterns('',
    # Examples:
    # url(r'^$', 'DigiSpace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/', 'mobileapp.views.consumer_signup',name='signup'),
    url(r'^check-otp/', 'mobileapp.views.check_otp',name='check_otp'),
    url(r'^resend-otp/', 'mobileapp.views.resend_otp',name='resend_otp'),
    url(r'^social-signup/', 'mobileapp.views.social_signup',name='social_signup'),
    url(r'^consumer-login/', 'mobileapp.views.consumer_login',name='login'),
    url(r'^forget-password/', 'mobileapp.views.forgot_password',name='forget-password'),
    url(r'^get-city-list/', 'mobileapp.views.get_city_list',name='get_city_list'),
    url(r'^get-category-list/', 'mobileapp.views.get_category_list',name='get_category_list'),
    url(r'^get-advert-details/', 'mobileapp.views.get_advert_details',name='get_advert_details'),
    url(r'^get-advert-list/', 'mobileapp.views.get_advert_list',name='get_advert_list'),
    url(r'^get-coupon-code/', 'mobileapp.views.get_coupon_code',name='get_coupon_code'),
    url(r'^get-discount-details/', 'mobileapp.views.get_discount_details',name='get_discount_details'),
    url(r'^get-favourite-details/', 'mobileapp.views.get_favourite_details',name='get_favourite_details'),
    url(r'^get-active-discount-details/', 'mobileapp.views.get_active_discount_details',name='get_active_discount_details'),
    url(r'^edit-customer-profile/', 'mobileapp.views.edit_customer_profile',name='edit_customer_profile'),
    url(r'^send-feedback/', 'mobileapp.views.consumer_feedback',name='send_feedback'),
    url(r'^update-device-token/', 'mobileapp.views.update_device_token',name='update_device_token'),
    url(r'^update-profile-photo/', 'mobileapp.views.update_profile_photo',name='update-profile-photo'),
    url(r'^like-advert/', 'mobileapp.views.like_advert',name='like_advert'),
    url(r'^favourite-advert/', 'mobileapp.views.favourite_advert',name='favourite_advert'),
    url(r'^search-advert/', 'mobileapp.views.search_advert',name='search_advert'),
    url(r'^get-category/', 'mobileapp.views.get_category',name='get_category'),
    url(r'^get-category-subcategory-list/', 'mobileapp.views.get_category_subcategory_list',name='get_category_subcategory_list'),
    url(r'^user-logout/', 'mobileapp.views.user_logout',name='user_logout'),
    url(r'^get-bottom-advert-list/', 'mobileapp.views.get_bottom_advert_list',name='get_bottom_advert_list'),
    url(r'^get-top-advert/', 'mobileapp.views.get_top_advert',name='get_top_advert'),
    url(r'^set-notification-settings/', 'mobileapp.views.set_notification_settings',name='set_notification_settings'),
    url(r'^save-sellticket/', 'mobileapp.views.save_sellticket',name='save_sellticket'),
    url(r'^view-list-sellticket/', 'mobileapp.views.view_list_sellticket',name='view_list_sellticket'),
    url(r'^view-sellticket-detail/','mobileapp.views.view_sellticket_detail',name='view_sellticket_detail'),
    url(r'^like-sellticket/', 'mobileapp.views.like_sellticket',name='like_sellticket'),
    url(r'^favourite-sellticket/', 'mobileapp.views.favourite_sellticket',name='favourite_sellticket'),
    url(r'^post-sellticket-review/', 'mobileapp.views.post_sellticket_review',name='post_sellticket_review'),
    url(r'^get-map-advert-list/', 'mobileapp.views.get_map_advert_list',name='get_map_advert_list'),
    url(r'^post-advert-review/', 'mobileapp.views.post_advert_review',name='post_advert_review'),
    url(r'^search-sellticket/', 'mobileapp.views.search_sellticket',name='search_sellticket'),
    url(r'^share-sellticket/', 'mobileapp.views.share_sell_ticket',name='share_sell_ticket'),
    

    url(r'^get-about-city/', 'mobileapp.views.get_about_city',name='get_about_city'),
    url(r'^user-advert-activity/', 'mobileapp.views.user_advert_activity',name='user_advert_activity'),
    url(r'^guest-login/', 'mobileapp.views.guest_login',name='guest_login'),

    url(r'^get-city-star/', 'mobileapp.views.get_city_star',name='get_city_star'),
    url(r'^like-city-star/', 'mobileapp.views.like_city_star',name='like_city_star'),
    url(r'^share-city-star/', 'mobileapp.views.share_city_star',name='share_city_star'),

    #==================================CityLife===================================
    
    url(r'^get-citylife-category-list/', 'mobileapp.views.get_citylife_category_list',name='get_citylife_category_list'),
    url(r'^save-citylife-post/', 'mobileapp.views.save_citylife_post',name='save_citylife_post'),
    url(r'^save-citylife-files/', 'mobileapp.views.save_citylife_files',name='save_citylife_files'),
    url(r'^view-citylife-post/', 'mobileapp.views.view_citylife_post',name='view_citylife_post'),
    url(r'^view-citylife-post-details/', 'mobileapp.views.view_citylife_post_details',name='view_citylife_post_details'),
    url(r'^like-dislike-post/', 'mobileapp.views.like_dislike_post',name='like_dislike_post'),
    url(r'^favourite-post/', 'mobileapp.views.favourite_post',name='favourite_post'),
    url(r'^share-post/', 'mobileapp.views.share_citylife',name='share_post'),

    url(r'^update-post/', 'mobileapp.views.update_post',name='update_post'),
    url(r'^delete-post/', 'mobileapp.views.delete_post',name='delete_post'),

    url(r'^view-favorite-post/', 'mobileapp.views.view_favorite_post',name='view_favorite_post'),
    url(r'^view-active-post/', 'mobileapp.views.view_active_post',name='view_active_post'),
    url(r'^view-all-post/', 'mobileapp.views.view_all_post',name='view_all_post'),
    url(r'^search-post/', 'mobileapp.views.search_post',name='search_post'),
    url(r'^remove-post-file/', 'mobileapp.views.remove_post_file',name='remove_post_file'),

    url(r'^post-comment/', 'mobileapp.views.post_comment',name='post_comment'),
    url(r'^edit-comment/', 'mobileapp.views.edit_comment',name='edit_comment'),
    url(r'^delete-comment/', 'mobileapp.views.delete_comment',name='delete_comment'),
    url(r'^like-dislike-comment/', 'mobileapp.views.like_dislike_comment',name='like_dislike_comment'),

    url(r'^post-reply/', 'mobileapp.views.post_reply',name='post_reply'),
    url(r'^edit-reply/', 'mobileapp.views.edit_reply',name='edit_reply'),
    url(r'^delete-reply/', 'mobileapp.views.delete_reply',name='delete_reply'),
    url(r'^like-dislike-reply/', 'mobileapp.views.like_dislike_reply',name='like_dislike_reply'),

) + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
