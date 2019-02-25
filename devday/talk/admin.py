from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from talk.forms import SessionReservationForm
from .models import (Room, Talk, TalkFormat, TalkMedia, TalkSlot, TimeSlot,
                     Track, SessionReservation)


class TalkMediaInline(admin.StackedInline):
    model = TalkMedia


class TalkSlotInline(admin.StackedInline):
    model = TalkSlot
    fields = (('room', 'time', 'spots'),)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'event']
    list_filter = ['event']
    ordering = ['-event__title', 'name']


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'draft_speaker', 'event', 'track')
    search_fields = (
        'title', 'draft_speaker__name', 'event__title',
        'track__name')
    list_filter = ['event', 'track']
    inlines = [
        TalkMediaInline,
        TalkSlotInline,
    ]
    ordering = ['title']
    list_select_related = [
        'draft_speaker', 'event', 'track', 'track__event']
    filter_horizontal = ('talkformat',)
    prepopulated_fields = {'slug': ("title",)}
    actions = ['publish_talks']

    def publish_talks(self, request, queryset):
        if 'apply' in request.POST:
            published = 0
            for talk in queryset.all():
                track_field_name = 'selected_track-{}'.format(talk.id)
                if request.POST[track_field_name]:
                    track = Track.objects.get(
                        id=int(request.POST[track_field_name]))
                    talk.publish(track)
                    published += 1
            self.message_user(
                request,
                ngettext_lazy(
                    'One Session has been published.',
                    '%(count)d sessions have been published.',
                    published
                ) % {'count': published})
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'talk/admin/publish_talks.html', context={
            'talks': queryset,
            'tracks': Track.objects.order_by('name')
        })

    publish_talks.short_description = _('Publish selected sessions')


@admin.register(TalkSlot)
class TalkSlotAdmin(admin.ModelAdmin):
    list_display = ['time', 'event', 'room', 'talk', 'spots']
    list_filter = ['time__event']

    # NOTYET autocomplete_fields = list_display

    def event(self, obj):
        return obj.time.event

    event.short_desription = _('Event')


@admin.register(TalkFormat)
class TalkFormatAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'start_time', 'end_time']
    list_filter = ['event']
    ordering = ['-event__title', 'start_time']


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'event']
    list_filter = ['event']
    ordering = ['-event__title', 'name']


@admin.register(SessionReservation)
class SessionReservationAdmin(admin.ModelAdmin):
    list_display = ('email', 'talk_title', 'is_confirmed')
    list_select_related = (
        'attendee', 'talk_slot', 'talk_slot__talk', 'attendee__user')
    list_filter = ('attendee__event', 'is_confirmed')
    ordering = ('talk_slot__talk__title',)
    form = SessionReservationForm

    def email(self, obj):
        return obj.attendee.user.email

    def talk_title(self, obj):
        return obj.talk_slot.talk.title
