from django.contrib import admin
from django.urls import path, include
from maintenance import views as mt_views

urlpatterns = [
    path('allequipment/', include([
        path('', mt_views.showAllEquipment.as_view()),
        path('add/', mt_views.addEquipment.as_view())]
    )
         ),
    path('allstates/', include([
        path('', mt_views.showallstate.as_view()),
        path('add/', mt_views.addstates.as_view())]
    )
         ),
    path('manage/', include([
        path('', mt_views.showrepair_manage.as_view()),
        path('schedules/', include([
            path('', mt_views.showrepair_schedule.as_view()),
            path('detail/', mt_views.showrepair_scheduledetail.as_view()),
            path('add/', mt_views.addrepair_schedule.as_view())]
        )
             ),
        path('request/', include([
            path('', mt_views.showrepair_request.as_view()),
            path('detail/', mt_views.showrepair_requestdetail.as_view()),
            path('add/', mt_views.addrepair_request.as_view())]
        )
             ),
        path('off/', include([
            path('', mt_views.showrepair_off_req.as_view()),
            path('detail/', mt_views.showrepair_off_reqdetail.as_view()),
            path('add/', mt_views.addrepair_off_req.as_view())]
        )
             ),
        path('accept/', include([
            path('', mt_views.showrepair_accept.as_view()),
            path('detail/', mt_views.showrepair_acceptdetail.as_view()),
            path('add/', mt_views.addrepair_accept.as_view())]
        )
             )
    ]
    )),
]
